# Core 모듈

애플리케이션의 핵심 설정, 초기화, 의존성 관리 모듈입니다.

## 구조

```
core/
├── __init__.py          # 모듈 export
├── config.py            # 애플리케이션 설정 (환경 변수 등)
├── database.py          # 데이터베이스 연결 및 Vector Store 초기화
├── llm.py               # LLM 모델 초기화 및 관리
├── model_loader.py      # 로컬 HuggingFace 모델 로더 ⭐
├── dependencies.py      # FastAPI 의존성 함수
└── README.md            # 이 파일
```

## 모델 로더 (`model_loader.py`)

로컬에 저장된 Midm 모델을 로드하는 함수들을 제공합니다.

### 사용 방법

#### 1. 기본 사용 (transformers만)

```python
from backend.app.core.model_loader import load_midm_model

model, tokenizer = load_midm_model()
```

#### 2. HuggingFace Pipeline 생성

```python
from backend.app.core.model_loader import create_midm_pipeline

pipe = create_midm_pipeline(
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True,
)
```

#### 3. LangChain HuggingFacePipeline로 로드 (권장)

```python
from backend.app.core.model_loader import load_midm_langchain_model
from backend.app.core.llm import initialize_llm_model

# LangChain 모델로 로드
llm = load_midm_langchain_model(
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True,
)

# LLM 모델 초기화
initialize_llm_model(llm)
```

### main.py에서 사용 예시

```python
from backend.app.core.model_loader import load_midm_langchain_model
from backend.app.core.llm import initialize_llm_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... 기타 초기화 ...

    # Midm 모델 로드 및 초기화
    llm = load_midm_langchain_model(
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True,
    )
    initialize_llm_model(llm)

    yield
```

### 모델 경로

기본 모델 경로: `backend/app/models/midm`

다른 경로를 사용하려면:

```python
llm = load_midm_langchain_model(
    model_path="/path/to/your/model",
    max_new_tokens=512,
)
```

### 파라미터

- `model_path`: 모델 경로 (기본값: `backend/app/models/midm`)
- `torch_dtype`: torch dtype (기본값: `"auto"`)
- `device_map`: 디바이스 맵핑 (기본값: `"auto"`)
- `trust_remote_code`: 원격 코드 신뢰 여부 (기본값: `True`, Midm 필수)
- `**pipeline_kwargs`: pipeline에 전달할 추가 인자 (예: `max_new_tokens`, `temperature` 등)

## LLM 모델 주입

자세한 내용은 [LLM 모델 주입 가이드](llm.py)를 참조하세요.
