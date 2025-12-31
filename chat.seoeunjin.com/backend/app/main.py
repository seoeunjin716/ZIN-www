"""FastAPI 애플리케이션 진입점."""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.core.database import check_postgres_connection, initialize_vector_store
from backend.app.router.chat_router import router as chat_router
from backend.app.services.vector_store import VectorStoreService

# 전역 Vector Store 서비스
vector_store_service: Optional[VectorStoreService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 시 실행되는 lifespan 이벤트."""
    global vector_store_service

    # 시작 시
    print("🚀 LangChain + pgvector FastAPI 서버 시작!")
    print("-" * 50)

    # PostgreSQL 연결 확인 (Neon PostgreSQL 사용)
    check_postgres_connection()

    # Vector Store 초기화
    vector_store = initialize_vector_store()
    if vector_store is None:
        print("⚠️  Vector Store 초기화 실패 - Vector Store 기능은 사용할 수 없습니다.")
        vector_store_service = None
    else:
        vector_store_service = VectorStoreService(vector_store)

    # LLM 모델 초기화 - Midm 모델 사용
    try:
        from backend.app.core.llm import initialize_llm_model
        from backend.app.core.model_loader import load_midm_langchain_model

        print("📦 Midm 모델 로딩 중...")
        llm = load_midm_langchain_model(
            torch_dtype="bfloat16",  # RTX 3050 지원, 메모리 효율적
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
        )
        initialize_llm_model(llm)
        print("✅ Midm 모델 초기화 완료")
    except Exception as e:
        print(f"⚠️  Midm 모델 로딩 실패: {e}")
        print("   LLM 기능은 사용할 수 없습니다.")

    print("✅ 초기화 완료!")
    print("=" * 50)

    yield

    # 종료 시 (필요한 정리 작업)


app = FastAPI(
    title="LangChain RAG API",
    description="LangChain과 pgvector를 사용한 RAG (Retrieval Augmented Generation) API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(router, prefix="/api/v1", tags=["RAG"])
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])


@app.get("/")
async def root():
    """루트 엔드포인트."""
    return {
        "message": "LangChain RAG API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
