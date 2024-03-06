# Technical challenge

## Goal
Build a simple data pipeline & visualisation in python on order data, and extract some knowledge.

## Description

### 01_preliminary_data_exploration

In this first part we take a step back and quickly explore the data to understand it better. This section consists of a jupyter notebook. You can view the notebook with your preferred editor. No need to run the notebook (the results are stored in it).

### 02_data_pipeline

To ingest the csv files and analyze the data, we use a small-scale data pipeline with the following stack:

- orchestrator: Apache Airflow
- data warehouse: PostgreSQL database
- visualization engine: Metabase

These tools are configured and packaged in docker containers. 

### 03_basket_orders_analysis

Once the data is properly stored, we can use Metabase and data analysis principles to pull insights from the data. You will find a simple sales dashboard in Metabase (see the `Useful links` section). This dashboard is completed by an analysis availalable at `./03_basket_orders_analysis/analysis.md`.

## Prerequisites for the pipeline host

- docker>=20.0.0
- docker-compose>=1.29.2
- Available ports: 8080, 5432, 3000

## How to setup the pipeline

`cd` into the root of the project.

To setup the data pipeline:

    ./run.sh

Once the containers are running, wait a few minutes for everything to setup. Then go to the `Useful links` section or the `How to load and visualize data` section.

To stop the data pipeline:
    
    ./stop.sh


Tips:
- At first launch, the pipeline takes a few minutes to setup, be patient.
- Run as user (not root) to avoid permission issues
- The scripts are configured to call `docker-compose`, if you use docker desktop, please replace `docker-compose` with `docker compose` in both run.sh and stop.sh

### Useful links

With the default configuration the following links will lead you to the web UI of different tools:

- [Airflow](http://localhost:8080) (login: airflow, pwd: airflow)
- [Metabase](http://localhost:3000/) (login: metabase@metabase.com, pwd: metabase123)

The postgreSQL data warehouse is running on 5432 (login: postgres, password: postgres)

##  How to load and visualize data

To run the ETL on a new csv file:

-   Drop the input file in `./02_data_pipeline/data/raw_data/`
-   Optional `chmod 777 ./02_data_pipeline/data/raw_data/my_file.csv` because of permission issues
-  Go to the [pipeline page in airflow](http://localhost:8080/dags/order_csv_ingestion/grid?root=)
-  Run the pipeline. (play button top right corner)
-  Optional go to the [Metabase dashboard](http://localhost:3000/dashboard/2-orders-and-baskets-analysis) and enjoy the dynamic update!

## Possible improvements 

-   Data management
-   Better permission management (for now some punctual use of chmod 777 might help sometimes)
-   Better deployment (setup.sh file)
-   Improve the data pipeline (record wise ingestion, failure management, data quality, etc.)
-   Testing dag(s)
-   Better duplicate management
-   More modular code in airflow
-   Triggering the pipeline when there is a new file directory
-   Security (versions, logins, secret keys)
-   Optimize pipeline for more data
-   Save Metabase SQL requests externally