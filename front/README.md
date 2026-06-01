# 공연 정보 플랫폼 - Frontend

Vue 3 기반의 공연 정보 및 커뮤니티 플랫폼 프론트엔드입니다.

## 개요

사용자 맞춤형 공연 추천, AI 기반 검색, 박스오피스 랭킹, 커뮤니티 리뷰 시스템을 제공하는 SPA(Single Page Application)입니다.

## 주요 기능

- **AI 검색**: 자연어 기반 공연 검색 및 AI 추천
- **박스오피스 랭킹**: 장르별 주간 랭킹 및 하이라이트 캐러셀
- **공연 정보**: 상세 정보, Kakao Map 연동, YouTube 영상
- **커뮤니티**: 리뷰 작성, 댓글, 좋아요, 별점 평가
- **개인화**: Tinder 스타일 온보딩, 맞춤 추천, 찜/관람함
- **다크모드**: 전역 테마 토글

## 기술 스택

| 분류 | 기술 | 버전 |
|------|------|------|
| Framework | Vue | ^3.5.25 |
| Build Tool | Vite | ^7.2.4 |
| State Management | Pinia | ^3.0.4 |
| Routing | Vue Router | ^4.6.3 |
| HTTP Client | Axios | ^1.13.2 |
| Styling | Tailwind CSS | ^3.4.0 |

## 프로젝트 구조

```
front/
├── src/
│   ├── api/              # API 통신 모듈
│   ├── components/       # 재사용 컴포넌트
│   │   ├── AISearch/
│   │   ├── BoxOffice/
│   │   ├── Common/
│   │   ├── Community/
│   │   ├── Performance/
│   │   ├── PerformanceDetail/
│   │   ├── Recommendation/
│   │   ├── User/
│   │   └── YouTube/
│   ├── composables/      # Composition API 로직
│   ├── stores/           # Pinia 상태 관리
│   ├── views/            # 페이지 컴포넌트
│   ├── router/           # 라우팅 설정
│   └── assets/           # 정적 파일
├── public/               # 공개 리소스
└── dist/                 # 빌드 결과물
```

## 설치 및 실행

### 사전 요구사항

- Node.js: ^20.19.0 또는 >=22.12.0
- npm (Node.js와 함께 설치됨)

### 설치

```bash
# 의존성 설치
npm install

# 환경 변수 설정 (선택사항)
cp .env.production .env
# .env 파일에 Kakao Map API 키 입력
```

### 개발 서버 실행

```bash
npm run dev
```

개발 서버: http://localhost:5173

### 프로덕션 빌드

```bash
# 빌드
npm run build

# 빌드 미리보기
npm run preview
```

## 주요 특징

### 1. Vue 3 Composition API
- `<script setup>` 문법으로 간결한 코드
- Composables 패턴으로 로직 재사용
- 반응형 상태 관리

### 2. JWT 인증
- Access/Refresh Token 자동 관리
- Axios 인터셉터로 토큰 갱신
- 로그인 상태 유지

### 3. 상태 관리 (Pinia)
- 모듈화된 스토어 구조
- localStorage 동기화
- 낙관적 업데이트

### 4. 컴포넌트 설계
- 단일 책임 원칙
- Props Down, Events Up
- 재사용 가능한 구조

## 개발 가이드

자세한 개발 가이드는 [프론트엔드 개요 문서](../docs/final-submission/01-프로젝트-개요/03-프론트엔드-개요.md)를 참고하세요.

## 문제 해결

### CORS 에러
백엔드 서버의 CORS 설정 및 `src/api/axios.js`의 baseURL을 확인하세요.

### 토큰 만료
Refresh Token이 만료되었을 경우 재로그인이 필요합니다.

### Kakao Map 로드 실패
`.env` 파일에 올바른 API 키가 설정되어 있는지 확인하세요.

## 라이센스

본 프로젝트는 교육 목적으로 제작되었습니다.
