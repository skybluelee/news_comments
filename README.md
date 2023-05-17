# news_comments
# Airflow 2.5.1 Installation:

- 우분투 20.04에서 Airflow 2.5.1을 설치하는 방법에 대한 문서로 파이썬 3.8을 사용
- 앞서 별도로 공유된 ssh 로그인 문서를 참조하여 할당된 EC2 서버로 로그인 (이 때 ubuntu 계정을 사용함).
- VS Code에서 바로 접근하는 방법도 있으며 이 역시 별도 문서를 제공할 예정

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
