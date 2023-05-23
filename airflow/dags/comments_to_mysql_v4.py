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

#---------------------------------------------------------------
# end_date 수정!
dag = DAG(
    dag_id = 'Comment_Extract_4',
    start_date = datetime(2023,5,10), # 날짜가 미래인 경우 실행이 안됨
    end_date = datetime(2023, 5, 17, 14, 0), # UTC기준으로 동작
    schedule = '8/10 * * * *',  # 10분마다 업데이트
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    }
)

def etl(**context):
    sql_num = context["params"]["sql_num"]
    remote_webdriver = 'remote_chromedriver4'
    with webdriver.Remote(f'{remote_webdriver}:4444/wd/hub', options=options) as driver:
        # Scraping part
        driver.get(context["params"]["link"])
        title = crawling_functions.main(driver)
        timestamp = crawling_functions.comments_analysis(driver, title, sql_num)

        while(1): # 모든 댓글이 나올때까지 더보기 클릭
            try:
                crawling_functions.more_comments(driver)
            except:
                break
        crawling_functions.comments(driver, title, timestamp, sql_num)

#---------------------------------------------------------------
# link 수정!   
etl = PythonOperator(
    task_id = 'etl',
    python_callable = etl,
    execution_timeout=timedelta(seconds=600), # 10분내에 성공하지 못하면 retry
    # 메인 기사 링크
    params = {
        "link": "https://n.news.naver.com/mnews/article/277/0005260463?sid=100",
        "sql_num" : "_2"
    },
    dag = dag
)

etl