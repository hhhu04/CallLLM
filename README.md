# CallLLM

문서 검색 기반 질의응답 시스템입니다. 외부 검색 API에서 관련 문서를 가져와 Gemini 또는 EXAONE을 통해 답변을 생성합니다.

## 기능

- **문서 기반 질의응답**: 외부 검색 API를 통해 관련 문서를 찾아 AI 모델이 답변 생성
- **다중 AI 모델 지원**: Google Gemini와 LG EXAONE 로컬 서버 지원
- **RESTful API**: FastAPI 기반의 간단한 웹 API
- **환경 변수 관리**: .env 파일을 통한 설정 관리

## API 엔드포인트

### `/gemini`
Google Gemini를 사용한 질의응답
- **Method**: GET
- **Parameters**:
  - `query`: 질문 내용
  - `index_name`: 인덱스 이름
  - `path`: 파일 경로

### `/exaone`
LG EXAONE 로컬 서버를 사용한 질의응답
- **Method**: GET
- **Parameters**:
  - `query`: 질문 내용
  - `index_name`: 인덱스 이름
  - `path`: 파일 경로

### `/exaone/health`
EXAONE 서버 상태 확인
- **Method**: GET
- **Response**: 서버 상태 정보

### `/hello/{name}`
간단한 인사 테스트 엔드포인트
- **Method**: GET
- **Parameters**:
  - `name`: 이름

## 설정

### 환경 변수 (.env 파일)

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_VERSION=gemini-1.5-flash

# EXAONE Local Server Configuration
EXAONE_BASE_URL=http://localhost:8080

# External API Configuration
SEARCH_API_BASE_URL=http://localhost:8000
```

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 필요한 API 키와 서버 URL을 설정하세요.

### 3. 서버 실행
```bash
uvicorn main:app --reload
```

기본적으로 `http://localhost:8000`에서 실행됩니다.

## 프로젝트 구조

```
CallLLM/
├── main.py          # FastAPI 애플리케이션 메인
├── llm.py           # Gemini 서비스
├── xaion.py         # EXAONE 서비스
├── client.py        # HTTP 클라이언트 유틸리티
├── requirements.txt # 패키지 의존성
├── .env            # 환경 변수 (git에서 제외)
└── .gitignore      # Git 제외 파일 목록
```

## 주요 구성 요소

### GeminiService (llm.py)
- Google Gemini API를 사용한 답변 생성
- 문서 컨텍스트 기반 프롬프트 구성
- 참조 문서 목록 자동 생성

### ExaoneService (xaion.py)
- LG EXAONE 로컬 서버와의 통신
- Gemini와 동일한 인터페이스 제공
- 서버 상태 확인 기능

### APIClient (client.py)
- 외부 검색 API와의 비동기 HTTP 통신
- GET/POST 요청 지원
- 타임아웃 및 오류 처리

## 사용 예시

### Gemini로 질문하기
```bash
curl "http://localhost:8000/gemini?query=제안서%20마감일&index_name=test&path=test1"
```

### EXAONE으로 질문하기
```bash
curl "http://localhost:8000/exaone?query=제안서%20마감일&index_name=test&path=test1"
```

### EXAONE 서버 상태 확인
```bash
curl "http://localhost:8000/exaone/health"
```