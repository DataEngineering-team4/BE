# Hello DET4

AZURE를 이용해서 배포했습니다.

test는 pytest -s 하면 됩니다. 아마 코드는 잘 읽혀질 겁니다

core/utility.py에 가공하는 함수를 다 넣어놨습니다.

현재 로그인은 구현이 안됐으며, rest framework 의존성은 설치해놓았습니다.

ssh는 전용 pem을 이용해야 합니다. (민준)한테 파일 있으니 요구하면 드리겠습니다.
ssh -i <private key path> shsf@4.230.8.32

daphne -b 0.0.0.0 -p 8000 config.asgi:application
