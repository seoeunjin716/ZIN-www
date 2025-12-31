"""API 라우터."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.dependencies import get_vector_store_service
from backend.app.models.schemas import (
    DocumentItem,
    DocumentResponse,
    SearchQuery,
    SearchResponse,
)
from backend.app.services.vector_store import VectorStoreService

router = APIRouter()


@router.get("/health")
async def health_check():
    """헬스 체크 엔드포인트."""
    from backend.app.main import vector_store_service

    return {
        "status": "healthy",
        "vector_store_initialized": vector_store_service is not None
        and vector_store_service.vector_store is not None,
    }


@router.post("/search", response_model=SearchResponse)
async def search(
    query: SearchQuery,
    service: VectorStoreService = Depends(get_vector_store_service),
):
    """유사도 검색 엔드포인트."""
    try:
        results = service.search(query.query, k=query.k)
        return SearchResponse(results=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류 발생: {str(e)}")


@router.post("/documents", response_model=DocumentResponse)
async def add_documents(
    documents: List[DocumentItem],
    service: VectorStoreService = Depends(get_vector_store_service),
):
    """문서 추가 엔드포인트."""
    try:
        document_ids = service.add_documents(documents)
        return DocumentResponse(
            message=f"{len(documents)}개의 문서가 추가되었습니다.",
            document_ids=document_ids,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 추가 중 오류 발생: {str(e)}")
