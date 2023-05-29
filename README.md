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
## 정치 기사가 아닌 경우
단순한 사실 보고가 아닌 인간이 분노하는 기사의 경우 좋아요의 수가 더 높았다. 이와 같이 판단한 근거는 아래와 같이
--700피트 상공서 항공기 출입문 연 30대 '최근 실직 스트레스'--
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/cddfca29-8c1d-4071-8c1e-f3ca6ed58adb"/>

분노할 만한 사건의 경우 전체 댓글 당 좋아요의 비율이 최소 2이상이 나왔기 때문이다. 정치 댓글의 경우 좋아요의 비율이 1~2 사이인 것을 감안하면 좋아요를 더 많은 사람이 누르는 것을 확인할 수 있다.
# 수집 시간
## 수집 시간이 9시 ~ 13시인 경우
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/0a5c647d-d3ec-44cf-9a0c-45cbc03c906b"/>

40대의 댓글 비율은 9시 ~ 12시까지는 거의 동일하며 12시부터 비율이 빠르게 증가하였다. 이는 회사의 점심 시간과 연관이 있어보인다.
# 성별과 좋아요 수
여성의 경우 남성에 비해 댓글 비율이 적으며 정치 분야의 경우 비율 차이는 더 심하다. 정치 기사의 경우 남성의 댓글 비율이 대부분이 80% 이상이다.
여성과 남성의 비율이 상대적으로 적은 경우 좋아요를 누르는 비율이 감소하였다.
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/c8bc7986-c5e7-4f61-966c-0b5b806e1280"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/2909e485-9b9d-4fa1-aade-3479e3fca909"/>

위의 경우 여성의 비율이 30%가 넘어가며 이때 전체 댓글당 좋아요의 비율이 0.6을 넘지 못한다.
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/60a311f9-f41b-456a-9b05-08b6d19328e3"/>
<img width="80%" src="https://github.com/skybluelee/news_comments/assets/107929903/d0830d84-57d6-44a3-a408-245fb8fdb460"/>

반면 여성의 비율이 낮은 경우 좋아요의 비율이 2.5에 근사한 결과가 나왔다.
