import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import urllib.request
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from airflow.providers.mysql.hooks.mysql import MySqlHook

def get_MySQL_connection():
    hook = MySqlHook(mysql_conn_id='mysql')
    conn = hook.get_conn()
    cur = conn.cursor()
    return conn, cur

# 출판사, 제목, 기자, 본문, 댓글창
def main(driver):
    time.sleep(1)
    total = driver.find_element(By.CLASS_NAME, "end_container")
    title_area = total.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    title_info = title_area.find_element(By.CLASS_NAME, "media_end_head_title")
    title = title_info.text
    pub_info = title_area.find_element(By.CLASS_NAME, "media_end_head_top")
    pub = pub_info.find_element(By.CSS_SELECTOR, "img").get_attribute("title")
    rep_info = title_area.find_element(By.CLASS_NAME, "media_end_head_journalist")
    reporter = rep_info.text
    article_info = title_area.find_element(By.ID, "dic_area")
    article = article_info.text

    try: # 호감순 댓글 확인 가능
        more_comments = title_area.find_element(By.CLASS_NAME, "u_cbox_btn_view_comment")
        comment_exposed = 1
    except: # 댓글 확인 불가
        more_comments = title_area.find_element(By.CLASS_NAME, "simplecmt_link.is_navercomment")
        comment_exposed = 0

    more_comments.click()

    # 메인 기사에서 수집한 데이터는 시간에 따라 바뀌지 않으므로 예외처리 진행
    conn, cur = get_MySQL_connection()
    try:
        sql = f"INSERT INTO comments_db.articles VALUES ('{title}', '{pub}', '{reporter}', '{article}', '{comment_exposed}');"
        cur.execute(sql)
        conn.commit() 
    except: # title이 PK임
        pass
    
    time.sleep(0.5)
    return title

# 더보기 클릭
def more_comments(driver):
    comment_area = driver.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    total_comment = comment_area.find_element(By.ID, "cbox_module")
    time.sleep(0.5)
    # comments_new = total_comment.find_element(By.CLASS_NAME, "u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_new")
    see_more = total_comment.find_element(By.CLASS_NAME, "u_cbox_paginate")
    see_more.click()

# 댓글 통계
def comments_analysis(driver, title):
    comment_area = driver.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    total_comment = comment_area.find_element(By.ID, "cbox_module")
    time.sleep(0.5)
    try:
        comments_num = total_comment.find_element(By.CLASS_NAME, "u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_new")
    except:
        comments_num = total_comment.find_element(By.CLASS_NAME, "u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_favorite")
    comments_cnt = comments_num.find_element(By.CLASS_NAME, "u_cbox_comment_count_wrap")
    comments = comments_cnt.find_elements(By.CSS_SELECTOR, "ul > li")
    total = comments[0].find_elements(By.CSS_SELECTOR, "span")[0].text
    self_removed = comments[1].find_elements(By.CSS_SELECTOR, "span")[0].text
    auto_removed = comments[2].find_elements(By.CSS_SELECTOR, "span")[0].text

    male, female, age_10, age_20, age_30, age_40, age_50, age_60 = '', '', '', '', '', '', '', ''
    try:
        comments_two = comments_num.find_element(By.CLASS_NAME, "u_cbox_chart_wrap.u_cbox_chart_open")
        comments_sex_age = comments_two.find_element(By.CLASS_NAME, "u_cbox_chart_cont_inner")
        comments_sex = comments_sex_age.find_element(By.CLASS_NAME, "u_cbox_chart_sex")
        comments_male = comments_sex.find_element(By.CLASS_NAME, "u_cbox_chart_progress.u_cbox_chart_male")
        male = comments_male.find_elements(By.CSS_SELECTOR, "span")[0].text[:-1]
        comments_female = comments_sex.find_element(By.CLASS_NAME, "u_cbox_chart_progress.u_cbox_chart_female")
        female = comments_female.find_elements(By.CSS_SELECTOR, "span")[0].text[:-1]

        comments_age = comments_sex_age.find_element(By.CLASS_NAME, "u_cbox_chart_age")
        comments_age_total = comments_age.find_elements(By.CLASS_NAME, "u_cbox_chart_progress")
        age_list = []
        for i in comments_age_total:
            age_list.append(i.text[:-5])
        age_10, age_20, age_30, age_40, age_50, age_60 = age_list[0], age_list[1], age_list[2], age_list[3], age_list[4], age_list[5][:-1]
    except:
        pass
    timestamp = datetime.now()

    conn, cur = get_MySQL_connection()
    sql = f"CREATE TABLE IF NOT EXISTS comments_db.users_dist_'{title[:10]}' (title varchar(255),\
                                                                                total int(5),  \
                                                                                self_removed int(5), \
                                                                                auto_removed int(5), \
                                                                                male int(3), \
                                                                                female int(3), \
                                                                                age_10 int(3), \
                                                                                age_20 int(3), \
                                                                                age_30 int(3), \
                                                                                age_40 int(3), \
                                                                                age_50 int(3), \
                                                                                age_60 int(3), \
                                                                                timestamp datetime(),\
                                                                                primary key (timestamp)\
                                                                                ) engine=InnoDB default charset=utf8;"
    cur.execute(sql)
    sql = f"INSERT INTO comments_db.users_dist_'{title[:10]}' VALUES ('{title}', '{total}', '{self_removed}', '{auto_removed}',\
             '{male}', '{female}', '{age_10}', '{age_20}','{age_30}', '{age_40}', '{age_50}', '{age_60}', '{timestamp}');"
    cur.execute(sql)
    conn.commit()     

    return timestamp

# 전체 댓글 수집
def comments(driver, title, timestamp):
    conn, cur = get_MySQL_connection()
    sql = f"CREATE TABLE IF NOT EXISTS comments_db.comments_dist_'{title[:10]}' (title varchar(255),\
                                                                                comment varchar(300),  \
                                                                                good int(6), \
                                                                                bad int(6), \
                                                                                timestamp datetime(), \
                                                                                primary key (comment, timestamp)\
                                                                                ) engine=InnoDB default charset=utf8;"
    cur.execute(sql)
    comment_area = driver.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    total_comments = comment_area.find_element(By.ID, "cbox_module")
    total_comment = total_comments.find_element(By.ID, "cbox_module_wai_u_cbox_content_wrap_tabpanel")
    comments = total_comment.find_elements(By.CSS_SELECTOR, "li")
    for i in comments:
        comment = i.find_element(By.CLASS_NAME, "u_cbox_text_wrap").text
        if comment != '클린봇이 부적절한 표현을 감지한 댓글입니다.' and comment != '작성자에 의해 삭제된 댓글입니다.':
            good_bad = i.find_element(By.CLASS_NAME, "u_cbox_recomm_set")
            good_bads = good_bad.find_elements(By.CSS_SELECTOR, "a > em")
            sql = f"INSERT INTO comments_db.comments_dist_'{title[:10]}' VALUES ('{title}', '{comment}', '{good_bads[0].text}', '{good_bads[1].text}', '{timestamp}');"
            cur.execute(sql)
    conn.commit() 