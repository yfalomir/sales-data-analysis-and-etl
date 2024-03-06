/bin/echo -e "AIRFLOW_UID=$(id -u)" >> ./02_data_pipeline/.env
docker-compose -f 02_data_pipeline/docker-compose.yml up -d
