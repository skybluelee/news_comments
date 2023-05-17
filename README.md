# news_comments

## Airflow Python Module Installation

#### 먼저 우분투의 소프트웨어 관리 툴인 apt-get을 업데이트하고 파이썬 3.0 pip을 설치한다.

원래는 apt-get update 이후에 python3-pip을 설치하면 되는데 pyopenssl 관련 충돌이 있어서 이를 먼저 해결하고 python3-pip를 설치

```
sudo apt-get update 
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip3 install pyopenssl --upgrade
sudo apt-get install -y python3-pip
```
