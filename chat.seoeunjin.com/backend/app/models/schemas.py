"""Pydantic 스키마 모델."""

from typing import Any, List, Optional

from pydantic import BaseModel


class SearchQuery(BaseModel):
    """검색 쿼리 모델."""

    query: str
    k: int = 2


class DocumentItem(BaseModel):
    """문서 아이템 모델."""

    content: str
    metadata: Optional[dict[str, Any]] = None


class SearchResult(BaseModel):
    """검색 결과 모델."""

    content: str
    metadata: dict[str, Any]
    score: Optional[float] = None


class SearchResponse(BaseModel):
    """검색 응답 모델."""

    results: List[SearchResult]
    count: int


class DocumentResponse(BaseModel):
    """문서 추가 응답 모델."""

    message: str
    document_ids: List[str]


class ChatMessage(BaseModel):
    """채팅 메시지 모델."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """채팅 요청 모델."""

    message: str
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """채팅 응답 모델."""

    response: str
