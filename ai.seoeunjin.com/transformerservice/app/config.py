"""
Transformer Service 설정
"""
from pydantic_settings import BaseSettings
from typing import Optional


class TransformerServiceConfig(BaseSettings):
    """Transformer 서비스 설정"""
    service_name: str = "Transformer Service"
    service_version: str = "1.0.0"
    port: int = 9000
    debug: bool = False
    
    # 모델 설정
    model_path: Optional[str] = None  # 로컬 모델 경로 (기본값: app/koelectra/koelectra_model)
    use_gpu: bool = False  # GPU 사용 여부
    
    class Config:
        env_file = ".env"
        case_sensitive = False
