# news_comments
네이버 기사의 댓글을 Airflow를 이용해 10분 간격으로 크롤링한 결과를 MySQL에 저장한 후 S3에 업로드한다.
이후 Zeppelin에서 Spark SQL을 사용하여 데이터를 정리하여 Redshift에 업로드

# Airflow Extend
selenium의 경우 Airflow Docker image에 기본적으로 포함되지 않으므로 Extend하여 Airflow를 실행해야 한다.
```
docker pull selenium/standalone-chrome
```
