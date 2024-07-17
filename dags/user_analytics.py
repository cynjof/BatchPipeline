import os
import shutil
from datetime import datetime, timedelta
import boto3
import duckdb
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from create_user_behaviour_metric import create_user_behaviour_metric
from get_s3_folder import get_s3_folder


with DAG(
    "user_analytics_dag",
    description="A DAG to Pull user data and movie review data to analyze their behaviour",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    user_analytics_bucket = "user-analytics"

    create_s3_bucket = S3CreateBucketOperator(
        task_id="create_s3_bucket", bucket_name=user_analytics_bucket
    )
    movie_review_to_s3 = LocalFilesystemToS3Operator(
        task_id="movie_review_to_s3",
        filename="/opt/airflow/data/movie_review.csv",
        dest_key="raw/movie_review.csv",
        dest_bucket=user_analytics_bucket,
        replace=True,
    )

    user_purchase_to_s3 = SqlToS3Operator(
        task_id="user_purchase_to_s3",
        sql_conn_id="postgres_default",
        query="select * from retail.user_purchase",
        s3_bucket=user_analytics_bucket,
        s3_key="raw/user_purchase/user_purchase.csv",
        replace=True,
    )

    movie_classifier = BashOperator(
        task_id="movie_classifier",
        bash_command="python /opt/airflow/dags/scripts/spark/random_text_classification.py",
    )

    get_movie_review_to_warehouse = PythonOperator(
        task_id="get_movie_review_to_warehouse",
        python_callable=get_s3_folder,
        op_kwargs={"s3_bucket": "user-analytics", "s3_folder": "clean/movie_review"},
    )

    get_user_purchase_to_warehouse = PythonOperator(
        task_id="get_user_purchase_to_warehouse",
        python_callable=get_s3_folder,
        op_kwargs={"s3_bucket": "user-analytics", "s3_folder": "raw/user_purchase"},
    )

    get_user_behaviour_metric = PythonOperator(
        task_id="get_user_behaviour_metric",
        python_callable=create_user_behaviour_metric,
    )

    markdown_path = "/opt/airflow/dags/scripts/dashboard/"
    q_cmd = f"cd {markdown_path} && quarto render {markdown_path}/dashboard.qmd"
    gen_dashboard = BashOperator(task_id="generate_dashboard", bash_command=q_cmd)

    (
        create_s3_bucket
        >> user_purchase_to_s3
        >> movie_classifier
        >> get_user_purchase_to_warehouse
        >> get_user_behaviour_metric
        >> gen_dashboard,
        create_s3_bucket
        >> movie_review_to_s3
        >> get_movie_review_to_warehouse
        >> get_user_behaviour_metric,
    )