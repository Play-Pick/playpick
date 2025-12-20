# 임베딩 데이터 관리 가이드

## 개요

AI 검색 기능을 위한 임베딩 벡터 생성, 추출, 공유 방법을 설명합니다.

### 모델 구조

```
Performance (공연 기본 정보)
    ↓ OneToOne
PerformanceEmbedding (임베딩 벡터)
    - vector: JSONField (1536차원)
    - created_at: DateTime
    - updated_at: DateTime
```

**분리 이유:**
- Performance 테이블 용량 최적화 (1536차원 벡터 분리)
- 일반 공연 조회 시 성능 향상
- 임베딩 재생성 시 안전성 확보
- 벡터 DB 확장 용이

---

## 1. 임베딩 생성

### 1.1 전체 공연 임베딩 생성

```bash
python manage.py generate_embeddings
```

**동작:**
- 임베딩이 없는 공연들만 자동 선택
- OpenAI `text-embedding-3-small` 모델 사용 (1536차원)
- PerformanceEmbedding 테이블에 저장

**옵션:**
```bash
# 배치 크기 조정
python manage.py generate_embeddings --batch-size 50

# 기존 임베딩도 재생성 (강제)
python manage.py generate_embeddings --force
```

### 1.2 임베딩 텍스트 생성 전략

`test_strategy_2_standard` 방식 사용:

```
공연명 + 장르 + 출연진 + 지역 + 공연시설 + 관람연령 + 러닝타임 + 제작사 + 줄거리(200자)
```

---

## 2. 임베딩 추출 (팀원 공유용)

### 2.1 NumPy 포맷으로 추출

```bash
python manage.py export_embeddings --export
```

**결과:**
```
embeddings/performance_embeddings.npz  (약 15.3 MB)
```

**포함 데이터:**
- `mt20ids`: 공연 ID 배열
- `embeddings`: 임베딩 벡터 배열 (1536차원)
- `updated_ats`: 업데이트 시간 배열

**장점:**
- JSON 대비 약 2.4배 작은 용량
- 압축 포맷 (.npz)
- 빠른 로드 속도

### 2.2 출력 디렉토리 지정

```bash
python manage.py export_embeddings --export --output-dir custom_path
```

---

## 3. 임베딩 로드 (팀원이 받은 파일 사용)

### 3.1 기본 로드

```bash
python manage.py export_embeddings --import embeddings/performance_embeddings.npz
```

**동작:**
- 이미 임베딩이 있는 공연은 자동 스킵
- DB에 없는 공연은 경고 후 건너뜀
- PerformanceEmbedding 테이블에 저장

### 3.2 로드 과정

```
1. .npz 파일 읽기
2. Performance 존재 여부 확인
3. 기존 임베딩 있으면 스킵
4. PerformanceEmbedding.objects.update_or_create()
5. 결과 출력 (성공/스킵/미발견)
```

---

## 4. Fixture 데이터 추출

### 4.1 전체 앱 데이터 추출

```bash
# 기본 스크립트 (임베딩 제외)
python export_fixtures.py
```

**결과:**
```
fixtures/
  ├── performances.json    (공연 기본 정보)
  ├── accounts.json        (사용자 정보)
  └── community.json       (커뮤니티 정보)
```

### 4.2 Management Command 방식

```bash
# performances 앱 전체 (임베딩 제외)
python manage.py export_fixture performances --all

# PerformanceEmbedding 포함
python manage.py export_fixture performances --all --include-embedding

# 특정 모델만
python manage.py export_fixture performances Performance
python manage.py export_fixture performances PerformanceEmbedding
```

### 4.3 출력 디렉토리 지정

```bash
python manage.py export_fixture performances --all --output-dir custom_fixtures
```

---

## 5. 데이터 공유 전략

### 5.1 일반 데이터 공유

**방법:** Django Fixture (JSON)

```bash
# 추출
python export_fixtures.py

# 로드
python manage.py loaddata fixtures/performances.json
python manage.py loaddata fixtures/accounts.json
python manage.py loaddata fixtures/community.json
```

### 5.2 임베딩 데이터 공유

**방법:** NumPy 압축 파일 (.npz)

```bash
# 추출
python manage.py export_embeddings --export

# 공유 (파일 전달)
embeddings/performance_embeddings.npz → 팀원에게 전달

# 로드
python manage.py export_embeddings --import embeddings/performance_embeddings.npz
```

### 5.3 전체 프로세스 (신규 팀원 온보딩)

```bash
# 1. 기본 데이터 로드
python manage.py loaddata fixtures/performances.json
python manage.py loaddata fixtures/accounts.json
python manage.py loaddata fixtures/community.json

# 2. 마이그레이션 적용
python manage.py migrate

# 3. 임베딩 데이터 로드
python manage.py export_embeddings --import embeddings/performance_embeddings.npz

# 4. 완료!
```

---

## 6. 파일 크기 비교

| 데이터 | JSON (Fixture) | NumPy (.npz) | 비율 |
|--------|----------------|--------------|------|
| 공연 기본 정보 | ~5 MB | - | - |
| 임베딩 (3088개) | ~36 MB | ~15 MB | 2.4배 절약 |

**권장:**
- 일반 데이터: JSON Fixture 사용
- 임베딩 데이터: NumPy .npz 사용

---

## 7. 환경 변수 설정

임베딩 생성에 필요한 환경 변수:

```bash
# .env 파일
GMS_KEY=your-gms-api-key
```

**확인 방법:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GMS_KEY'))"
```

---

## 8. 트러블슈팅

### 8.1 임베딩 생성 중단

**증상:** 1700개 정도에서 멈춤

**원인:** API Rate Limiting

**해결:**
```bash
# 다시 실행 (이미 생성된 것은 자동 스킵)
python manage.py generate_embeddings
```

### 8.2 임베딩 로드 시 스킵

**증상:** 모든 데이터가 스킵됨

**원인:** 이미 임베딩이 존재

**해결:**
```bash
# 강제 재로드 (기존 데이터 덮어쓰기)
# 현재는 수동으로 삭제 후 재실행
python manage.py shell
>>> from performances.models import PerformanceEmbedding
>>> PerformanceEmbedding.objects.all().delete()
>>> exit()

python manage.py export_embeddings --import embeddings/performance_embeddings.npz
```

### 8.3 마이그레이션 오류

**증상:** PerformanceEmbedding 모델 없음

**해결:**
```bash
python manage.py migrate performances
```

---

## 9. API 사용량 참고

### 9.1 임베딩 생성 비용

- 모델: `text-embedding-3-small`
- 공연당 평균 토큰: ~200 tokens
- 3088개 공연: ~617,600 tokens
- 예상 비용: GMS 키 사용 (무료)

### 9.2 Rate Limiting 대응

```python
# generate_embeddings.py
time.sleep(0.05)  # 각 요청마다 50ms 대기
```

---

## 10. 데이터 검증

### 10.1 임베딩 개수 확인

```bash
python manage.py shell -c "from performances.models import PerformanceEmbedding; print(f'Total: {PerformanceEmbedding.objects.count()}')"
```

### 10.2 임베딩 차원 확인

```bash
python manage.py shell
>>> from performances.models import PerformanceEmbedding
>>> emb = PerformanceEmbedding.objects.first()
>>> len(emb.vector)
1536
```

### 10.3 누락된 공연 확인

```bash
python manage.py shell
>>> from performances.models import Performance
>>> without_embedding = Performance.objects.filter(embedding__isnull=True).count()
>>> print(f'임베딩 없는 공연: {without_embedding}개')
```

---

## 11. 백업 전략

### 11.1 정기 백업

```bash
# 매주 월요일 임베딩 백업
python manage.py export_embeddings --export --output-dir backups/embeddings_$(date +%Y%m%d)
```

### 11.2 Git에 포함하지 말 것

```gitignore
# .gitignore
embeddings/*.npz
fixtures/*.json
backups/
```

### 11.3 클라우드 스토리지 활용

```bash
# 예: Google Drive, Dropbox, AWS S3 등에 업로드
# performance_embeddings.npz 파일만 공유
```

---

## 12. 성능 최적화 팁

### 12.1 AI 검색 쿼리 최적화

```python
# ai_search.py
performances = list(
    performances_qs.filter(embedding__isnull=False)
    .select_related('embedding')  # 조인 최적화
)
```

### 12.2 배치 크기 조정

```bash
# 메모리 부족 시
python manage.py generate_embeddings --batch-size 50

# 빠른 처리 (메모리 충분 시)
python manage.py generate_embeddings --batch-size 200
```

---

## 요약

| 작업 | 명령어 |
|------|--------|
| 임베딩 생성 | `python manage.py generate_embeddings` |
| 임베딩 추출 | `python manage.py export_embeddings --export` |
| 임베딩 로드 | `python manage.py export_embeddings --import embeddings/performance_embeddings.npz` |
| Fixture 추출 | `python export_fixtures.py` |
| 개수 확인 | `python manage.py shell -c "from performances.models import PerformanceEmbedding; print(PerformanceEmbedding.objects.count())"` |
