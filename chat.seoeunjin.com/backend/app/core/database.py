"""데이터베이스 연결 및 초기화."""

from typing import Optional

from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from backend.app.core.config import settings


def check_postgres_connection() -> None:
    """PostgreSQL 연결 확인."""
    try:
        import psycopg2

        conn_str = settings.connection_string
        # 문자열로 명시적 변환 (Windows 인코딩 문제 해결)
        if isinstance(conn_str, bytes):
            conn_str = conn_str.decode("utf-8", errors="replace")
        conn_str = str(conn_str)

        conn = psycopg2.connect(conn_str)
        conn.close()
        print("✅ PostgreSQL 연결 확인 완료")
    except Exception as e:
        print(f"⚠️  PostgreSQL 연결 확인 실패: {e}")
        # Neon PostgreSQL은 클라우드 서비스이므로 연결 실패 시에도 계속 진행
        # (네트워크 문제일 수 있음)


def initialize_embeddings() -> Embeddings:
    """Embedding 모델 초기화."""
    from langchain_core.embeddings import FakeEmbeddings

    if settings.OPENAI_API_KEY:
        try:
            from langchain_openai import OpenAIEmbeddings

            return OpenAIEmbeddings()
        except ImportError:
            return FakeEmbeddings(size=1536)
    else:
        return FakeEmbeddings(size=1536)


def initialize_vector_store() -> Optional[PGVector]:
    """PGVector 스토어 초기화."""
    try:
        embeddings = initialize_embeddings()

        # Vector store 연결
        print("📦 PostgreSQL 연결 문자열 확인 중...")
        conn_str = settings.connection_string

        # 연결 문자열이 비어있거나 기본값인지 확인
        if not conn_str or conn_str.strip() == "":
            raise ValueError(
                "PostgreSQL 연결 문자열이 설정되지 않았습니다. POSTGRES_CONNECTION_STRING 환경 변수를 확인하세요."
            )

        # 기본 localhost 연결 문자열인지 확인
        if "localhost" in conn_str or "127.0.0.1" in conn_str:
            print("⚠️  경고: localhost 연결 문자열이 감지되었습니다.")
            print("   POSTGRES_CONNECTION_STRING이 설정되지 않았을 수 있습니다.")
            print("   GitHub Secrets에서 POSTGRES_CONNECTION_STRING을 확인하세요.")

        # 연결 문자열에서 비밀번호 부분을 마스킹하여 로그 출력
        masked_conn_str = conn_str
        if "@" in conn_str and ":" in conn_str:
            try:
                # postgresql://user:password@host:port/db 형식에서 password 마스킹
                parts = conn_str.split("@")
                if len(parts) == 2:
                    auth_part = parts[0]
                    if "://" in auth_part:
                        protocol_user = auth_part.split("://")[1]
                        if ":" in protocol_user:
                            user = protocol_user.split(":")[0]
                            masked_conn_str = (
                                f"{conn_str.split('://')[0]}://{user}:***@{parts[1]}"
                            )
            except Exception:
                pass  # 마스킹 실패 시 원본 사용

        print(f"📦 연결 문자열: {masked_conn_str}")

        vector_store = PGVector(
            embedding_function=embeddings,
            collection_name=settings.COLLECTION_NAME,
            connection_string=conn_str,
        )
        print("✅ PGVector 초기화 완료")

        # 초기 문서가 있는지 확인 (문서 수가 0이면 초기 문서 추가)
        try:
            existing_docs = vector_store.similarity_search("", k=1)
            if len(existing_docs) == 0:
                # 초기 문서 추가
                initial_docs = [
                    Document(
                        page_content="안녕하세요! 이것은 LangChain과 pgvector의 Hello World 예제입니다.",
                        metadata={"source": "hello_world", "type": "greeting"},
                    ),
                    Document(
                        page_content="LangChain은 LLM 애플리케이션을 구축하기 위한 프레임워크입니다.",
                        metadata={"source": "langchain_info", "type": "info"},
                    ),
                    Document(
                        page_content="pgvector는 PostgreSQL에서 벡터 유사도 검색을 가능하게 하는 확장입니다.",
                        metadata={"source": "pgvector_info", "type": "info"},
                    ),
                ]
                vector_store.add_documents(initial_docs)
                print("✅ 초기 문서 추가 완료")
            else:
                print("✅ 기존 문서 발견")
        except Exception as e:
            # 에러가 발생해도 계속 진행 (문서 추가는 선택사항)
            print(f"⚠️  초기 문서 추가 중 오류 (무시됨): {e}")

        return vector_store
    except Exception as e:
        print(f"❌ PGVector 초기화 실패: {e}")
        print("⚠️  Vector Store 기능은 사용할 수 없습니다.")
        print("   PostgreSQL 연결을 확인하세요:")
        print("   - POSTGRES_CONNECTION_STRING 환경 변수 확인")
        print(
            "   - 또는 POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB 확인"
        )
        # 연결 실패 시에도 애플리케이션은 시작할 수 있도록 None 반환
        return None
