from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.models import Variable

from datetime import datetime
from datetime import timedelta

import requests
import logging
import psycopg2
import json

from functions import crawling_functions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from airflow.providers.mysql.hooks.mysql import MySqlHook

options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1200x600')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

dag = DAG(
    dag_id = 'Comment_Extract',
    start_date = datetime(2023,5,10), # 날짜가 미래인 경우 실행이 안됨
    end_date = datetime(2023, 5, 17, 14, 0), # UTC기준으로 동작
    schedule = '0/10 * * * *',  # 10분마다 업데이트
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    }
)

def etl(**context):
    remote_webdriver = 'remote_chromedriver'
    with webdriver.Remote(f'{remote_webdriver}:4444/wd/hub', options=options) as driver:
        # Scraping part
        driver.get(context["params"]["link"])
        title = crawling_functions.main(driver)
        timestamp = crawling_functions.comments_analysis(driver, title)

        while(1): # 모든 댓글이 나올때까지 더보기 클릭
            try:
                crawling_functions.more_comments(driver)
            except:
                break
        crawling_functions.comments(driver, title, timestamp)
    
etl = PythonOperator(
    task_id = 'etl',
    python_callable = etl,
    execution_timeout=timedelta(seconds=600), # 10분내에 성공하지 못하면 retry
    # 메인 기사 링크
    params = {
        "link": "https://n.news.naver.com/mnews/article/277/0005260463?sid=100"
    },
    dag = dag
)

etl

# schema = "kusdk"
# table = "nps"
# s3_bucket = "grepp-data-engineering"
# s3_key = schema + "-" + table       # s3_key = schema + "/" + table


# mysql_to_s3_nps = SqlToS3Operator(
#     task_id = 'mysql_to_s3_nps',
#     query = "SELECT * FROM prod.nps WHERE DATE(created_at) = DATE('{{ execution_date }}')",
#     s3_bucket = s3_bucket,
#     s3_key = s3_key,
#     sql_conn_id = "mysql_conn_id",
#     aws_conn_id = "aws_conn_id",
#     verify = False,
#     replace = True,
#     pd_kwargs={"index": False, "header": False},    
#     dag = dag
# )

# s3_to_redshift_nps = S3ToRedshiftOperator(
#     task_id = 's3_to_redshift_nps',
#     s3_bucket = s3_bucket,
#     s3_key = s3_key,
#     schema = schema,
#     table = table,
#     copy_options=['csv'],
#     redshift_conn_id = "redshift_dev_db",
#     aws_conn_id = "aws_conn_id",
#     method = "UPSERT",
#     upsert_keys = ["id", "created_at"],
#     dag = dag
# )

# mysql_to_s3_nps >> s3_to_redshift_nps

# import pymysql

# con = pymysql.connect(host='localhost', user='root', password='', \
#                        db='comments_db', charset='utf8') # 한글처리 (charset = 'utf8')
# cur = con.cursor()
# sql = "BEGIN;DELETE FROM comments_db.comments;"
# sql = "SELECT player, birth FROM baseball"
# cur.execute(sql)
 
# rows = cur.fetchall()
# print(rows)     # 전체 rows

# con.close()