# Vue3 + Django REST Framework 프로젝트 설정 가이드

## 프로젝트 구조

```
11-pjt/
├── back/                 # Django 백엔드
│   ├── accounts/         # 사용자 인증
│   ├── community/        # 커뮤니티 (리뷰, 댓글)
│   ├── performances/     # 공연 정보
│   └── mypjt/           # Django 프로젝트 설정
└── front/               # Vue3 프론트엔드
    ├── src/
    │   ├── api/         # API 클라이언트
    │   ├── components/  # Vue 컴포넌트
    │   ├── views/       # 페이지 뷰
    │   ├── stores/      # Pinia 스토어
    │   └── router/      # Vue Router
    └── package.json
```

## 백엔드 설정 (Django)

### 1. 가상환경 활성화
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. 필요한 패키지가 설치되어 있는지 확인
```bash
cd back
pip list
```

다음 패키지들이 설치되어 있어야 합니다:
- Django
- djangorestframework
- django-cors-headers
- djangorestframework-simplejwt
- django-filter
- python-dotenv

### 3. 데이터베이스 마이그레이션 (이미 완료됨)
```bash
python manage.py migrate
```

### 4. Django 서버 실행
```bash
python manage.py runserver
```

서버는 http://127.0.0.1:8000 에서 실행됩니다.

### API 엔드포인트

#### 공연 관련
- `GET /api/performances/` - 공연 목록
- `GET /api/performances/{id}/` - 공연 상세
- `GET /api/performances/genres/` - 장르 목록
- `GET /api/boxoffice/` - 박스오피스 랭킹
- `GET /api/boxoffice/latest_by_genre/` - 장르별 최신 랭킹

#### 커뮤니티 관련
- `GET /api/reviews/` - 리뷰 목록
- `POST /api/reviews/` - 리뷰 생성
- `GET /api/reviews/{id}/` - 리뷰 상세
- `PUT /api/reviews/{id}/` - 리뷰 수정
- `DELETE /api/reviews/{id}/` - 리뷰 삭제
- `POST /api/reviews/{id}/like/` - 리뷰 좋아요/취소

#### 댓글 관련
- `GET /api/comments/?review={review_id}` - 특정 리뷰의 댓글 목록
- `POST /api/comments/` - 댓글 생성
- `DELETE /api/comments/{id}/` - 댓글 삭제

#### 사용자 관련
- `GET /api/users/` - 사용자 목록
- `GET /api/users/{id}/` - 사용자 상세
- `GET /api/users/me/` - 현재 사용자 정보
- `POST /api/users/{id}/follow/` - 팔로우/언팔로우

## 프론트엔드 설정 (Vue3)

### 1. 의존성 설치
```bash
cd front
npm install
```

### 2. 개발 서버 실행
```bash
npm run dev
```

서버는 http://localhost:5173 에서 실행됩니다.

### 3. 빌드 (프로덕션)
```bash
npm run build
```

## 주요 기능

### CORS 설정
- Django 백엔드는 Vue 개발 서버(localhost:5173)로부터의 요청을 허용하도록 설정됨
- `withCredentials: true` 설정으로 인증 정보 포함

### Axios 인스턴스
- 기본 URL: `http://127.0.0.1:8000/api`
- 요청/응답 인터셉터 구현
- 토큰 기반 인증 지원

### Pinia 스토어
- `performanceStore`: 공연 정보 관리
- `communityStore`: 리뷰 및 댓글 관리
- `userStore`: 사용자 정보 및 인증 관리

### Vue Router
- `/` - 홈
- `/performances` - 공연 목록
- `/performances/:id` - 공연 상세
- `/community` - 커뮤니티

## 동시 실행 방법

### 터미널 1 (백엔드)
```bash
cd back
python manage.py runserver
```

### 터미널 2 (프론트엔드)
```bash
cd front
npm run dev
```

## 테스트 방법

1. Django 서버 실행 확인
   - http://127.0.0.1:8000/api/ 접속
   - DRF Browsable API 확인

2. Vue 앱 실행 확인
   - http://localhost:5173 접속
   - 네비게이션 메뉴 확인

3. API 연동 테스트
   - 공연 목록 페이지에서 데이터 로딩 확인
   - 브라우저 개발자 도구 Network 탭에서 API 요청 확인

## 개발 팁

### Django 관리자 계정 생성
```bash
cd back
python manage.py createsuperuser
```

### Vue DevTools
- Vue DevTools 브라우저 확장 프로그램 설치 권장
- Pinia 스토어 상태 확인 가능

### API 테스트
- Postman 또는 Thunder Client 사용 권장
- DRF Browsable API 직접 사용 가능

## 문제 해결

### CORS 오류
- Django settings.py의 CORS_ALLOWED_ORIGINS 확인
- 프론트엔드 포트 번호 일치 확인

### API 연결 실패
- Django 서버 실행 확인
- axios.js의 baseURL 확인
- 브라우저 콘솔에서 에러 메시지 확인

### 인증 문제
- 토큰 저장 확인 (localStorage)
- API 요청 헤더에 Authorization 포함 확인
