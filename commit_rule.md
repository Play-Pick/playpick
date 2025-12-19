# Commit Message 규칙

## Commit Type

| Type | 설명 | 예시 |
|------|------|------|
| **feat** | 새로운 기능 추가 (create 대신 사용) | `feat: 회원가입 기능 구현`<br>`feat: 추천 페이지 UI 추가` |
| **fix** | 버그 수정 | `fix: 로그인 500 에러 해결`<br>`fix: 오타 수정` |
| **docs** | 문서 수정 | `docs: README.md 팀원 소개 추가`<br>`docs: API 명세서 업데이트` |
| **style** | 코드 포맷팅 (로직 변경 ❌) | `style: 세미콜론 누락 수정`<br>`style: 코드 줄바꿈 정리` |
| **refactor** | 코드 리팩토링 (기능 변경 ❌) | `refactor: 중복 코드 함수화`<br>`refactor: 변수명 명확하게 변경` |
| **test** | 테스트 코드 | `test: 회원가입 성공 테스트 코드 추가` |
| **chore** | 기타 설정 및 잡일 | `chore: 패키지 설치`<br>`chore: settings.py 설정 변경`<br>`chore: .gitignore 수정` |

## 작성 예시

```
#feat: front/back 소셜 로그인(카카오) 기능 추가
#fix: front/back 게시글 작성 시 이미지 업로드 오류 수정
#refactor: front/back 추천 알고리즘 for문 최적화
#docs: 프로젝트 실행 가이드(README) 작성
#chore: requirements.txt 패키지 업데이트
```



# Branch 규칙

## 1. `master` 브랜치
- **목적**: 최종 검증된 배포 버전 유지
- **특징**: 항상 안정적이고 배포 가능한 상태 유지

## 2. `develop` 브랜치
- **목적**: 개발 브랜치로 기능 개발 및 버그 수정
- **파생**: `master`에서 파생, 모든 `feature` 브랜치는 `develop`에 병합

## 3. `feat` 브랜치
- **목적**: 새로운 기능 개발
- **명명 규칙**: `feat/<feature-name>`
  - `feat/performance-list`
- **파생**: `develop` 브랜치에서 파생하여 개발 완료 후 `develop`에 병합

## 4. `fix` 브랜치
- **목적**: 기능 개선
- **명명 규칙**: `fix/<feature-name>/개선 내용`
  - 예시: `fix/performance-list`
