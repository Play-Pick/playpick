# 배포 준비 체크리스트 (Django + DRF + Vite + Vue3)

## 목적 및 배경

이 문서는 **Django + DRF 백엔드**와 **Vite + Vue3 프론트엔드**를 분리 배포하기 전 필수 사전 점검 사항을 정리한 안내서입니다.

- **프론트엔드**: Vercel 또는 Netlify
- **백엔드**: Render 또는 Railway
- **목표**: 초보자도 단계별로 따라 할 수 있도록 구체적인 예시와 설명 제공

---

## 1. 환경변수 템플릿

### 1-1. 프론트엔드 환경변수 (`front/.env.example`)

```env
# 백엔드 API 기본 URL
VITE_API_BASE_URL=https://your-backend-domain.com/api

# 카카오 맵 API 키
VITE_KAKAO_MAP_API_KEY=your_kakao_map_api_key_here
```

#### 변수 설명

| 변수명 | 의미 | 예시값 | 입력 위치 |
|--------|------|--------|-----------|
| `VITE_API_BASE_URL` | 백엔드 API 기본 URL (끝에 `/api` 포함) | `https://api.example.com/api` | Vercel/Netlify 환경변수 |
| `VITE_KAKAO_MAP_API_KEY` | 카카오 지도 API 키 | `abc123def456ghi789` | Vercel/Netlify 환경변수 |

#### 로컬 개발 시 `.env` 파일 예시

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_KAKAO_MAP_API_KEY=your_local_test_key
```

---

### 1-2. 백엔드 환경변수 (`back/.env.example`)

```env
# Django Secret Key (50자 이상 랜덤 문자열)
SECRET_KEY=your-secret-key-here-min-50-characters-random-string

# 디버그 모드 (배포 시 반드시 False)
DEBUG=False

# 허용 호스트 (콤마로 구분)
ALLOWED_HOSTS=your-backend-domain.com,localhost,127.0.0.1

# CSRF 신뢰 도메인 (프론트엔드 도메인 포함)
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com,https://your-preview-domain.vercel.app

# CORS 허용 도메인 (프론트엔드 도메인 포함)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-preview-domain.vercel.app

# 데이터베이스 URL (PostgreSQL)
DATABASE_URL=postgresql://username:password@hostname:5432/database_name

# PostgreSQL SSL 모드 (Render/Railway 필수)
DB_SSLMODE=require

# YouTube API 키
YOUTUBE_API_KEY=your_youtube_api_key_here

# YouTube 플레이리스트 ID
YOUTUBE_PLAYLIST_ID_MAIN=your_playlist_id_here

# KOPIS API 키
KOPIS_API=your_kopis_api_key_here

# Google Maps API 키
GMS_KEY=your_google_maps_api_key_here
```

#### 변수 설명

| 변수명 | 의미 | 예시값 | 입력 위치 |
|--------|------|--------|-----------|
| `SECRET_KEY` | Django 암호화 키 (50자 이상) | `django-insecure-abc123...xyz` | Render/Railway 환경변수 |
| `DEBUG` | 디버그 모드 (배포 시 False) | `False` | Render/Railway 환경변수 |
| `ALLOWED_HOSTS` | 요청 허용 호스트 (콤마 구분) | `api.example.com,localhost` | Render/Railway 환경변수 |
| `CSRF_TRUSTED_ORIGINS` | CSRF 신뢰 도메인 (https:// 포함) | `https://example.com,https://preview.vercel.app` | Render/Railway 환경변수 |
| `CORS_ALLOWED_ORIGINS` | CORS 허용 도메인 (https:// 포함) | `https://example.com,https://preview.vercel.app` | Render/Railway 환경변수 |
| `DATABASE_URL` | PostgreSQL 연결 URL | `postgresql://user:pass@host:5432/dbname` | Render/Railway에서 자동 생성 또는 수동 입력 |
| `DB_SSLMODE` | PostgreSQL SSL 모드 | `require` | Render/Railway 환경변수 |
| `YOUTUBE_API_KEY` | YouTube Data API v3 키 | `AIzaSyABC...XYZ` | Render/Railway 환경변수 |
| `YOUTUBE_PLAYLIST_ID_MAIN` | YouTube 플레이리스트 ID | `PLAbc123...xyz` | Render/Railway 환경변수 |
| `KOPIS_API` | 공연예술통합전산망 API 키 | `abc123def456` | Render/Railway 환경변수 |
| `GMS_KEY` | Google Maps API 키 | `AIzaSyDEF...ABC` | Render/Railway 환경변수 |

#### 로컬 개발 시 `.env` 파일 예시

```env
SECRET_KEY=django-insecure-local-development-key-123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
DATABASE_URL=sqlite:///db.sqlite3
DB_SSLMODE=
YOUTUBE_API_KEY=
YOUTUBE_PLAYLIST_ID_MAIN=
KOPIS_API=
GMS_KEY=
```

---

## 2. 프론트엔드 점검 (Vite + Vue3)

### 2-1. API 기본 URL 설정 확인

**파일**: `front/src/api/axios.js`

#### 체크 포인트

1. **환경변수 사용 확인**
   ```javascript
   const instance = axios.create({
     baseURL: import.meta.env.VITE_API_BASE_URL, // ✅ 환경변수 사용
     withCredentials: true, // ✅ 쿠키 포함
   })
   ```

2. **Refresh 토큰 요청도 동일한 baseURL 사용**
   ```javascript
   const response = await axios.post(
     `${import.meta.env.VITE_API_BASE_URL}/accounts/token/refresh/`, // ✅ 동일한 base URL
     {},
     { withCredentials: true }
   )
   ```

3. **withCredentials 유지**
   - 모든 axios 인스턴스에서 `withCredentials: true` 설정 확인
   - JWT 리프레시 토큰이 쿠키로 전송되므로 필수

### 2-2. 빌드 설정 확인

#### Vercel 설정 예시

**Build Command**:
```bash
npm ci && npm run build
```

**Output Directory**:
```
dist
```

**Install Command**:
```bash
npm ci
```

#### Netlify 설정 예시

**Build Command**:
```bash
npm ci && npm run build
```

**Publish Directory**:
```
dist
```

#### 로컬 빌드 테스트

```bash
cd front
npm ci
npm run build
```

빌드 성공 시 `dist/` 폴더 생성 확인

---

## 3. 백엔드 점검 (Django + DRF)

### 3-1. settings.py 필수 설정

#### 기본 설정 (환경변수 기반)

```python
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# 환경변수에서 가져오기 (배포 시 필수)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-dev-only')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

#### 데이터베이스 설정 (PostgreSQL + SQLite fallback)

```python
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',  # 로컬 개발 시 SQLite 사용
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# PostgreSQL SSL 설정 (Render/Railway)
if os.environ.get('DB_SSLMODE') == 'require':
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
```

#### 정적 파일 설정 (Whitenoise)

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise를 사용한 정적 파일 서빙
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

#### MIDDLEWARE 설정

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ SecurityMiddleware 바로 다음
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ✅ CommonMiddleware 앞
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### CORS/CSRF 설정 (프론트엔드 도메인 허용)

```python
# CORS 설정
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
).split(',')
CORS_ALLOW_CREDENTIALS = True

# CSRF 설정
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
).split(',')
```

#### 배포 환경 보안 설정

```python
# HTTPS/프록시 설정 (Render/Railway/Vercel)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SAMESITE = 'None'
```

### 3-2. 필수 패키지 설치

**파일**: `back/requirements.txt`

```txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
whitenoise==6.6.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

#### 설치 명령

```bash
cd back
pip install -r requirements.txt
```

### 3-3. Procfile 생성 (선택사항, Render/Railway는 Start Command 사용 가능)

**파일**: `back/Procfile`

```
web: gunicorn mypjt.wsgi:application --bind 0.0.0.0:$PORT
```

### 3-4. Gunicorn 실행 명령

**Start Command (Render/Railway)**:
```bash
gunicorn mypjt.wsgi:application --bind 0.0.0.0:$PORT
```

**로컬 테스트**:
```bash
cd back
gunicorn mypjt.wsgi:application --bind 127.0.0.1:8000
```

---

## 4. 배포 순서 체크리스트

### Step 1: 환경변수 설정

- [ ] `front/.env.example` 작성 완료
- [ ] `back/.env.example` 작성 완료
- [ ] Vercel/Netlify에 프론트엔드 환경변수 입력
  - `VITE_API_BASE_URL`
  - `VITE_KAKAO_MAP_API_KEY`
- [ ] Render/Railway에 백엔드 환경변수 입력
  - `SECRET_KEY` (50자 이상 랜덤)
  - `DEBUG=False`
  - `ALLOWED_HOSTS` (백엔드 도메인)
  - `CSRF_TRUSTED_ORIGINS` (프론트 도메인, https://)
  - `CORS_ALLOWED_ORIGINS` (프론트 도메인, https://)
  - `DATABASE_URL` (PostgreSQL)
  - `DB_SSLMODE=require`
  - API 키들 (YOUTUBE_API_KEY, KOPIS_API 등)

### Step 2: 백엔드 설정 점검

- [ ] `settings.py`에서 환경변수 기반 설정 확인
- [ ] `DATABASES`에 `dj_database_url.config` 사용
- [ ] `STATIC_ROOT` 및 Whitenoise 설정 완료
- [ ] `MIDDLEWARE`에 WhiteNoiseMiddleware 추가 (SecurityMiddleware 다음)
- [ ] `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` 설정
- [ ] 배포 시 `SameSite=None`, `SECURE_PROXY_SSL_HEADER` 설정
- [ ] `requirements.txt`에 필수 패키지 포함 확인
  - psycopg2-binary
  - dj-database-url
  - whitenoise
  - gunicorn

### Step 3: 프론트엔드 설정 점검

- [ ] `front/src/api/axios.js`에서 `VITE_API_BASE_URL` 사용 확인
- [ ] Refresh 토큰 요청도 동일한 baseURL 사용 확인
- [ ] `withCredentials: true` 설정 확인
- [ ] 빌드 커맨드: `npm ci && npm run build`
- [ ] 로컬 빌드 테스트 성공

### Step 4: 마이그레이션 및 정적 파일

- [ ] 로컬에서 마이그레이션 파일 생성 완료
  ```bash
  python manage.py makemigrations
  ```
- [ ] 배포 환경에서 마이그레이션 실행 (Release Command)
  ```bash
  python manage.py migrate
  ```
- [ ] 정적 파일 수집 (Release Command)
  ```bash
  python manage.py collectstatic --noinput
  ```

### Step 5: 배포

#### 백엔드 배포 (Render/Railway)

**Build Command** (선택사항):
```bash
pip install -r requirements.txt
```

**Release Command** (마이그레이션 + 정적 파일):
```bash
python manage.py migrate && python manage.py collectstatic --noinput
```

**Start Command**:
```bash
gunicorn mypjt.wsgi:application --bind 0.0.0.0:$PORT
```

#### 프론트엔드 배포 (Vercel/Netlify)

**Build Command**:
```bash
npm ci && npm run build
```

**Output Directory**:
```
dist
```

### Step 6: 배포 후 헬스체크

- [ ] 백엔드 API 응답 확인
  - GET `https://your-backend.com/api/` (또는 헬스체크 엔드포인트)
- [ ] 프론트엔드 로딩 확인
  - `https://your-frontend.com/`
- [ ] CORS 테스트
  - 프론트에서 백엔드 API 호출 성공 확인
- [ ] 로그인/회원가입 테스트
  - JWT 토큰 발급 및 리프레시 동작 확인
- [ ] 정적 파일 로딩 확인
  - Django Admin CSS/JS 정상 로딩 확인

---

## 5. 배포 플랫폼별 입력값 정리

### Vercel (프론트엔드)

**Environment Variables**:
```
VITE_API_BASE_URL=https://your-backend.onrender.com/api
VITE_KAKAO_MAP_API_KEY=your_kakao_key
```

**Build Settings**:
- Framework Preset: `Vite`
- Build Command: `npm ci && npm run build`
- Output Directory: `dist`
- Install Command: `npm ci`

### Netlify (프론트엔드)

**Environment Variables**:
```
VITE_API_BASE_URL=https://your-backend.onrender.com/api
VITE_KAKAO_MAP_API_KEY=your_kakao_key
```

**Build Settings**:
- Build Command: `npm ci && npm run build`
- Publish Directory: `dist`

### Render (백엔드)

**Environment Variables**:
```
SECRET_KEY=your-50-character-random-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend-preview.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend-preview.vercel.app
DATABASE_URL=postgresql://...  (Render가 자동 생성)
DB_SSLMODE=require
YOUTUBE_API_KEY=your_youtube_key
YOUTUBE_PLAYLIST_ID_MAIN=your_playlist_id
KOPIS_API=your_kopis_key
GMS_KEY=your_google_maps_key
```

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
gunicorn mypjt.wsgi:application --bind 0.0.0.0:$PORT
```

**Health Check Path** (선택):
```
/api/health
```

### Railway (백엔드)

**Environment Variables**: Render와 동일

**Build Command**: (자동 감지)
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
gunicorn mypjt.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 6. 문제 해결 팁

### 6-1. CORS/CSRF 403 에러

**증상**:
```
Access to XMLHttpRequest has been blocked by CORS policy
```
또는
```
CSRF token missing or incorrect
```

**해결 방법**:
1. **도메인 확인**
   - 프론트엔드 도메인이 `CORS_ALLOWED_ORIGINS`와 `CSRF_TRUSTED_ORIGINS`에 정확히 입력되었는지 확인
   - `https://` 프로토콜 포함 확인
   - 끝에 `/` 없이 입력 (예: `https://example.com` ⭕, `https://example.com/` ❌)

2. **SameSite/HTTPS 확인**
   - 배포 환경에서 `CSRF_COOKIE_SAMESITE = 'None'` 설정 확인
   - `SESSION_COOKIE_SAMESITE = 'None'` 설정 확인
   - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` 설정 확인

3. **CORS Credentials 확인**
   - `CORS_ALLOW_CREDENTIALS = True` 설정 확인
   - 프론트엔드 axios에서 `withCredentials: true` 설정 확인

### 6-2. 정적 파일 404 에러

**증상**:
```
GET /static/admin/css/base.css 404 Not Found
```

**해결 방법**:
1. **collectstatic 실행 확인**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **STATIC_ROOT 설정 확인**
   ```python
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

3. **Whitenoise 설정 확인**
   - `MIDDLEWARE`에 `whitenoise.middleware.WhiteNoiseMiddleware` 포함 확인
   - `STORAGES`에 `whitenoise.storage.CompressedManifestStaticFilesStorage` 설정 확인

4. **배포 플랫폼 Release Command 확인**
   ```bash
   python manage.py collectstatic --noinput
   ```

### 6-3. 데이터베이스 연결 오류

**증상**:
```
django.db.utils.OperationalError: connection to server failed
```

**해결 방법**:
1. **DATABASE_URL 형식 확인**
   ```
   postgresql://username:password@hostname:5432/database_name
   ```
   - 사용자명, 비밀번호, 호스트, 포트, 데이터베이스 이름 정확한지 확인

2. **SSL 모드 설정 확인**
   ```python
   if os.environ.get('DB_SSLMODE') == 'require':
       DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
   ```

3. **Render/Railway PostgreSQL 생성 확인**
   - 대시보드에서 PostgreSQL 인스턴스 생성
   - `DATABASE_URL` 환경변수 자동 설정 확인

4. **방화벽/네트워크 확인**
   - PostgreSQL 인스턴스가 외부 접속 허용하는지 확인
   - IP 화이트리스트 설정 확인

### 6-4. JWT 리프레시 실패

**증상**:
```
POST /api/accounts/token/refresh/ 404 Not Found
```
또는
```
POST http://localhost:8000/api/accounts/token/refresh/ (프로덕션에서 localhost 호출)
```

**해결 방법**:
1. **VITE_API_BASE_URL 확인**
   - Vercel/Netlify 환경변수에 정확히 입력되었는지 확인
   - 예: `https://your-backend.onrender.com/api`

2. **Refresh 요청 baseURL 확인**
   ```javascript
   // ❌ 하드코딩된 URL
   await axios.post('http://localhost:8000/api/accounts/token/refresh/', ...)

   // ✅ 환경변수 사용
   await axios.post(`${import.meta.env.VITE_API_BASE_URL}/accounts/token/refresh/`, ...)
   ```

3. **쿠키 전송 확인**
   - `withCredentials: true` 설정 확인
   - 브라우저 개발자 도구에서 Network 탭 > Cookies 확인

### 6-5. 빌드 실패

**증상**:
```
npm ERR! Cannot find module 'vite'
```

**해결 방법**:
1. **의존성 설치 확인**
   ```bash
   npm ci  # package-lock.json 기반 정확한 버전 설치
   ```

2. **node_modules 재설치**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Node 버전 확인**
   - Vite는 Node 18+ 권장
   - 배포 플랫폼에서 Node 버전 설정 확인

### 6-6. 환경변수가 적용되지 않음

**증상**:
```
console.log(import.meta.env.VITE_API_BASE_URL) // undefined
```

**해결 방법**:
1. **변수명 확인**
   - Vite 환경변수는 반드시 `VITE_` 접두사 필요
   - 예: `VITE_API_BASE_URL` ⭕, `API_BASE_URL` ❌

2. **빌드 시점에 주입되므로 재빌드 필요**
   - 환경변수 변경 후 반드시 재배포

3. **Vercel/Netlify 환경변수 재확인**
   - 대시보드에서 정확히 입력되었는지 확인
   - Preview/Production 환경 구분 확인

---

## 7. 최종 점검 체크리스트

배포 전 아래 항목을 모두 확인하세요:

### 백엔드 (Django + DRF)
- [ ] `SECRET_KEY`를 환경변수로 관리, 배포 시 50자 이상 랜덤 값 사용
- [ ] `DEBUG=False` 설정
- [ ] `ALLOWED_HOSTS`에 백엔드 도메인 추가
- [ ] `CSRF_TRUSTED_ORIGINS`에 프론트 도메인 추가 (https://)
- [ ] `CORS_ALLOWED_ORIGINS`에 프론트 도메인 추가 (https://)
- [ ] `CORS_ALLOW_CREDENTIALS=True` 설정
- [ ] `DATABASE_URL`을 PostgreSQL로 설정
- [ ] `DB_SSLMODE=require` 설정 (Render/Railway)
- [ ] `STATIC_ROOT` 및 Whitenoise 설정 완료
- [ ] `MIDDLEWARE`에 WhiteNoiseMiddleware 추가
- [ ] `requirements.txt`에 필수 패키지 포함
- [ ] Start Command: `gunicorn mypjt.wsgi:application --bind 0.0.0.0:$PORT`
- [ ] Release Command: `python manage.py migrate && python manage.py collectstatic --noinput`

### 프론트엔드 (Vite + Vue3)
- [ ] `VITE_API_BASE_URL`을 환경변수로 설정
- [ ] `front/src/api/axios.js`에서 환경변수 사용
- [ ] `withCredentials: true` 설정
- [ ] Refresh 토큰 요청도 동일한 baseURL 사용
- [ ] Build Command: `npm ci && npm run build`
- [ ] Output Directory: `dist`
- [ ] 로컬 빌드 테스트 성공

### 배포 후 테스트
- [ ] 백엔드 헬스체크 성공
- [ ] 프론트엔드 페이지 로딩 성공
- [ ] 로그인/회원가입 동작 확인
- [ ] JWT 토큰 발급 및 리프레시 동작 확인
- [ ] API 호출 시 CORS 에러 없음
- [ ] Django Admin 정적 파일 정상 로딩

---

## 8. 참고 자료

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Whitenoise Documentation](http://whitenoise.evans.io/en/stable/)
- [dj-database-url Documentation](https://github.com/jazzband/dj-database-url)
- [Render Django Deploy Guide](https://render.com/docs/deploy-django)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

---

**작성일**: 2025-12-23
**프로젝트**: SSAFY Final Project
**스택**: Django 4.2 + DRF + Vite + Vue3
