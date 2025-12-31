"""로컬 HuggingFace 모델 로더."""

import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    # 타입 힌트를 위한 더미 타입
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore

# device_map 사용 시 accelerate 필요
try:
    import accelerate

    ACCELERATE_AVAILABLE = True
except ImportError:
    ACCELERATE_AVAILABLE = False


def load_midm_model(
    model_path: Optional[str] = None,
    torch_dtype: Optional[str] = None,
    device_map: str = "auto",
    trust_remote_code: bool = True,
) -> Tuple["AutoModelForCausalLM", "AutoTokenizer"]:
    """Midm 모델을 로컬 경로에서 로드.

    Args:
        model_path: 모델 경로. None이면 기본 경로 사용.
        torch_dtype: torch dtype (기본값: None, "auto" 사용 시 None).
        device_map: 디바이스 맵핑 (기본값: "auto").
        trust_remote_code: 원격 코드 신뢰 여부 (기본값: True).

    Returns:
        (model, tokenizer) 튜플.
    """
    if model_path is None:
        # 기본 경로: backend/app/models/midm
        current_dir = Path(__file__).parent
        model_path = str(current_dir.parent / "models" / "midm")

    # 경로 확인
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 경로를 찾을 수 없습니다: {model_path}")

    print(f"📦 모델 로딩 중: {model_path}")

    # accelerate 확인 (device_map 사용 시 필요)
    if device_map and device_map != "cpu" and not ACCELERATE_AVAILABLE:
        raise ImportError(
            "device_map을 사용하려면 accelerate가 필요합니다. "
            "`pip install accelerate`를 실행하세요."
        )

    # 모델 로드 파라미터 준비
    load_kwargs = {
        "trust_remote_code": trust_remote_code,
    }

    # device_map 설정
    if device_map:
        load_kwargs["device_map"] = device_map

    # dtype 설정 (torch_dtype 대신 dtype 사용)
    if torch_dtype and torch_dtype != "auto":
        import torch

        if torch_dtype == "float16":
            load_kwargs["dtype"] = torch.float16
        elif torch_dtype == "bfloat16":
            load_kwargs["dtype"] = torch.bfloat16
        elif torch_dtype == "float32":
            load_kwargs["dtype"] = torch.float32
        # "auto"인 경우 또는 None인 경우 dtype 설정하지 않음

    # 모델 로드
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        **load_kwargs,
    )

    print("✅ 모델 로드 완료")

    # 토크나이저 로드
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    print("✅ 토크나이저 로드 완료")

    return model, tokenizer


def create_midm_pipeline(
    model_path: Optional[str] = None,
    torch_dtype: Optional[str] = None,
    device_map: str = "auto",
    trust_remote_code: bool = True,
    **pipeline_kwargs,
):
    """Midm 모델을 사용하여 HuggingFace pipeline 생성.

    Args:
        model_path: 모델 경로. None이면 기본 경로 사용.
        torch_dtype: torch dtype (기본값: "auto").
        device_map: 디바이스 맵핑 (기본값: "auto").
        trust_remote_code: 원격 코드 신뢰 여부 (기본값: True).
        **pipeline_kwargs: pipeline에 전달할 추가 인자.

    Returns:
        HuggingFace pipeline 객체.
    """
    model, tokenizer = load_midm_model(
        model_path=model_path,
        torch_dtype=torch_dtype,
        device_map=device_map,
        trust_remote_code=trust_remote_code,
    )

    # pipeline 생성
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        **pipeline_kwargs,
    )

    print("✅ Pipeline 생성 완료")

    return pipe


def load_midm_langchain_model(
    model_path: Optional[str] = None,
    torch_dtype: Optional[str] = None,
    device_map: str = "auto",
    trust_remote_code: bool = True,
    **pipeline_kwargs,
):
    """Midm 모델을 LangChain HuggingFacePipeline로 로드.

    Args:
        model_path: 모델 경로. None이면 기본 경로 사용.
        torch_dtype: torch dtype (기본값: "auto").
        device_map: 디바이스 맵핑 (기본값: "auto").
        trust_remote_code: 원격 코드 신뢰 여부 (기본값: True).
        **pipeline_kwargs: pipeline에 전달할 추가 인자.

    Returns:
        HuggingFacePipeline 인스턴스.
    """
    try:
        from langchain_huggingface import HuggingFacePipeline
    except ImportError:
        raise ImportError(
            "langchain-huggingface가 설치되지 않았습니다. "
            "`pip install langchain-huggingface`를 실행하세요."
        )

    # pipeline 생성
    pipe = create_midm_pipeline(
        model_path=model_path,
        torch_dtype=torch_dtype,
        device_map=device_map,
        trust_remote_code=trust_remote_code,
        **pipeline_kwargs,
    )

    # LangChain HuggingFacePipeline로 래핑
    llm = HuggingFacePipeline(pipeline=pipe)

    print("✅ LangChain HuggingFacePipeline 생성 완료")

    return llm
