from distutils.command.clean import clean
import pendulum
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.bash_operator import BashOperator
from airflow.decorators import dag, task
from airflow.models import Variable


def is_files_to_process(**kwargs) -> bool:
    """Returns if there are files to process"""
    return kwargs['ti'].xcom_pull(
        task_ids='get_files_to_process', key='return_value') != []


@dag(
    start_date=pendulum.yesterday(),
    schedule="0 0 * * *",
    catchup=False,
)
def order_csv_ingestion():
    POSTGRES_CONN_ID = "postgres_default"
    raw_data_dir = Variable.get("raw_data_dir")
    archive_data_dir = Variable.get("archive_data_dir")

    @task
    def get_files_to_process() -> list:
        """Runs through the raw_data folder to return available csv input files"""
        import logging
        from pathlib import Path
        raw_data_dir_path = Path(raw_data_dir)
        files_in_data_dir = raw_data_dir_path.glob("*.csv")
        files_to_process = [
            str(f) for f in files_in_data_dir if f.is_file()]
        logging.info(f"Files to process: {files_to_process}")
        return files_to_process

    """Stop pipeline if there is no file to process"""
    csv_exists = ShortCircuitOperator(
        task_id='csv_exists_short_circuit',
        provide_context=True,
        python_callable=is_files_to_process,
    )

    @task
    def pg_insert(files):
        """Use simple PostgreSQL COPY to import content of input files inside the database
        """
        import logging
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        for f in files:
            logging.info(f"Inserting {f} in database")
            # Check if exists
            pg_hook.copy_expert(
                sql="COPY orders FROM STDIN WITH CSV HEADER",
                filename=f)

    pg_remove_duplicates = PostgresOperator(
        task_id="pg_remove_duplicates",
        postgres_conn_id="postgres_default",
        sql="sql/remove_duplicates.sql"
    )

    """Archiving processed files"""
    cleanup_files = BashOperator(
        task_id="cleanup_files",
        bash_command="bash/cleanup_files.sh",
        env={"RAW_DATA_DIR": raw_data_dir, "ARCHIVE_DATA_DIR": archive_data_dir}
    )

    files_to_process = get_files_to_process()
    insertion = pg_insert(files_to_process)

    files_to_process >> csv_exists >> insertion >> pg_remove_duplicates >> cleanup_files


order_csv_ingestion()
