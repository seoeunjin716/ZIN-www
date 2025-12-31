"""RAG (Retrieval Augmented Generation) 서비스."""

from typing import List, Optional

from langchain_core.language_models import BaseChatModel

from backend.app.services.vector_store import VectorStoreService


class RAGService:
    """RAG 서비스 클래스.

    Vector Store와 LLM을 결합하여 RAG 기능을 제공합니다.
    """

    def __init__(
        self,
        vector_store_service: VectorStoreService,
        llm_model: Optional[BaseChatModel] = None,
    ):
        """RAG 서비스 초기화.

        Args:
            vector_store_service: Vector Store 서비스 인스턴스.
            llm_model: LLM 모델 인스턴스 (선택적).
        """
        self.vector_store_service = vector_store_service
        self.llm_model = llm_model

    def set_llm_model(self, llm_model: BaseChatModel) -> None:
        """LLM 모델 설정.

        Args:
            llm_model: 설정할 LLM 모델 인스턴스.
        """
        self.llm_model = llm_model

    async def generate_response(
        self,
        query: str,
        k: int = 2,
    ) -> str:
        """검색된 문서를 기반으로 응답 생성.

        Args:
            query: 사용자 쿼리.
            k: 검색할 문서 수.

        Returns:
            LLM이 생성한 응답.

        Raises:
            ValueError: LLM 모델이 설정되지 않은 경우.
        """
        if self.llm_model is None:
            raise ValueError("LLM 모델이 설정되지 않았습니다.")

        # 문서 검색
        search_results = self.vector_store_service.search(query, k=k)

        # 검색된 문서를 컨텍스트로 구성
        context = "\n\n".join(
            [f"[{i + 1}] {result.content}" for i, result in enumerate(search_results)]
        )

        # 프롬프트 구성
        prompt = f"""다음 문서들을 참고하여 질문에 답변해주세요.

문서:
{context}

질문: {query}

답변:"""

        # LLM으로 응답 생성
        response = await self.llm_model.ainvoke(prompt)

        # 응답이 AIMessage인 경우 content 추출
        if hasattr(response, "content"):
            return response.content
        return str(response)

    def search_documents(self, query: str, k: int = 2) -> List:
        """문서 검색 (LLM 없이).

        Args:
            query: 검색 쿼리.
            k: 검색할 문서 수.

        Returns:
            검색 결과 리스트.
        """
        return self.vector_store_service.search(query, k=k)
