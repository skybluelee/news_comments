# news_comments
네이버 기사의 댓글을 Airflow를 이용해 10분 간격으로 크롤링한 결과를 MySQL에 저장한 후 S3에 업로드한다. 이후 Zeppelin에서 Spark SQL을 사용하여 데이터를 필터링하고 Redshift에 업로드. 마지막으로 Redshift에서 얻은 데이터를 dataframe으로 만들어 시각화를 진행한다.

**이 글은 댓글 분석 결과를 서술하며, 기타 프로그램 설명은 각 폴더에 존재함**

# 데이터 수집
각 기사에 대해 1시간 30분 동안 10분 단위로 공감순으로 상위 10개의 댓글을 수집.

# 뉴스 댓글 유형
댓글의 경우 공감순(좋아요 순)이 보이는 기사와 보이지 않는 기사가 존재함. 호감순이 존재하지 않는 경우 최신순으로만 댓글이 나열됨.
성별과 나이대의 경우 공개가 되는 기사와 공개가 되지 않는 기사가 존재하며 공개가 되더라도 댓글 수가 100개 이상이 되어야 공개됨.

# 최신순만 존재하는 경우
<img width="80%" src="[https://user-images.githubusercontent.com/16822641/109461495-913fc480-7aa5-11eb-9d0e-aff762669f98.gif](https://github.com/skybluelee/news_comments/assets/107929903/1bb26ff7-d7e7-4ee2-a490-8c5cc18852ce)"/>
