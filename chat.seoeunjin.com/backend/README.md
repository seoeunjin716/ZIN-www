# Backend API

LangChain과 pgvector를 사용한 RAG (Retrieval Augmented Generation) FastAPI 백엔드.

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API 라우터
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # 설정
│   │   ├── database.py      # 데이터베이스 연결 및 초기화
│   │   └── model_loader.py  # 모델 로더
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic 모델
│   └── services/
│       ├── __init__.py
│       └── vector_store.py  # Vector Store 서비스
├── scripts/
│   └── hello_world.py       # 원본 예제 스크립트
├── requirements.txt         # Python 의존성
└── run.py                   # 서버 실행 스크립트
```

## 로컬 개발 환경 설정

### 1. 의존성 설치

```bash
# 프로젝트 루트에서
cd backend
pip install -r requirements.txt

# 또는 가상환경 사용 (권장)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하거나 환경 변수를 설정합니다:

```bash
# .env 파일 생성 (프로젝트 루트 또는 backend 디렉토리)
POSTGRES_CONNECTION_STRING=postgresql://neondb_owner:npg_l7ivQxhmjJA3@ep-rough-moon-a1hk3p1c-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
OPENAI_API_KEY=your-openai-api-key-here  # 선택사항
```

또는 PowerShell에서:

```powershell
$env:POSTGRES_CONNECTION_STRING="postgresql://neondb_owner:npg_l7ivQxhmjJA3@ep-rough-moon-a1hk3p1c-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. 서버 실행

#### 방법 1: run.py 사용 (권장)

```bash
# 프로젝트 루트에서
python backend/run.py

# 또는 backend 디렉토리에서
cd backend
python run.py
```

#### 방법 2: uvicorn 직접 사용

```bash
# 프로젝트 루트에서
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# 또는 backend 디렉토리에서
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 실행 확인

서버가 시작되면 다음 URL에서 접근할 수 있습니다:

- API 문서: http://localhost:8000/docs
- 대체 문서: http://localhost:8000/redoc
- 헬스 체크: http://localhost:8000/api/v1/health

## 환경 변수

### 필수 환경 변수

- `POSTGRES_CONNECTION_STRING`: Neon PostgreSQL 연결 문자열

### 선택적 환경 변수

- `OPENAI_API_KEY`: OpenAI API 키 (OpenAI Embeddings 사용 시)
- `POSTGRES_HOST`: PostgreSQL 호스트 (연결 문자열 미사용 시)
- `POSTGRES_PORT`: PostgreSQL 포트 (연결 문자열 미사용 시)
- `POSTGRES_USER`: PostgreSQL 사용자 (연결 문자열 미사용 시)
- `POSTGRES_PASSWORD`: PostgreSQL 비밀번호 (연결 문자열 미사용 시)
- `POSTGRES_DB`: PostgreSQL 데이터베이스 (연결 문자열 미사용 시)

## 문제 해결

### 모듈을 찾을 수 없는 오류

```bash
# 프로젝트 루트에서 실행해야 합니다
# backend 디렉토리에서 실행하면 import 오류가 발생할 수 있습니다
```

### PostgreSQL 연결 오류

- Neon PostgreSQL 연결 문자열이 올바른지 확인
- 네트워크 연결 확인
- SSL 모드가 올바르게 설정되었는지 확인

### 포트가 이미 사용 중

```bash
# 다른 포트 사용
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8001
```

## API 엔드포인트

- `GET /`: API 정보
- `GET /api/v1/health`: 헬스 체크
- `POST /api/v1/search`: 유사도 검색
- `POST /api/v1/documents`: 문서 추가
- `GET /docs`: Swagger UI 문서
