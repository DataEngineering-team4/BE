# Hello DET4

AZURE를 이용해서 배포했습니다.
현재 주소는 4.230.8.32:5000 입니다.
도매인을 det4.site로 걸어놓았고 포트가 5000이므로
**http://www.det4.site:5000** 으로 이용하셔도 됩니다.

현재 admin 주소는 **http://www.det4.site:5000/admin**이고, ID/PW 모두 **admin**입니다.

test는 pytest -s 하면 됩니다. 아마 코드는 잘 읽혀질 겁니다
core/utility.py에 가공하는 함수를 다 넣어놨습니다.

ssh는 전용 pem을 이용해야 합니다. (민준)한테 파일 있으니 요구하면 드리겠습니다.
ssh -i <private key path> shsf@4.230.8.32

배포하고 싶을 때는 다음과 같이 입력하시면 됩니다.
BE 폴더에서 pipenv shell 수행 후
nohup daphne -b 0.0.0.0 -p 5000 config.asgi:application

process 확인은 sudo lsof -i :5000

그리고 kill -9 <PID> 하시면 됩니다.
