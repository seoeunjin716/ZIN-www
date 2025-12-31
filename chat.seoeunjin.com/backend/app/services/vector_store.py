"""Vector Store 서비스."""

from typing import List, Optional

from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document

from backend.app.models.schemas import DocumentItem, SearchResult


class VectorStoreService:
    """Vector Store 서비스 클래스."""

    def __init__(self, vector_store: Optional[PGVector] = None):
        """Vector Store 서비스 초기화."""
        self.vector_store = vector_store

    def search(self, query: str, k: int = 2) -> List[SearchResult]:
        """유사도 검색."""
        if self.vector_store is None:
            raise ValueError("Vector store가 초기화되지 않았습니다.")

        results_with_score = self.vector_store.similarity_search_with_score(query, k=k)

        return [
            SearchResult(
                content=doc.page_content,
                metadata=doc.metadata,
                score=float(score),
            )
            for doc, score in results_with_score
        ]

    def add_documents(self, documents: List[DocumentItem]) -> List[str]:
        """문서 추가."""
        if self.vector_store is None:
            raise ValueError("Vector store가 초기화되지 않았습니다.")

        docs = [
            Document(
                page_content=doc.content,
                metadata=doc.metadata or {},
            )
            for doc in documents
        ]

        return self.vector_store.add_documents(docs)
