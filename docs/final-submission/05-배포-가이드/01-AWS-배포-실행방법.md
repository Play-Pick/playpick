# AWS 배포 서버 실행 방법

## 서버 정보
- **백엔드 IP**: 13.239.105.171
- **프론트엔드 IP**: 13.210.134.120
- **백엔드 포트**: 8000
- **프론트엔드 포트**: 80

---

## 1. 백엔드 서버 실행

### SSH 접속
```bash
ssh ubuntu@13.239.105.171
```

### 기본 서버 시작
```bash
cd ~/playpick/back
python manage.py runserver 0.0.0.0:8000
```

### 백그라운드 실행 (Screen 권장)
```bash
# Screen 세션 생성
screen -S backend

# 서버 실행
cd ~/playpick/back
python manage.py runserver 0.0.0.0:8000

# Ctrl+A, D 로 백그라운드로 전환
```

### Git Pull 후 재시작
```bash
cd ~/playpick
git pull
cd back
python manage.py runserver 0.0.0.0:8000
```

### 서버 상태 확인
```bash
# 8000번 포트 확인
sudo lsof -i :8000

# 프로세스 확인
ps aux | grep runserver
```

### 서버 중지
```bash
# 포그라운드 실행 시
Ctrl+C

# 백그라운드 실행 시
pkill -f runserver

# Screen 세션에서 실행 중일 때
screen -r backend  # 세션 재접속
Ctrl+C             # 서버 중지
exit               # 세션 종료
```

---

## 2. 프론트엔드 서버 실행

### SSH 접속
```bash
ssh ubuntu@13.210.134.120
```

### 프로덕션 빌드 + 실행
```bash
cd ~/playpick/front
npm run build
npm run preview -- --host 0.0.0.0 --port 80
```

### 백그라운드 실행 (Screen 권장)
```bash
# Screen 세션 생성
screen -S frontend

# 빌드 및 서버 실행
cd ~/playpick/front
npm run build
npm run preview -- --host 0.0.0.0 --port 80

# Ctrl+A, D 로 백그라운드로 전환
```

### Git Pull 후 재빌드 + 재시작
```bash
cd ~/playpick
git pull
cd front
npm run build
npm run preview -- --host 0.0.0.0 --port 80
```

### 서버 상태 확인
```bash
# 80번 포트 확인
sudo lsof -i :80

# 프로세스 확인
ps aux | grep vite
```

### 서버 중지
```bash
# 포그라운드 실행 시
Ctrl+C

# 백그라운드 실행 시
pkill -f "vite preview"

# Screen 세션에서 실행 중일 때
screen -r frontend  # 세션 재접속
Ctrl+C              # 서버 중지
exit                # 세션 종료
```

---

## 3. 데이터베이스 초기 설정

### 마이그레이션
```bash
cd ~/playpick/back
python manage.py migrate
```

### Fixtures 데이터 로드
```bash
cd ~/playpick/back

# 공연 데이터
python manage.py loaddata fixtures/performances_performance.json
python manage.py loaddata fixtures/performances_performancedetail.json
python manage.py loaddata fixtures/performances_performanceimage.json
python manage.py loaddata fixtures/performances_boxofficeranking.json

# 사용자 및 커뮤니티 데이터
python manage.py loaddata fixtures/accounts_user.json
python manage.py loaddata fixtures/community_article.json
python manage.py loaddata fixtures/community_comment.json
```

### 임베딩 데이터 로드
```bash
cd ~/playpick/back
python manage.py export_embeddings --import embeddings/performance_embeddings.npz
```

### 전체 데이터 로드 (한 번에)
```bash
cd ~/playpick/back && \
python manage.py loaddata fixtures/accounts_user.json && \
python manage.py loaddata fixtures/performances_performance.json && \
python manage.py loaddata fixtures/performances_performancedetail.json && \
python manage.py loaddata fixtures/performances_performanceimage.json && \
python manage.py loaddata fixtures/performances_boxofficeranking.json && \
python manage.py loaddata fixtures/community_article.json && \
python manage.py loaddata fixtures/community_comment.json && \
echo "✅ 모든 fixtures 로드 완료!"
```

---

## 4. Screen 세션 관리

### Screen 기본 명령어
```bash
# 모든 세션 보기
screen -ls

# 세션 생성
screen -S [세션명]

# 세션에 재접속
screen -r [세션명]

# 세션에서 나가기 (백그라운드로)
Ctrl+A, D

# 세션 종료 (세션 안에서)
exit

# 세션 강제 종료
screen -X -S [세션명] quit
```

### 실전 예제
```bash
# 백엔드 세션 만들기
screen -S backend
cd ~/playpick/back
python manage.py runserver 0.0.0.0:8000
# Ctrl+A, D

# 프론트엔드 세션 만들기
screen -S frontend
cd ~/playpick/front
npm run build
npm run preview -- --host 0.0.0.0 --port 80
# Ctrl+A, D

# 세션 목록 확인
screen -ls

# 백엔드 세션 다시 보기
screen -r backend

# 프론트엔드 세션 다시 보기
screen -r frontend
```

---

## 5. 전체 배포 프로세스

### 처음 배포 시
```bash
# 1. 백엔드 서버
ssh ubuntu@13.239.105.171
cd ~/playpick
git clone [레포지토리 URL] .
cd back
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
# 데이터 로드 (위의 3번 참고)
screen -S backend
python manage.py runserver 0.0.0.0:8000
# Ctrl+A, D

# 2. 프론트엔드 서버
ssh ubuntu@13.210.134.120
cd ~/playpick
git clone [레포지토리 URL] .
cd front
npm install
npm run build
screen -S frontend
npm run preview -- --host 0.0.0.0 --port 80
# Ctrl+A, D
```

### 코드 업데이트 시
```bash
# 백엔드
ssh ubuntu@13.239.105.171
screen -r backend
# Ctrl+C로 서버 중지
cd ~/playpick
git pull
cd back
python manage.py migrate  # 마이그레이션이 있는 경우
python manage.py runserver 0.0.0.0:8000
# Ctrl+A, D

# 프론트엔드
ssh ubuntu@13.210.134.120
screen -r frontend
# Ctrl+C로 서버 중지
cd ~/playpick
git pull
cd front
npm run build
npm run preview -- --host 0.0.0.0 --port 80
# Ctrl+A, D
```

---

## 6. 트러블슈팅

### 백엔드 서버 접속 안 됨
```bash
# 1. 서버 실행 확인
sudo lsof -i :8000

# 2. AWS 보안 그룹 확인
# - 8000번 포트가 열려있는지 확인
# - 인바운드 규칙에 Custom TCP, Port 8000 추가

# 3. 서버가 0.0.0.0으로 바인딩되었는지 확인
ps aux | grep runserver
# 127.0.0.1이 아닌 0.0.0.0:8000이어야 함
```

### 프론트엔드 서버 접속 안 됨
```bash
# 1. 서버 실행 확인
sudo lsof -i :80

# 2. AWS 보안 그룹 확인
# - 80번 포트가 열려있는지 확인

# 3. 80번 포트 권한 문제
# sudo 없이 80번 포트 사용하려면:
sudo setcap 'cap_net_bind_service=+ep' $(which node)
```

### CORS 에러
```bash
# backend settings.py 확인
# CORS_ALLOWED_ORIGINS에 프론트엔드 IP가 있는지 확인
# - "http://13.210.134.120"
# - "http://13.210.134.120:80"
```

### .env 파일 적용 안 됨
```bash
# 백엔드
cd ~/playpick/back
cat .env  # 파일 내용 확인
# 서버 재시작 필요

# 프론트엔드
cd ~/playpick/front
cat .env.production  # 파일 내용 확인
npm run build  # 재빌드 필요
```

---

## 7. 유용한 명령어

### 로그 확인 (nohup 사용 시)
```bash
# 백엔드
tail -f ~/playpick/back/server.log

# 프론트엔드
tail -f ~/playpick/front/server.log
```

### 환경 변수 확인
```bash
# 백엔드
cd ~/playpick/back
cat .env

# 프론트엔드
cd ~/playpick/front
cat .env.production
```

### 데이터베이스 초기화
```bash
cd ~/playpick/back
rm db.sqlite3
python manage.py migrate
# 데이터 재로드 (위의 3번 참고)
```

---

## 8. 접속 URL

- **프론트엔드**: http://13.210.134.120
- **백엔드 API**: http://13.239.105.171:8000/api/
- **백엔드 Admin**: http://13.239.105.171:8000/admin/
