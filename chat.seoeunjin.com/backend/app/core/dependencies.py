"""FastAPI 의존성 함수."""

from typing import Optional

from fastapi import HTTPException
from langchain_core.language_models import BaseChatModel

from backend.app.core.llm import get_llm_model
from backend.app.services.vector_store import VectorStoreService


# 전역 Vector Store 서비스를 가져오기 위한 의존성
# (main.py에서 초기화된 인스턴스 참조)
def get_vector_store_service() -> VectorStoreService:
    """Vector Store 서비스 의존성."""
    from backend.app.main import vector_store_service

    if vector_store_service is None:
        raise HTTPException(
            status_code=503, detail="Vector store가 초기화되지 않았습니다."
        )
    return vector_store_service


def get_llm_dependency() -> BaseChatModel:
    """LLM 모델 의존성.

    FastAPI 엔드포인트에서 사용할 LLM 모델을 주입합니다.

    Returns:
        LLM 모델 인스턴스.

    Raises:
        HTTPException: LLM 모델이 초기화되지 않은 경우.
    """
    llm = get_llm_model()
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM 모델이 초기화되지 않았습니다.")
    return llm


def get_optional_llm_dependency() -> Optional[BaseChatModel]:
    """선택적 LLM 모델 의존성.

    LLM 모델이 선택적으로 필요한 경우 사용합니다.

    Returns:
        LLM 모델 인스턴스 또는 None.
    """
    return get_llm_model()
