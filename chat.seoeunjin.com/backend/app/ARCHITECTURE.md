# 백엔드 아키텍처

LLM 모델 주입을 위한 최적화된 아키텍처 구조입니다.

## 디렉토리 구조

```
backend/app/
├── api/                    # API 라우터
│   ├── __init__.py
│   └── routes.py          # API 엔드포인트 정의
│
├── core/                   # 핵심 모듈 (설정, 초기화, 의존성)
│   ├── __init__.py
│   ├── config.py          # 애플리케이션 설정
│   ├── database.py        # 데이터베이스 및 Vector Store 초기화
│   ├── llm.py             # LLM 모델 관리 (⭐ 모델 주입 위치)
│   ├── dependencies.py    # FastAPI 의존성 함수
│   └── README.md          # Core 모듈 설명
│
├── models/                 # Pydantic 스키마
│   ├── __init__.py
│   └── schemas.py         # 요청/응답 모델
│
├── services/               # 비즈니스 로직
│   ├── __init__.py
│   ├── vector_store.py    # Vector Store 서비스
│   └── rag_service.py     # RAG 서비스 (Vector + LLM)
│
├── main.py                 # FastAPI 앱 진입점
└── __init__.py
```

## LLM 모델 주입 방법

### 방법 1: main.py에서 직접 주입 (권장)

`backend/app/main.py`의 `lifespan` 함수에서 LLM 모델을 초기화합니다.

```python
from backend.app.core.llm import initialize_llm_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... 기타 초기화 ...

    # LLM 모델 주입
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    initialize_llm_model(llm)

    yield
```

### 방법 2: FastAPI 의존성으로 주입

API 엔드포인트에서 `Depends`를 사용하여 LLM 모델을 주입받습니다.

```python
from fastapi import Depends
from backend.app.core.dependencies import get_llm_dependency

@router.post("/chat")
async def chat(llm: BaseChatModel = Depends(get_llm_dependency)):
    response = await llm.ainvoke("Hello")
    return {"response": response.content}
```

### 방법 3: 서비스 레이어에서 사용

`RAGService`나 다른 서비스에서 LLM 모델을 사용합니다.

```python
from backend.app.core.llm import get_llm_model
from backend.app.services.rag_service import RAGService

# 서비스 생성
rag_service = RAGService(
    vector_store_service,
    llm_model=get_llm_model()
)

# 사용
response = await rag_service.generate_response("질문", k=3)
```

## 모듈 설명

### `core/llm.py`

LLM 모델의 전역 인스턴스를 관리합니다.

- `llm_model`: 전역 LLM 모델 인스턴스
- `initialize_llm_model(model)`: LLM 모델 초기화
- `get_llm_model()`: LLM 모델 인스턴스 가져오기
- `reset_llm_model()`: LLM 모델 리셋

### `core/dependencies.py`

FastAPI의 의존성 주입 함수를 제공합니다.

- `get_llm_dependency()`: 필수 LLM 모델 의존성 (없으면 503 에러)
- `get_optional_llm_dependency()`: 선택적 LLM 모델 의존성 (없으면 None)
- `get_vector_store_service()`: Vector Store 서비스 의존성

### `services/rag_service.py`

RAG (Retrieval Augmented Generation) 기능을 제공하는 서비스입니다.

- `generate_response(query, k)`: 검색된 문서를 기반으로 응답 생성
- `search_documents(query, k)`: 문서 검색 (LLM 없이)
- `set_llm_model(llm)`: LLM 모델 설정

## 데이터 흐름

```
1. main.py (lifespan)
   └─> initialize_llm_model(llm_instance)
       └─> core/llm.py: llm_model = llm_instance

2. API 엔드포인트
   └─> Depends(get_llm_dependency)
       └─> core/dependencies.py: get_llm_dependency()
           └─> core/llm.py: get_llm_model()
               └─> return llm_model

3. 서비스 레이어
   └─> get_llm_model()
       └─> core/llm.py: get_llm_model()
           └─> return llm_model
```

## 사용 예시

### 완전한 예시

```python
# 1. main.py에서 초기화
from backend.app.core.llm import initialize_llm_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # LLM 모델 주입
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    initialize_llm_model(llm)
    yield

# 2. API에서 사용
from backend.app.core.dependencies import get_llm_dependency

@router.post("/chat")
async def chat(
    query: str,
    llm: BaseChatModel = Depends(get_llm_dependency)
):
    response = await llm.ainvoke(query)
    return {"response": response.content}

# 3. 서비스에서 사용
from backend.app.services.rag_service import RAGService
from backend.app.core.llm import get_llm_model

rag_service = RAGService(vector_store_service, llm_model=get_llm_model())
response = await rag_service.generate_response("질문", k=3)
```

## 확장성

이 아키텍처는 다음을 지원합니다:

- ✅ 여러 LLM 모델 지원 (순차 교체 가능)
- ✅ LLM 모델이 선택적인 엔드포인트 지원
- ✅ 테스트를 위한 모의(Mock) LLM 주입
- ✅ 서비스 레이어와 API 레이어의 명확한 분리
- ✅ FastAPI의 의존성 주입 패턴 활용

