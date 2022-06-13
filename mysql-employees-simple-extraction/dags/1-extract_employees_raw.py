import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

from common.operators.transfer_sql_to_gcs import MySQLToGCSOperator 

args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'schedule_interval': '@once',
}

dag = DAG(
    dag_id='sql_employees_schema_extraction_raw',
    default_args=args,
    dagrun_timeout=timedelta(minutes=60),
    start_date=days_ago(1),
    schedule_interval='@once',
)

GCP_CONN_ID = 'google_cloud_default'
GCS_BUCKET = 'adamln-datalake1'
EMPLOYEES_RAW_DATA_DIR = '1-raw/mysql-employees/'
MYSQL_CONN_ID = 'mysql_default'

extraction_done = DummyOperator(
    task_id='extraction_done',
    dag=dag)

def create_extraction_operator(
    sql,
    tablename,
    approx_max_file_size_bytes=64000000,
    filedir=EMPLOYEES_RAW_DATA_DIR,
    export_format='parquet',
    bucket=GCS_BUCKET,
    gcp_conn_id = GCP_CONN_ID,
    mysql_conn_id = MYSQL_CONN_ID,
    dag = dag):

    task = MySQLToGCSOperator(
        sql=sql,
        bucket=bucket,
        approx_max_file_size_bytes=approx_max_file_size_bytes,
        filename=filedir+tablename+'_part-{}'+'.'+export_format,
        export_format=export_format,
        gcp_conn_id=gcp_conn_id,
        mysql_conn_id=mysql_conn_id,
        task_id='employees_'+tablename,
        dag=dag,
    )
    task >> extraction_done
    return task

# extraction
t1 = create_extraction_operator(sql='./sql/1-raw/departments.sql', tablename='departments')
t2 = create_extraction_operator(sql='./sql/1-raw/dept_emp.sql', tablename='dept_emp')
t3 = create_extraction_operator(sql='./sql/1-raw/dept_manager.sql', tablename='dept_manager')
t4 = create_extraction_operator(sql='./sql/1-raw/employees.sql', tablename='employees')
t5 = create_extraction_operator(sql='./sql/1-raw/salaries.sql', tablename='salaries')
t6 = create_extraction_operator(sql='./sql/1-raw/titles.sql', tablename='titles')

# t1 >> t2 >> t3 >> t4 >> t5 >> t6

if __name__ == "__main__":
    dag.cli()