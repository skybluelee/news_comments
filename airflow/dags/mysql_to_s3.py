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
import pandas as pd

def get_MySQL_connection():
    hook = MySqlHook(mysql_conn_id='mysql')
    conn = hook.get_conn()
    cur = conn.cursor()
    return conn, cur

def article_update():
    conn, cur = get_MySQL_connection()
    sql = "SELECT * FROM comments_db.articles_temp;"
    df = pd.read_sql_query(sql,conn)
    for i in range(5):
        title, pub, reporter, article, comment_exposed, input_time = df.loc[i, 'title'], df.loc[i, 'pub'], df.loc[i, 'reporter'], df.loc[i, 'article'], df.loc[i, 'comment_exposed'], df.loc[i, 'written_time']
        sql = f"INSERT INTO comments_db.articles VALUES ('{title}', '{pub}', '{reporter}', '{article}', '{comment_exposed}', '{input_time}');"
        cur.execute(sql) 
    conn.commit()        

def get_title():
    title_list = [0,0,0,0,0]
    conn, cur = get_MySQL_connection()
    sql = "SELECT * FROM comments_db.articles_temp;"
    df = pd.read_sql_query(sql,conn)
    for i in range(5):
        title = df.loc[i, 'title']
        id = df.loc[i, 'id']
        title_list[id] = title
        cur.execute(sql)
    return title_list[0], title_list[1], title_list[2], title_list[3], title_list[4]

def delete_table():
    conn, cur = get_MySQL_connection()
    sql = 'DELETE FROM comments_db.articles_temp;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.user_distribution_0;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.comments_0;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.user_distribution_1;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.comments_1;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.user_distribution_2;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.comments_2;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.user_distribution_3;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.comments_3;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.user_distribution_4;'
    cur.execute(sql)
    sql = 'DELETE FROM comments_db.comments_4;'
    cur.execute(sql)
    conn.commit() 

dag = DAG(
    dag_id = 'mysql_to_s3',
    start_date = datetime(2022,8,24), # 날짜가 미래인 경우 실행이 안됨
    schedule = '0 8 * * *',  # etl이 끝나는 시간에 맞춤
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

etl = PythonOperator(
    task_id = 'delete_table',
    python_callable = delete_table,
    dag = dag
)

article_update = PythonOperator(
    task_id = 'article_update',
    python_callable = article_update,
    dag = dag
)

s3_bucket = "news-comments"
title_0, title_1, title_2, title_3, title_4 = get_title()

mysql_to_s3_user_distribution_0 = SqlToS3Operator(
    task_id = 'mysql_to_s3_user_distribution_0',
    query = "SELECT * FROM comments_db.user_distribution_0",
    s3_bucket = s3_bucket,
    s3_key = "user_distribution_" + title_0,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_comments_0 = SqlToS3Operator(
    task_id = 'mysql_to_s3_comments_0',
    query = "SELECT * FROM comments_db.comments_0",
    s3_bucket = s3_bucket,
    s3_key = "comments_" + title_0,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_user_distribution_1 = SqlToS3Operator(
    task_id = 'mysql_to_s3_user_distribution_1',
    query = "SELECT * FROM comments_db.user_distribution_1",
    s3_bucket = s3_bucket,
    s3_key = "user_distribution_" + title_1,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_comments_1 = SqlToS3Operator(
    task_id = 'mysql_to_s3_comments_1',
    query = "SELECT * FROM comments_db.comments_1",
    s3_bucket = s3_bucket,
    s3_key = "comments_" + title_1,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_user_distribution_2 = SqlToS3Operator(
    task_id = 'mysql_to_s3_user_distribution_2',
    query = "SELECT * FROM comments_db.user_distribution_2",
    s3_bucket = s3_bucket,
    s3_key = "user_distribution_" + title_2,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_comments_2 = SqlToS3Operator(
    task_id = 'mysql_to_s3_comments_2',
    query = "SELECT * FROM comments_db.comments_2",
    s3_bucket = s3_bucket,
    s3_key = "comments_" + title_2,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_user_distribution_3 = SqlToS3Operator(
    task_id = 'mysql_to_s3_user_distribution_3',
    query = "SELECT * FROM comments_db.user_distribution_3",
    s3_bucket = s3_bucket,
    s3_key = "user_distribution_" + title_3,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_comments_3 = SqlToS3Operator(
    task_id = 'mysql_to_s3_comments_3',
    query = "SELECT * FROM comments_db.comments_3",
    s3_bucket = s3_bucket,
    s3_key = "comments_" + title_3,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_user_distribution_4 = SqlToS3Operator(
    task_id = 'mysql_to_s3_user_distribution_4',
    query = "SELECT * FROM comments_db.user_distribution_4",
    s3_bucket = s3_bucket,
    s3_key = "user_distribution_" + title_4,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

mysql_to_s3_comments_4 = SqlToS3Operator(
    task_id = 'mysql_to_s3_comments_4',
    query = "SELECT * FROM comments_db.comments_4",
    s3_bucket = s3_bucket,
    s3_key = "comments_" + title_4,
    sql_conn_id = "mysql",
    aws_conn_id = "aws",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": True},    
    dag = dag
)

article_update >> mysql_to_s3_user_distribution_0 >> mysql_to_s3_comments_0 >> mysql_to_s3_user_distribution_1 >> mysql_to_s3_comments_1 >> mysql_to_s3_user_distribution_2 >> mysql_to_s3_comments_2 >> mysql_to_s3_user_distribution_3 >> mysql_to_s3_comments_3 >> mysql_to_s3_user_distribution_4 >> mysql_to_s3_comments_4 >> etl