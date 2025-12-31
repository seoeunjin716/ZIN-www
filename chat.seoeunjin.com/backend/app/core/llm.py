"""LLM 모델 초기화 및 관리."""

from typing import Any, Optional, Union

from langchain_core.language_models import BaseChatModel, BaseLLM
from langchain_core.language_models.base import BaseLanguageModel

# 전역 LLM 모델 인스턴스
# 직접 주입할 모델 인스턴스를 여기에 할당하세요
llm_model: Optional[Union[BaseChatModel, BaseLLM]] = None


def initialize_llm_model(model: Union[BaseChatModel, BaseLLM]) -> None:
    """LLM 모델 초기화.

    Args:
        model: 초기화할 LLM 모델 인스턴스 (BaseChatModel 또는 BaseLLM).
    """
    global llm_model
    llm_model = model


def get_llm_model() -> Optional[Union[BaseChatModel, BaseLLM]]:
    """LLM 모델 인스턴스 가져오기.

    Returns:
        LLM 모델 인스턴스. 초기화되지 않은 경우 None.
    """
    return llm_model


def reset_llm_model() -> None:
    """LLM 모델 리셋."""
    global llm_model
    llm_model = None
