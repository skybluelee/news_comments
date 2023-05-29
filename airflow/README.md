# 사용환경
aws ubuntu t3.large

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
### 동시에 dag 실행하기
docker image의 이름을 변경한다.
```
docker image tag selenium/standalone-chrome:latest selenium/standalone-chrome:v1
```
최대 몇개까지 동작하는지는 테스트해보지 않음
```
$ docker images
REPOSITORY                      TAG       IMAGE ID       CREATED        SIZE
selenium/standalone-chrome      latest    b4da11a7c583   2 days ago     1.29GB
selenium/standalone-chrome      v1        b4da11a7c583   2 days ago     1.29GB
```
위와 같이 tag가 바뀐 image가 생성된다
## docker-compose.yaml
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.0/docker-compose.yaml'
```
[Airflow Document](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)에서 확인
최신 docker-compose.yaml파일을 다운받는다.
```
vi docker-compose.yaml

...
x-airflow-common:
  &airflow-common
  # In order to add custom dependencies or upgrade provider packages you can use your extended image.
  # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
  # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
  image: ${AIRFLOW_IMAGE_NAME:-extend_airflow:latest}
...
service:
...
  selenium:
    container_name: remote_chromedriver
    image: selenium/standalone-chrome:latest
    ports:
      - 4444:4444
    restart: always
  selenium2: # 병렬 처리시 사용
    container_name: remote_chromedriver2
    image: selenium/standalone-chrome:v1
    ports:
      - 4445:4445 # 포트는 겹치면 run되지 않음
    restart: always
volumes:
  postgres-db-volume:
```
image 이름을 변경하고 docker-compose.yaml 파일에 selenium 파트를 추가한다.
## requirements.txt
``` 
vi requirements.txt

selenium
webdriver_manager
```
필요한 module을 추가한다.
## Dockerfile
```
vi Dockerfile

FROM apache/airflow:2.6.0
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
```
docker extend 조건을 지정한다.
## docker run
```
docker build . --tag extend_airflow:latest
docker compose up -d
```
