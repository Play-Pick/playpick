# Gunicorn 서비스 시작 가이드

## EC2에서 실행할 명령어

```bash
# 1. back 디렉토리로 이동
cd ~/playpick/back

# 2. setup 스크립트에 실행 권한 부여
chmod +x setup-systemd.sh

# 3. systemd 서비스 설치 및 시작
./setup-systemd.sh
```

또는 수동으로 실행:

```bash
# systemd 서비스 파일 복사
sudo cp gunicorn.service /etc/systemd/system/

# systemd 데몬 리로드
sudo systemctl daemon-reload

# 부팅 시 자동 시작 활성화
sudo systemctl enable gunicorn

# 서비스 시작
sudo systemctl start gunicorn

# 서비스 상태 확인
sudo systemctl status gunicorn
```

## 서비스 관리 명령어

```bash
# 서비스 중지
sudo systemctl stop gunicorn

# 서비스 재시작
sudo systemctl restart gunicorn

# 서비스 상태 확인
sudo systemctl status gunicorn

# 로그 확인
sudo journalctl -u gunicorn -f
```

## 트러블슈팅

서비스가 시작되지 않으면:

```bash
# 상세 로그 확인
sudo journalctl -u gunicorn -n 50 --no-pager

# 설정 파일 확인
cat /etc/systemd/system/gunicorn.service

# 수동으로 gunicorn 실행해서 에러 확인
cd ~/playpick/back
source ~/.venv/bin/activate
gunicorn --workers 2 --timeout 120 --bind 0.0.0.0:8000 mypjt.wsgi:application
```
