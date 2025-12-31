"""
😎😎 FastAPI 기준의 API 엔드포인트 계층입니다.

chat_router.py
POST /api/v1/chat
세션 ID, 메시지 리스트 등을 받아 대화형 응답 반환.
"""

from fastapi import APIRouter, HTTPException

from backend.app.core.llm import get_llm_model
from backend.app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """채팅 엔드포인트."""
    try:
        llm = get_llm_model()
        if llm is None:
            raise HTTPException(
                status_code=503,
                detail="LLM 모델이 초기화되지 않았습니다.",
            )

        # 대화 히스토리를 프롬프트 문자열로 변환
        prompt_parts = []

        # 시스템 프롬프트
        prompt_parts.append(
            "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 대화합니다.\n\n"
        )

        # 대화 히스토리 추가
        if request.history:
            for msg in request.history:
                if msg.role == "user":
                    prompt_parts.append(f"사용자: {msg.content}\n")
                elif msg.role == "assistant":
                    prompt_parts.append(f"어시스턴트: {msg.content}\n")

        # 현재 메시지 추가
        prompt_parts.append(f"사용자: {request.message}\n어시스턴트:")

        prompt = "".join(prompt_parts)

        # LLM 호출 (HuggingFacePipeline은 문자열을 받음)
        llm_response = await llm.ainvoke(prompt)

        # 응답 추출
        if isinstance(llm_response, str):
            response_text = llm_response
        elif hasattr(llm_response, "content"):
            response_text = str(getattr(llm_response, "content"))
        else:
            response_text = str(llm_response)

        return ChatResponse(response=response_text)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"챗봇 응답 생성 중 오류 발생: {str(e)}",
        )
