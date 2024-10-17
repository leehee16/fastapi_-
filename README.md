# fastapi_실습
**fastapi실습_2024년 10월 17일 목요일**



# fastapi mypjt 실습
## python 가상환경 만들기
```
# 파이썬 가상환경
python -m venv fa_venv
# 콘다 가상환경
conda create -n faenv_py310 python=3.10
```
## 가상환경 활성화
```
[windows]
fa_venv/scripts/activate
[mac/linux]
source fa_venv/bin/activate
[anaconda]
conda activate faenv_py310
```
## 설치 라이브러리
<pre>
pip install fastapi "uvicorn[standard]"
pip install jinja2 python-multipart
pip install sqlalchemy
pip install pymysql cryptography
</pre>
## 서버 실행방법
```
uvicorn main:app --reload
또는
python app_start.py
```
## mypjt 클라이언트 확인
```
[앱 실행]
http://localhost:8000
[스웨거]
http://localhost:8000/docs
```








