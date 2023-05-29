# news_comments
네이버 기사의 댓글을 Airflow를 이용해 10분 간격으로 크롤링한 결과를 MySQL에 저장한 후 S3에 업로드한다. 이후 Zeppelin에서 Spark SQL을 사용하여 데이터를 필터링하고 Redshift에 업로드. 마지막으로 Redshift에서 얻은 데이터를 dataframe으로 만들어 시각화를 진행한다.

**이 글은 댓글 분석 결과를 서술하며, 기타 프로그램 설명은 각 폴더에 존재함**

