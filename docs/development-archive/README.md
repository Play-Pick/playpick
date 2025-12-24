# 📦 개발 과정 문서 아카이브

> 이 폴더는 프로젝트 개발 과정에서 작성된 문서들을 보관합니다.
> **최종 제출용 문서**는 [`../final-submission/`](../final-submission/) 폴더를 참고하세요.

---

## 📂 폴더 구조

```
development-archive/
├── refactoring/              # 리팩토링 계획 및 TODO
│   ├── REFACTORING.md
│   ├── FRONTEND_REFACTORING_TODO.md
│   └── FRONTEND_REFACTORING_TODO_API.md
│
├── todo-lists/               # 개발 중 작성한 TODO 리스트
│   ├── todo.md
│   └── ai_todo.md
│
├── ai-development/           # AI 기능 개발 과정
│   ├── ai_구현_1.md
│   ├── AI활용방안.md
│   └── aitest/              # AI 테스트 파일들
│
├── guides/                   # 개발 과정 가이드 문서
│   ├── 프론트엔드_작업가이드.md
│   ├── 프론트엔드_인수인계서.md
│   ├── Card-Components-Analysis.md
│   └── Vue-Slots-Guide.md
│
├── unused-specs/             # 초기 명세서 (최종본으로 통합됨)
│   ├── 찜하기_기능_가이드.md
│   ├── 찜하기_버튼_구현_완료.md
│   ├── 공연추천_알고리즘_설계서.md
│   ├── 추천알고리즘_상세구현방안1.md
│   ├── JWT_IMPLEMENTATION_GUIDE.md
│   └── ADMIN.md
│
├── 프로젝트-회고.md          # 개발 과정 회고
└── 커밋규칙.md               # Git 커밋 컨벤션
```

---

## 📋 폴더별 설명

### 🔧 refactoring/
프론트엔드/백엔드 리팩토링 계획 및 개선 사항
- 코드 품질 개선 항목
- 성능 최적화 TODO
- 구조 개선 계획

### ✅ todo-lists/
개발 중 작성한 할 일 목록
- 전체 프로젝트 TODO
- AI 기능 개발 TODO
- 완료된 항목 포함

### 🤖 ai-development/
AI 기능 개발 과정 문서 및 테스트
- OpenAI Embedding 실험
- 추천 알고리즘 프로토타입
- AI 검색 성능 테스트
- 임베딩 생성 테스트 코드

### 📖 guides/
팀원 간 인수인계 및 작업 가이드
- 프론트엔드 컴포넌트 분석
- Vue Slots 활용법
- 작업 환경 설정 가이드
- 코드 작성 규칙

### 📄 unused-specs/
초기 작성된 명세서 (이후 통합 문서로 대체됨)
- 찜하기 기능 초기 명세 → `final-submission/03-기능-명세/02-관람함-찜하기.md`로 통합
- 추천 알고리즘 초기 설계 → `final-submission/02-기술-문서/01-추천알고리즘.md`로 통합
- JWT 구현 가이드 초기 버전 → `final-submission/02-기술-문서/03-JWT-인증시스템.md`로 통합

### 📝 기타 문서
- **프로젝트-회고.md**: 개발 과정에서의 고민과 배운 점
- **커밋규칙.md**: Git 커밋 메시지 컨벤션

---

## 🎯 최종 제출 문서와의 관계

| 아카이브 문서 | 최종 문서 |
|:---|:---|
| `ai-development/` → | `final-submission/02-기술-문서/02-AI-검색엔진.md` |
| `unused-specs/추천알고리즘_*.md` → | `final-submission/02-기술-문서/01-추천알고리즘.md` |
| `unused-specs/찜하기_*.md` → | `final-submission/03-기능-명세/02-관람함-찜하기.md` |
| `unused-specs/JWT_*.md` → | `final-submission/02-기술-문서/03-JWT-인증시스템.md` |
| `guides/프론트엔드_*.md` → | `final-submission/01-프로젝트-개요/03-프론트엔드-개요.md` |

---

## 📌 참고 사항

- 이 문서들은 **제출 시 포함하지 않음**
- 개발 과정 참고용으로만 보관
- 최종 제출 문서는 **[`docs/final-submission/`](../final-submission/)** 폴더 사용
- 프로젝트 히스토리 및 의사결정 과정 추적용

---

**아카이브 생성일**: 2025-12-24
**정리자**: Claude Code Assistant
