"""A liveness prober dag for monitoring composer.googleapis.com/environment/healthy."""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.operators import python_operator
from google.cloud import datastore
from my_first_projecr_demo_1.create_records_in_datastore import create_record_table1, create_recod_table2



def _call_func():
    datastore_client = datastore.Client()
    start_time = time.perf_counter()
    p1 = mp.Process(target=create_record_table1, args=(datastore_client, "Task", "12345623784574"))
    p2 = mp.Process(target=create_recod_table2, args=(datastore_client, "Employee_table", "234564438589475"))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end_time = time.perf_counter()
    print(f"Done with datastore update... in {round(end_time- start_time, 2)} second(s)")


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
        python_callable=_call_func,
        dag=dag
)

