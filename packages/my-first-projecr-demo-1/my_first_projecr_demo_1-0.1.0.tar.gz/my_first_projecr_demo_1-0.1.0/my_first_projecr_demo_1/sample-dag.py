"""A liveness prober dag for monitoring composer.googleapis.com/environment/healthy."""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.operators import python_operator
from google.cloud import datastore
from my_first_projecr_demo_1.create_records_in_datastore import create_record_table1, create_recod_table2

datastore_client = datastore.Client()

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'sample_dag1',
    default_args=default_args,
    description='My first smaple dag program',
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=20))

# priority_weight has type int in Airflow DB, uses the maximum.
hello_python = python_operator.PythonOperator(
        task_id='create_records01',
        python_callable= create_record_table1(datastore_client, "Task", "54321")
)

