from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

from crawling_functions import more_comments, comments_analysis, main, comments

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get("https://n.news.naver.com/article/comment/119/0002709755")
# driver.get("https://n.news.naver.com/article/119/0002709755")
# driver.get("https://n.news.naver.com/mnews/article/005/0001606450")
# driver.get("https://n.news.naver.com/mnews/article/comment/005/0001606450")
driver.get("https://n.news.naver.com/mnews/article/025/0003281914?sid=100")

# a = comments_analysis(driver)
# print(a)

pub, title, reporter, article, timestamp = main(driver) # 본문에서 크롤링 후 댓글창으로 이동
print(timestamp)
print(type(timestamp))
total, self_removed, auto_removed, male, female, age_10, age_20, age_30, age_40, age_50, age_60, now = comments_analysis(driver)
while(1): # 모든 댓글이 나올때까지 더보기 클릭
    try:
        more_comments(driver)
    except:
        break
comments_list = comments(driver)
print(len(comments_list))