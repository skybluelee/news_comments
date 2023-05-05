from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

from crawling_functions import more_comments, comments_analysis

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://n.news.naver.com/article/comment/119/0002709755")

# while(1):
#     try:
#         more_comments(driver)
#     except:
#         break
# time.sleep(2)

a,b,c = comments_analysis(driver)
print(a,b,c)