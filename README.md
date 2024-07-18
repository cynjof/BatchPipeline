# Batch Pipeline Project

## Overview
Data Engineering project to set up a batch data pipeline of a company which collects user data and creates a user profile. The data pipeline goal is populate the user_behavior_metric table. The user_behavior_metric table is an OLAP table used by analysts. The data sources are:
- user_purchase: OLTP table with user purchase information.
- movie_review.csv: Data is sent every day by an external data vendor.

### Data Architecture
This data engineering project includes the following:
- Airflow: To schedule and orchestrate DAGs.
- Postgres: This database stores Airflow’s details and has a schema to represent upstream databases.
- DuckDB: To act as our warehouse
- Quarto with Plotly: To convert code in markdown format to HTML files that can be embedded in your app or served as is.
- Apache Spark: This is used to process our data, specifically to run a classification algorithm.
- Minio: To provide an S3 compatible open source storage system.
  
![image](https://github.com/user-attachments/assets/ca4a31fc-72af-4916-a4c5-2db9de5248c9)

![image](https://github.com/user-attachments/assets/e81e4d3b-dce3-42bf-9e72-14280b62f190)


## How to Run This Project

1. Clone the repo
2. Run command: `make up`
3. Go to Airflow UI and run the DAG "user_analytics.py"

## Lessons Learned
Setting up insfrastructure using github codespace. 
Learning new tools like quarto dashboards, Minio and DuckDB data warehouse.

