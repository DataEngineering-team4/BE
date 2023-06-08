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

## 현재 시스템 구성

현재 시스템은 daphne을 systemd로 이용하는 asgi protocol을 nginx가 리버스 프록싱 해주고 있습니다. /chat의 경우 websocket으로 연결을 해주고, /그 외의 프로토콜의 경우는 알아서 http로 연결해줍니다.

/etc/nginx/sites-available/BE 가 nginx configuration 파일이며,
/etc/systemd/system/daphne.service가 daphne service 파일입니다.

## https SSL 위치

/etc/letsencrypt/live/www.det4.site/fullchain.pem
/etc/letsencrypt/live/www.det4.site/privkey.pem
