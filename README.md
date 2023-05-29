# news_comments
네이버 기사의 댓글을 Airflow를 이용해 10분 간격으로 크롤링한 결과를 MySQL에 저장한 후 S3에 업로드한다. 이후 Zeppelin에서 Spark SQL을 사용하여 데이터를 필터링하고 Redshift에 업로드. 마지막으로 Redshift에서 얻은 데이터를 dataframe으로 만들어 시각화를 진행한다.

**이 글은 댓글 분석 결과를 서술하며, 기타 프로그램 설명은 각 폴더에 존재함**

# 데이터 수집
각 기사에 대해 1시간 30분 동안 10분 단위로 공감순으로 상위 10개의 댓글을 수집.

# 뉴스 댓글 유형
댓글의 경우 공감순(좋아요 순)이 보이는 기사와 보이지 않는 기사가 존재함. 호감순이 존재하지 않는 경우 최신순으로만 댓글이 나열됨.
성별과 나이대의 경우 공개가 되는 기사와 공개가 되지 않는 기사가 존재하며 공개가 되더라도 댓글 수가 100개 이상이 되어야 공개됨.

# 최신순만 존재하는 경우
## 댓글의 수가 적은 경우
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/dec950e4-87d1-45d3-943a-f620e4261856"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/a9bf94cd-f0a5-4a46-bdd5-568b2135a357"/>

좋아요 수의 전반적인 증가세를 확인할 수 있고 좋아요 상위 10개의 댓글의 위치의 변동이 심하다. 댓글이 적은 경우 조금 더 많은 댓글을 확인하고 공감이 가는 댓글에 좋아요를 눌렀을 거라고 추측한다.
## 댓글의 수가 많은 경우
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/51e4fc4c-76de-431a-90fd-1ce48e3f55e7"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/50916533-8141-4b53-b2ca-3b1390cbdf3f"/>

상위 7개 가량의 댓글의 좋아요 수는 처음과 마지막이 유사하며 위치 변동 또한 적다. 하위 3개 가량의 댓글의 경우 상위 10개 이내로 새로 들어오거나 나가는 경우가 많다. 이 부분은 최신순의 경우 댓글이 많아질 수록 묻히게 되고 댓글이 적을 때와 달리 전체 댓글을 보는 것이 아닌 눈에 보이는 댓글에 대해 좋아요를 누르기 때문으로 추정된다.

최신순의 경우 성별, 나이대를 공개하는 기사가 많지 않아 성별, 나이대에 대해 분석할 것이 없었다.

# 호감순이 존재하는 경우
## 정치 기사인 경우
정치 기사의 경우 댓글 당 좋아요의 수가 성별과 연령 분포에 따라 다른 경향이 존재했다.
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/51cc7965-efd6-45d3-86a5-e3e243ac4482"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/c723b33d-a9a3-455a-a7ff-fad3a025da7d"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/95170f53-4e55-42c5-9792-a3ad22fa2f30"/>

댓글 당 좋아요 수 비율이 1.5 이하인 경우, 60의 비율이 높았으며, 여성의 비율이 20% 미만이다.
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/c1167b31-e468-4a10-8831-f0e72b17fda3"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/9cf3abbc-37e6-48ee-bea0-9d16cc39f80a"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/7ef4abd6-7bb7-42b3-8327-f53b6b58b5df"/>

반면에 댓글 당 좋아요 수 비율이 2 이상인 경우, 40이 50, 60보다 비율이 높았으며, 여성의 비율이 20% 이상이다.

<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/28f67aa5-ef69-4c98-ac99-40b4fdd5fe56"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/5d34f570-0d69-4d86-a5a3-8fd2d9000ac6"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/72bdb3e8-319a-45ee-b162-7f01d86dd856"/>

위의 경우 좋아요 수 비율이 2 이상이며, 여성의 비율은 20% 미만이고 50의 비율이 가장 높았다.

**위 결과에서 정치 기사의 경우 40, 50이 60에 비해 상대적으로 좋아요를 누르는 경우가 많고 여성 비율은 주로 40이며 좋아요 수에는 미미한 영향을 미쳤을 것이라 추정된다.**

번외로 좋아요 비율이 높을 수록 댓글 순위의 변동이 전자에 비해 심했는데, 좋아요를 누르는 일이 더 많기 때문이라고 생각한다.
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/d1d95534-2253-4f3f-9188-f47f4e77fafb"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/78f4cfcb-af36-4e86-ba49-752fc98ca49e"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/59074c1e-cab5-4f6f-af51-d049691cf41a"/>
## 정치 기사가 아닌 경우
단순한 사실 보고가 아닌 인간이 분노하는 기사의 경우 좋아요의 수가 더 높았다. 이와 같이 판단한 근거는 아래와 같이

<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/cddfca29-8c1d-4071-8c1e-f3ca6ed58adb"/>

분노할 만한 사건의 경우 전체 댓글 당 좋아요의 비율이 최소 2이상이 나왔기 때문이다. 정치 기사의 경우 댓글 당 좋아요의 비율이 주로 2 이하인 것을 감안하면 좋아요를 더 많은 사람이 누르는 것을 확인할 수 있다.
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/55b5fed3-d2fb-48fd-a7e7-69a85e069614"/>

상위 10개의 댓글의 위치는 거의 변하지 않았다.

<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/02670e1b-227d-49ac-907e-88cd88aac0bb"/>

또한 여성 비율이 30% 가까이 가거나, 30%가 넘는 경우가 많았다.
# 수집 시간
## 수집 시간이 9시 ~ 13시인 경우
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/0a5c647d-d3ec-44cf-9a0c-45cbc03c906b"/>

40대의 댓글 비율은 9시 ~ 12시까지는 거의 동일하며 12시부터 비율이 빠르게 증가하였다. 이는 회사의 점심 시간과 연관이 있어보인다.
수집 시간과 상관 없이 좋아요 수와 좋아요 비율은 기사마다 다양했기에 좋아요와의 연관성은 찾지 못했다.
