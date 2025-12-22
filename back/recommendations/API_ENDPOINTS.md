# Recommendations API 엔드포인트 변경사항

## 변경 날짜
2025-12-22

## 변경 사유
백엔드 리팩토링: URL 관리를 각 앱의 urls.py로 위임

## 변경된 엔드포인트

### 1. 사용자 로그 API

**변경 전:**
- `GET /api/recommendations/log/`
- `POST /api/recommendations/log/`
- `GET /api/recommendations/log/{id}/`
- `PUT /api/recommendations/log/{id}/`
- `DELETE /api/recommendations/log/{id}/`

**변경 후:**
- `GET /api/recommendations/log/`
- `POST /api/recommendations/log/`
- `GET /api/recommendations/log/{id}/`
- `PUT /api/recommendations/log/{id}/`
- `DELETE /api/recommendations/log/{id}/`

**결과:** 경로 변경 없음 ✅

---

### 2. 추천 시스템 API

**변경 전:**
- `GET /api/recommendations/`
- `POST /api/recommendations/refresh/`

**변경 후:**
- `GET /api/recommendations/`
- `POST /api/recommendations/refresh/`

**결과:** 경로 변경 없음 ✅

---

## 백엔드 구조 변경사항

### 파일 구조
```
recommendations/
├── views/
│   ├── __init__.py
│   └── api_views.py          # UserLogViewSet, RecommendationViewSet
├── services/
│   ├── __init__.py
│   └── engine.py              # RecommendationEngine (비즈니스 로직)
├── urls.py                    # 신규 생성 - 라우터 관리
├── models.py
├── serializers.py
└── ...
```

### Import 경로 변경
- `from recommendations.api_views import ...` → `from recommendations.views.api_views import ...`
- `from recommendations.engine import ...` → `from recommendations.services.engine import ...`

### URL 관리 변경
- 기존: `mypjt/urls.py`에서 모든 라우터 관리
- 변경: `recommendations/urls.py`에서 자체 라우터 관리
- `mypjt/urls.py`에서는 `path('api/recommendations/', include('recommendations.urls'))` 사용

---

## 프론트엔드 영향

**변경 필요 없음!**

모든 API 엔드포인트 경로가 동일하게 유지되므로 프론트엔드 코드 수정이 필요하지 않습니다.

---

## 전체 API 엔드포인트 목록

### 사용자 로그 (UserLog)
| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| GET | `/api/recommendations/log/` | 본인의 로그 목록 조회 | 로그인 필요 |
| POST | `/api/recommendations/log/` | 로그 저장 (view, like, search) | 로그인 필요 |
| GET | `/api/recommendations/log/{id}/` | 특정 로그 조회 | 로그인 필요 |
| PUT | `/api/recommendations/log/{id}/` | 로그 수정 | 로그인 필요 |
| DELETE | `/api/recommendations/log/{id}/` | 로그 삭제 | 로그인 필요 |

### 추천 시스템 (Recommendation)
| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| GET | `/api/recommendations/` | 추천 목록 조회 (캐시 활용) | 로그인 필요 |
| POST | `/api/recommendations/refresh/` | 추천 캐시 강제 갱신 | 로그인 필요 |

---

## 쿼리 파라미터

### GET `/api/recommendations/`
- `top_n` (선택): 추천 개수 (기본값: 10)
  - 예시: `/api/recommendations/?top_n=20`

### POST `/api/recommendations/refresh/`
- Body:
  ```json
  {
    "top_n": 10
  }
  ```

---

## 응답 형식

### GET `/api/recommendations/`
```json
{
  "recommendations": [
    {
      "mt20id": "PF123456",
      "prfnm": "공연 제목",
      "genrenm": "뮤지컬",
      "poster": "포스터 URL",
      "prfstate": "공연중",
      "prfpdfrom": "2025-01-01",
      "prfpdto": "2025-03-31",
      "fcltynm": "공연장명",
      "area": "서울특별시",
      "is_liked": true,
      "like_count": 42,
      "score": 0.85,
      "reason": "embedding",
      "reason_text": "✨ AI가 선택한 당신의 완벽한 공연!"
    }
  ],
  "cached": false,
  "updated_at": "2025-12-22T10:30:00Z"
}
```

### POST `/api/recommendations/log/`
```json
{
  "success": true,
  "message": "로그가 저장되었습니다.",
  "data": {
    "id": 123,
    "user": 1,
    "performance": "PF123456",
    "action_type": "view",
    "timestamp": "2025-12-22T10:30:00Z"
  }
}
```

---

## 참고사항

### 추천 알고리즘 (7가지 점수 함수)
1. **f1_click (20%)**: 클릭/관심 로그 기반 (Time Decay 적용)
2. **f2_preference (15%)**: 취향 매칭 (장르, 배우)
3. **f3_location (10%)**: 위치 근접성 (광역시/도 매칭)
4. **f4_popularity (15%)**: 대중성 (BoxOffice 랭킹)
5. **f5_recency (10%)**: 최신성 (공연 시작일 임박도)
6. **f6_collaborative (10%)**: 협업 필터링 (유사 사용자)
7. **f7_embedding (20%)**: 임베딩 유사도 (AI 벡터 매칭)

### 캐시 정책
- 캐시 유효 시간: **1시간**
- 로그 생성 시 캐시 자동 무효화
- `/refresh/` 엔드포인트로 강제 갱신 가능

### 추천 사유 메시지
- `click`: "👁️ 최근 {장르} 장르를 자주 보셨어요!"
- `preference`: "❤️ 취향 저격 공연이에요!"
- `location`: "🏠 {지역}에서 공연해요!"
- `popularity`: "🔥 지금 가장 핫한 공연이에요!"
- `recency`: "⏰ 곧 시작하는 공연이에요!"
- `collaborative`: "👥 비슷한 취향의 사람들이 좋아해요!"
- `embedding`: "✨ AI가 선택한 당신의 완벽한 공연!"
