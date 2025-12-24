# 공연 정보 플랫폼 - Backend

Django REST Framework 기반의 공연 정보 플랫폼 백엔드 API 서버입니다.

## 개요

KOPIS API 연동, OpenAI 임베딩 기반 AI 검색, 하이브리드 추천 시스템, Tinder 스타일 온보딩을 제공하는 RESTful API 서버입니다.

## 주요 기능

- **RESTful API**: ViewSet 기반 체계적인 엔드포인트 구성
- **JWT 인증**: Access/Refresh Token 자동 갱신
- **하이브리드 추천**: 7개 점수 함수 조합 추천 엔진
- **AI 검색**: OpenAI 임베딩 기반 의미 검색
- **KOPIS 연동**: 공연 데이터 자동 수집
- **온보딩 시스템**: 사용자 선호도 벡터 생성
- **YouTube 연동**: 공연 관련 영상 추천

## 기술 스택

| 분류 | 기술 | 버전 |
|------|------|------|
| Framework | Django | 5.2.8 |
| API | Django REST Framework | 3.16.1 |
| Database | SQLite | 3.x |
| Authentication | djangorestframework-simplejwt | 5.5.1 |
| CORS | django-cors-headers | 4.9.0 |
| AI/ML | openai | 2.14.0 |
| | scikit-learn | 1.8.0 |
| | numpy | 2.3.5 |
| Utilities | python-dotenv | 1.2.1 |
| | requests | 2.32.5 |

## 프로젝트 구조

```
back/
├── accounts/         # 사용자 인증 및 온보딩
├── performances/     # 공연 정보 관리
├── community/        # 커뮤니티 (리뷰, 댓글)
├── recommendations/  # 추천 시스템
├── mypjt/           # Django 설정
├── tests/           # 테스트 스크립트
├── fixtures/        # 초기 데이터
├── embeddings/      # 임베딩 벡터
├── logs/            # 로그 파일
└── db.sqlite3       # 데이터베이스
```

## 설치 및 실행

### 사전 요구사항

- Python 3.8 이상
- pip (최신 버전)

### 설치

```bash
# 가상환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env_ .env
# .env 파일에 API 키 입력
```

### 데이터베이스 설정

```bash
# 마이그레이션
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

### 개발 서버 실행

```bash
python manage.py runserver
```

서버: http://127.0.0.1:8000

## 주요 API 엔드포인트

### 인증
- `POST /api/accounts/register/` - 회원가입
- `POST /api/accounts/token/` - 로그인 (JWT 발급)
- `POST /api/accounts/token/refresh/` - 토큰 갱신

### 공연
- `GET /api/performances/` - 공연 목록
- `GET /api/performances/<id>/` - 공연 상세
- `POST /api/performances/ai-search/` - AI 의미 검색
- `GET /api/performances/boxoffice-genre/` - 장르별 박스오피스
- `POST /api/performances/<id>/like/` - 찜하기

### 커뮤니티
- `GET /api/community/articles/` - 게시글 목록
- `POST /api/community/articles/` - 게시글 작성
- `GET /api/community/articles/best-reviews/` - 베스트 리뷰

### 추천
- `GET /api/recommendations/` - 개인화 추천

### 온보딩
- `GET /api/accounts/onboarding/candidates/` - 후보 공연
- `POST /api/accounts/onboarding/signals/` - 선호도 저장
- `POST /api/accounts/onboarding/complete/` - 온보딩 완료

## 관리자 커맨드

```bash
# 공연 데이터 수집
python manage.py collect_performances --start-date 2024-01-01 --end-date 2024-12-31

# 공연 상세 정보 수집
python manage.py collect_performance_detail

# 박스오피스 수집
python manage.py collect_boxoffice --date 20241223 --period week

# 임베딩 생성 (AI 검색용)
python manage.py generate_embeddings --batch-size 10
```

## 환경 변수 (.env)

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# KOPIS API
KOPIS_API=your-kopis-api-key

# OpenAI (GMS 프록시)
GMS_KEY=your-gms-key

# YouTube
YOUTUBE_API_KEY=your-youtube-api-key
YOUTUBE_PLAYLIST_ID_MAIN=your-playlist-id
```

## 개발 가이드

자세한 개발 가이드는 [백엔드 개요 문서](../docs/final-submission/01-프로젝트-개요/02-백엔드-개요.md)를 참고하세요.

## 주요 모델

- **User**: 사용자 정보 및 인증
- **Performance**: 공연 정보
- **PerformanceEmbedding**: AI 검색용 임베딩 벡터
- **BoxOfficeRanking**: 박스오피스 랭킹
- **Article**: 커뮤니티 게시글
- **UserPreference**: 사용자 선호도 벡터

## 라이센스

본 프로젝트는 교육 목적으로 제작되었습니다.
