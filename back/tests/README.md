# 테스트 및 유틸리티 스크립트

개발 과정에서 사용된 테스트 스크립트 및 데이터 생성 도구입니다.

## 파일 목록

### 박스오피스 관련
- **create_test_boxoffice.py** - 테스트용 박스오피스 랭킹 데이터 생성

### 장르/데이터 검증
- **test_api_genre.py** - 장르별 박스오피스 데이터 확인
- **test_genre.py** - 장르 코드별 데이터 검증 (JSON 출력)
- **test_ranking_dates.py** - 랭킹 날짜 및 장르별 genrenm 통계

### 환경 변수
- **test_env.py** - .env 파일의 환경 변수 로드 테스트

## 사용법

각 스크립트는 Django 환경에서 독립적으로 실행 가능합니다:

```bash
# 예시
python tests/create_test_boxoffice.py
python tests/test_genre.py
```

## 참고사항

이 파일들은 개발/디버깅 목적으로 작성되었으며, 프로덕션 환경에서는 필요하지 않습니다.
