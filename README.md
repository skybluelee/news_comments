# news_comments
네이버 기사의 댓글을 Airflow를 이용해 10분 간격으로 크롤링한 결과를 MySQL에 저장한 후 S3에 업로드한다.
이후 Zeppelin에서 Spark SQL을 사용하여 데이터를 정리하여 Redshift에 업로드 ...

# Airflow Extend
## selenium docker image pull
selenium의 경우 Airflow Docker image에 기본적으로 포함되지 않으므로 Extend하여 Airflow를 실행해야 한다.
```
docker pull selenium/standalone-chrome
```
```
$ docker images
REPOSITORY                      TAG       IMAGE ID       CREATED        SIZE
selenium/standalone-chrome      latest    b4da11a7c583   2 days ago     1.29GB
```
**Note: Only one Standalone container can run on port 4444 at the same time.**
selenium container는 동시에 수행되지 않는다.
-> 여러 dag를 실행하더라도 dag는 하나씩 수행한다(나머지는 대기).
## 동시에 dag 실행하기
docker image의 이름을 변경한다.
```
$ ocker image tag selenium/standalone-chrome:latest selenium/standalone-chrome:v1
```
## 
