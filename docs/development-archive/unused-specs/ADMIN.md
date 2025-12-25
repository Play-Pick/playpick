# 관리자 대시보드 명세서

## 개요
Vue 프론트엔드 기반 관리자 전용 대시보드로, KOPIS API 데이터 수집 및 관리 기능을 제공합니다.

## 접근 방법
- **URL**: `http://localhost:5174/admin`
- **권한**: 슈퍼유저 또는 스태프 권한 필요 (`is_staff=True` 또는 `is_superuser=True`)
- **인증**: JWT 토큰 기반 인증

## 주요 기능

### 1. 데이터 통계 대시보드
실시간으로 데이터베이스 통계를 확인할 수 있습니다.

**통계 항목:**
- 전체 공연 수
- 상세정보 보유 공연 수
- 상세정보 미보유 공연 수
- 공연 중인 공연 수
- 박스오피스 랭킹 총 개수
- 최신 박스오피스 업데이트 날짜
- 장르별 박스오피스 통계

**API 엔드포인트:**
```
GET /api/management/stats/
권한: IsAdminUser
```

### 2. KOPIS 데이터 수집 기능

#### 2.1 박스오피스 랭킹 수집
KOPIS API에서 최신 박스오피스 랭킹을 수집합니다.

**API 엔드포인트:**
```
POST /api/management/collect-boxoffice/
권한: IsAdminUser

Body (선택):
{
  "date": "20251215",        // YYYYMMDD 형식 (기본: 오늘)
  "period_type": "week"      // day/week/month (기본: week)
}
```

**Django Management Command:**
```bash
python manage.py collect_boxoffice
python manage.py collect_boxoffice --date 20251215 --period week
```

#### 2.2 공연 정보 수집
KOPIS API에서 공연 목록을 수집합니다.

**API 엔드포인트:**
```
POST /api/management/collect-performances/
권한: IsAdminUser

Body (선택):
{
  "start_date": "2025-01-01",  // 기본: 30일 전
  "end_date": "2025-12-31"     // 기본: 오늘
}
```

**Django Management Command:**
```bash
python manage.py collect_performances
python manage.py collect_performances --start-date 2025-01-01 --end-date 2025-12-31
```

#### 2.3 공연 상세 정보 수집
상세 정보가 없는 공연의 상세 정보를 수집합니다.

**API 엔드포인트:**
```
POST /api/management/collect-details/
권한: IsAdminUser

Body (선택):
{
  "limit": 100  // 수집 개수 제한 (기본: 100)
}
```

**Django Management Command:**
```bash
python manage.py collect_performance_detail --missing-only --limit 100
python manage.py collect_performance_detail --all  # 전체 재수집
```

#### 2.4 테스트 박스오피스 데이터 생성
DB 내 공연 데이터로 테스트용 박스오피스 랭킹을 생성합니다.

**API 엔드포인트:**
```
POST /api/management/create-test-boxoffice/
권한: IsAdminUser
```

**특징:**
- 각 장르별로 최대 20개씩 생성
- 공연중인 공연 우선 선택
- 오늘 날짜 기준으로 생성
- 기존 오늘 날짜 데이터는 삭제 후 재생성

## 백엔드 구조

### API Views
**파일:** `performances/management_api_views.py`

```python
# 주요 API 클래스
- CollectBoxOfficeAPIView: 박스오피스 수집
- CollectPerformancesAPIView: 공연 정보 수집
- CollectPerformanceDetailAPIView: 공연 상세 정보 수집
- CreateTestBoxOfficeAPIView: 테스트 데이터 생성
- DataStatsAPIView: 데이터 통계 조회
```

**공통 특징:**
- `permission_classes = [IsAdminUser]`: 관리자만 접근 가능
- `io.StringIO()`: 커맨드 출력을 캡처하여 반환
- 예외 처리: try-except로 안전하게 처리
- 응답 형식:
  ```json
  {
    "success": true,
    "message": "작업 완료 메시지",
    "output": "커맨드 실행 로그",
    "data": { /* 추가 데이터 */ }
  }
  ```

### URL 라우팅
**파일:** `mypjt/urls.py`

```python
urlpatterns = [
    # 관리자 전용 - 데이터 수집 API
    path('api/management/collect-boxoffice/', ...),
    path('api/management/collect-performances/', ...),
    path('api/management/collect-details/', ...),
    path('api/management/create-test-boxoffice/', ...),
    path('api/management/stats/', ...),
]
```

## 프론트엔드 구조

### 관리자 대시보드 컴포넌트
**파일:** `front/src/views/AdminDashboardView.vue`

**주요 기능:**
1. **권한 체크**: `onMounted`에서 `authStore.isAdmin` 확인
2. **통계 표시**: 4개의 통계 카드 (공연, 박스오피스, 공연중, 상세정보 없음)
3. **데이터 수집 버튼**: 4가지 수집 작업 버튼
4. **실시간 로그**: 작업 실행 로그 표시 (성공/실패/정보/경고)

### 라우팅
**파일:** `front/src/router/index.js`

```javascript
{
  path: '/admin',
  name: 'admin',
  component: () => import('@/views/AdminDashboardView.vue'),
  meta: { requiresAuth: true, requiresAdmin: true }
}
```

### 인증 스토어
**파일:** `front/src/stores/authStore.js`

```javascript
// 관리자 권한 체크
const isAdmin = computed(() =>
  user.value?.is_staff || user.value?.is_superuser || false
)
```

## 보안

### 권한 검증 레이어

**1. 프론트엔드 (UI 레이어)**
- `authStore.isAdmin`: UI 표시 여부 결정
- `router.beforeEach`: 페이지 접근 제어
- **목적**: 사용자 경험 향상 (불필요한 메뉴 숨김)
- **보안 수준**: 낮음 (클라이언트에서 우회 가능)

**2. 백엔드 (보안 레이어)**
- `permission_classes = [IsAdminUser]`: 실제 권한 검증
- Django의 `is_staff` 또는 `is_superuser` 체크
- **목적**: 실제 보안 적용
- **보안 수준**: 높음 (서버에서 강제)

### UserDetailSerializer에 is_staff 포함
```python
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'date_joined',
            'is_staff', 'is_superuser',  # UI 표시용
            'followers', 'followings',
            'followers_count', 'followings_count'
        ]
```

**보안상 안전한 이유:**
1. `is_staff`는 읽기 전용 정보 (read-only)
2. 외부에서 수정 불가능
3. 실제 권한 검증은 백엔드 API의 `IsAdminUser`에서 수행
4. Django REST framework의 일반적인 관행
5. UI 조건부 렌더링을 위해 필요한 정보

## 관리자 계정 생성

### Superuser 생성
```bash
cd back
python manage.py createsuperuser

# 입력 정보
Username: admin
Email: admin@example.com
Password: (안전한 비밀번호 입력)
```

### 기존 사용자를 스태프로 변경
```bash
python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(username='사용자명')
>>> user.is_staff = True
>>> user.save()
>>> exit()
```

## 사용 예시

### 1. 로그인
1. 슈퍼유저로 로그인
2. JWT 토큰 발급 및 저장

### 2. 관리자 대시보드 접근
1. `http://localhost:5174/admin` 접속
2. 자동으로 권한 체크 (비관리자는 홈으로 리다이렉트)

### 3. 데이터 수집
1. **박스오피스 수집** 버튼 클릭
2. 확인 다이얼로그에서 확인
3. 실행 로그에서 진행 상황 확인
4. 완료 후 통계 자동 업데이트

### 4. 로그 확인
- 성공/실패/정보/경고 로그를 색상으로 구분
- 커맨드 출력 전체를 터미널 스타일로 표시
- "로그 지우기" 버튼으로 로그 초기화

## 운영 환경 배포

### AWS EC2 + Cron (추천)
```bash
# crontab -e
# 매일 새벽 3시 박스오피스 업데이트
0 3 * * * cd /path/to/project && venv/bin/python manage.py collect_boxoffice

# 매주 월요일 새벽 4시 공연 정보 업데이트
0 4 * * 1 cd /path/to/project && venv/bin/python manage.py collect_performances

# 매일 새벽 5시 상세 정보 업데이트 (최대 100개)
0 5 * * * cd /path/to/project && venv/bin/python manage.py collect_performance_detail --missing-only --limit 100
```

### APScheduler (Django 내부)
```python
# settings.py
INSTALLED_APPS += ['django_apscheduler']

# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def start_scheduler():
    scheduler = BackgroundScheduler()

    # 매일 새벽 3시
    scheduler.add_job(
        lambda: call_command('collect_boxoffice'),
        'cron',
        hour=3,
        minute=0
    )

    scheduler.start()
```

## 주의사항

1. **KOPIS API Key**: `.env` 파일에 `KOPIS_API` 키 필수
2. **Rate Limit**: KOPIS API는 초당 10회 제한 (코드에서 0.15초 딜레이 적용)
3. **타임아웃**: 대량 데이터 수집 시 시간 소요 (프론트엔드 타임아웃 주의)
4. **데이터 중복**: `update_or_create` 사용으로 중복 방지
5. **트랜잭션**: 배치 단위로 트랜잭션 처리 (롤백 가능)

## 트러블슈팅

### 403 Forbidden
- 관리자 권한 확인 (`is_staff` 또는 `is_superuser`)
- JWT 토큰 유효성 확인
- 로그아웃 후 재로그인

### 데이터 수집 실패
- KOPIS API 키 확인 (`.env` 파일)
- 네트워크 연결 확인
- API Rate Limit 확인
- 로그 출력에서 상세 에러 확인

### 통계가 업데이트되지 않음
- "새로고침" 버튼 클릭
- 브라우저 콘솔에서 에러 확인
- 백엔드 서버 상태 확인

## API 응답 예시

### 성공 응답
```json
{
  "success": true,
  "message": "박스오피스 데이터 수집 완료",
  "output": "[뮤지컬] 수집 중...\n  뮤지컬: 10건 저장\n총 70건 수집 완료"
}
```

### 실패 응답
```json
{
  "success": false,
  "message": "오류 발생: KOPIS_API 키가 설정되지 않았습니다.",
  "output": ""
}
```

### 통계 응답
```json
{
  "success": true,
  "data": {
    "performances": {
      "total": 62374,
      "with_detail": 62334,
      "without_detail": 40,
      "ongoing": 1234
    },
    "boxoffice": {
      "total": 346,
      "latest_date": "2025-12-15",
      "by_genre": [
        {
          "code": "BBBC",
          "name": "뮤지컬",
          "count": 50
        }
      ]
    }
  }
}
```

## 향후 개선 사항

1. **실시간 진행률 표시**: WebSocket으로 실시간 진행률 업데이트
2. **스케줄링 UI**: 크론 작업을 UI에서 설정/관리
3. **에러 알림**: 이메일/Slack 알림 연동
4. **데이터 백업**: 자동 백업 스케줄링
5. **성능 모니터링**: API 호출 횟수, 응답 시간 추적
