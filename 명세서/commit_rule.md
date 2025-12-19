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
feat: 소셜 로그인(카카오) 기능 추가
fix: 게시글 작성 시 이미지 업로드 오류 수정
refactor: 추천 알고리즘 for문 최적화
docs: 프로젝트 실행 가이드(README) 작성
chore: requirements.txt 패키지 업데이트
```