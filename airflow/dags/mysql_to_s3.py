from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.models import Variable
from datetime import datetime
from datetime import timedelta
import requests
import logging
import psycopg2
import json
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.mysql.hooks.mysql import MySqlHook

def get_MySQL_connection():
    hook = MySqlHook(mysql_conn_id='mysql')
    conn = hook.get_conn()
    cur = conn.cursor()
    return conn, cur

def delete_table():
    conn, cur = get_MySQL_connection()
    sql = 'DELETE FROM comments_db.users_dist;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.comments;'
    cur.execute(sql)
    conn.commit() 

dag = DAG(
    dag_id = 'mysql_s3_test',
    start_date = datetime(2022,8,24), # 날짜가 미래인 경우 실행이 안됨
    schedule = '0 8 * * *',  # etl이 끝나는 시간에 맞춤
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

# waiting_for_etl = ExternalTaskSensor(
#     task_id='waiting_for_etl',
#     external_dag_id='Comment_Extract',
#     external_task_id='etl',
#     timeout=10*60,
#     # execution_date_fn=lambda x: x,
#     mode='reschedule',
#     dag = dag
# )

etl = PythonOperator(
    task_id = 'delete_table',
    python_callable = delete_table,
    dag = dag
)

schema = "kusdk"
table = "nps"
s3_bucket = "news-comments"
s3_key = schema + "-" + table       # s3_key = schema + "/" + table

mysql_to_s3_user_dist = SqlToS3Operator(
    task_id = 'mysql_to_s3',
    query = "SELECT * FROM comments_db.comments",
    s3_bucket = s3_bucket,
    s3_key = "user_distribution",
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": False},    
    dag = dag
)

mysql_to_s3_comments = SqlToS3Operator(
    task_id = 'mysql_to_s3_nps',
    query = "SELECT * FROM comments_db.comments",
    s3_bucket = s3_bucket,
    s3_key = "comments",
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": False},    
    dag = dag
)

mysql_to_s3_user_dist >> mysql_to_s3_comments>> etl