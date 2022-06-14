import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

import json, os, sys 
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

from common.operators.transfer_sql_to_gcs import MySQLToGCSOperator 

GCP_CONN_ID = 'google_cloud_default'
MYSQL_CONN_ID = 'mysql_default'
GCS_BUCKET = '<YOUR-GCS-BUCKET>'
EMPLOYEES_RAW_DATA_DIR = '<target-directory-in-GCS>/mysql-employees/'
SCHEMA_FILEPATH = '/schema/extraction.json'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'schedule_interval': '@once',
}

dag = DAG(
    dag_id='sql_employees_schema_extraction_raw',
    default_args=default_args,
    dagrun_timeout=timedelta(minutes=60),
    start_date=days_ago(1),
    schedule_interval='@once',
)

begin_extraction = DummyOperator(
    task_id='begin_extraction',
    dag=dag)

extraction_done = DummyOperator(
    task_id='extraction_done',
    dag=dag)

def create_extraction_operator(
    sql,
    tablename,
    schema_filepath=None,
    schema=None,
    filedir=EMPLOYEES_RAW_DATA_DIR,
    export_format='csv',
    bucket=GCS_BUCKET, 
    gcp_conn_id = GCP_CONN_ID,
    mysql_conn_id = MYSQL_CONN_ID,
    dag = dag):

    if (schema_filepath is not None):
        with open(
            os.path.abspath(os.path.dirname(__file__)) + schema_filepath, 'r'
        ) as f:
            schema = json.load(f)

    task = MySQLToGCSOperator(
        sql=sql,
        bucket=bucket,
        schema=schema,
        filename=filedir+tablename+'_part-{}'+'.'+export_format,
        export_format=export_format,
        gcp_conn_id=gcp_conn_id,
        mysql_conn_id=mysql_conn_id,
        task_id='employees_'+tablename,
        dag=dag,
    )
    begin_extraction >> task
    task >> extraction_done
    return task

# extraction
t1 = create_extraction_operator(sql='./sql/extract/departments.sql', tablename='departments')
t2 = create_extraction_operator(sql='./sql/extract/dept_emp.sql', tablename='dept_emp')
t3 = create_extraction_operator(sql='./sql/extract/dept_manager.sql', tablename='dept_manager')
t4 = create_extraction_operator(sql='./sql/extract/employees.sql', tablename='employees')
t5 = create_extraction_operator(sql='./sql/extract/salaries.sql', tablename='salaries')
t6 = create_extraction_operator(sql='./sql/extract/titles.sql', tablename='titles')

if __name__ == "__main__":
    dag.cli()