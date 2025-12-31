"""애플리케이션 설정."""

import os
from pathlib import Path
from typing import Optional

# .env 파일 로드 (python-dotenv는 uvicorn[standard]에 포함됨)
try:
    from dotenv import load_dotenv

    # .env 파일 찾기 (여러 경로 확인)
    possible_paths = [
        Path(__file__).parent.parent.parent.parent / ".env",  # 프로젝트 루트
        Path(__file__).parent.parent.parent / ".env",  # backend 디렉토리
        Path("/home/ubuntu/rag-app/.env"),  # EC2 배포 경로
        Path("/opt/rag-app/.env"),  # 대체 배포 경로
    ]

    env_loaded = False
    for env_path in possible_paths:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"✅ .env 파일 로드됨: {env_path}")
            env_loaded = True
            break

    if not env_loaded:
        print("⚠️  .env 파일을 찾을 수 없습니다. 환경 변수를 직접 사용합니다.")
except ImportError:
    # python-dotenv가 없는 경우 무시 (환경 변수 직접 사용)
    pass


class Settings:
    """애플리케이션 설정 클래스."""

    # Neon PostgreSQL 연결 문자열 (우선순위 높음)
    POSTGRES_CONNECTION_STRING: Optional[str] = os.getenv("POSTGRES_CONNECTION_STRING")

    # 개별 PostgreSQL 설정 (POSTGRES_CONNECTION_STRING이 없을 때 사용)
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "langchain")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "langchain123")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "langchain_db")

    # Vector Store 설정
    COLLECTION_NAME: str = "langchain_collection"

    # OpenAI 설정
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    @property
    def connection_string(self) -> str:
        """PostgreSQL 연결 문자열 생성.

        POSTGRES_CONNECTION_STRING이 설정되어 있으면 그것을 사용하고,
        없으면 개별 설정으로부터 연결 문자열을 생성합니다.
        """
        if self.POSTGRES_CONNECTION_STRING:
            # Windows 환경에서 인코딩 문제 해결
            conn_str = self.POSTGRES_CONNECTION_STRING
            # bytes인 경우 UTF-8로 디코딩
            if isinstance(conn_str, bytes):
                conn_str = conn_str.decode("utf-8", errors="replace")
            # 문자열로 변환하여 반환
            return str(conn_str)

        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
