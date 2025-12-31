"""
ML Service 설정
"""
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class MLServiceConfig(BaseSettings):
    """ML 서비스 설정"""
    
    service_name: str = "ML Service"
    service_version: str = "1.0.0"
    port: int = 8080
    
    # 데이터베이스 설정 (필요시)
    database_url: str = ""
    db_host: str = ""
    db_port: Optional[int] = 5432
    db_name: str = ""
    db_user: str = ""
    db_password: str = ""
    
    # Redis 설정 (필요시)
    redis_url: str = ""
    redis_host: str = ""
    redis_port: Optional[int] = 6379
    redis_password: str = ""
    redis_ssl_enabled: bool = True
    
    @field_validator('db_port', mode='before')
    @classmethod
    def parse_db_port(cls, v):
        """빈 문자열이나 None을 기본값으로 변환"""
        if v == '' or v is None:
            return 5432
        try:
            return int(v)
        except (ValueError, TypeError):
            return 5432
    
    @field_validator('redis_port', mode='before')
    @classmethod
    def parse_redis_port(cls, v):
        """빈 문자열이나 None을 기본값으로 변환"""
        if v == '' or v is None:
            return 6379
        try:
            return int(v)
        except (ValueError, TypeError):
            return 6379
    
    class Config:
        env_file = ".env"
        case_sensitive = False

