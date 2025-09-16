FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 업데이트
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 빌드 인자 선언
ARG GEMINI_API_KEY=""
ARG GEMINI_MODEL_VERSION="gemini-1.5-flash"
ARG EXAONE_BASE_URL="http://localhost:8080"
ARG SEARCH_API_BASE_URL="http://localhost:8000"

# 환경 변수 설정
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
ENV GEMINI_MODEL_VERSION=${GEMINI_MODEL_VERSION}
ENV EXAONE_BASE_URL=${EXAONE_BASE_URL}
ENV SEARCH_API_BASE_URL=${SEARCH_API_BASE_URL}

# 포트 노출
EXPOSE 8001

# 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]