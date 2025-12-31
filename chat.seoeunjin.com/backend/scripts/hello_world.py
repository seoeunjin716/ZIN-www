"""LangChain과 pgvector를 연동하는 Hello World 예제."""

import os
import time
from typing import List

from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document

# 환경 변수에서 데이터베이스 연결 정보 가져오기
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "langchain")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "langchain123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "langchain_db")

# 연결 문자열 생성
CONNECTION_STRING = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

COLLECTION_NAME = "langchain_collection"


def wait_for_postgres(max_retries: int = 30, delay: int = 2) -> None:
    """PostgreSQL이 준비될 때까지 대기."""
    import psycopg2

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DB,
            )
            conn.close()
            print("✅ PostgreSQL 연결 성공!")
            return
        except Exception as e:
            print(f"⏳ PostgreSQL 대기 중... ({i+1}/{max_retries}) - {e}")
            time.sleep(delay)
    raise Exception("PostgreSQL 연결 실패")
    raise Exception("PostgreSQL 연결 실패")


def main() -> None:
    """메인 함수."""
    print("🚀 LangChain + pgvector Hello World 시작!")
    print("-" * 50)

    # PostgreSQL 연결 대기
    wait_for_postgres()

    # Embedding 모델 초기화 (OpenAI 대신 간단한 모델 사용)
    # 실제 사용 시에는 OpenAI API 키가 필요하지만,
    # 여기서는 FakeEmbeddings를 사용하여 예제를 완성합니다
    from langchain_core.embeddings import FakeEmbeddings

    # OpenAI API 키가 있으면 OpenAIEmbeddings 사용, 없으면 FakeEmbeddings 사용
    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import OpenAIEmbeddings

            embeddings = OpenAIEmbeddings()
            print("✅ OpenAI Embeddings 사용")
        except ImportError:
            print("⚠️  langchain-openai가 설치되지 않아 FakeEmbeddings를 사용합니다.")
            embeddings = FakeEmbeddings(size=1536)
    else:
        print("⚠️  OpenAI API 키가 없어 FakeEmbeddings를 사용합니다.")
        embeddings = FakeEmbeddings(size=1536)

    print("✅ Embedding 모델 초기화 완료")

    # PGVector 스토어 생성
    try:
        vector_store = PGVector.from_documents(
            documents=[
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
            ],
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            connection_string=CONNECTION_STRING,
        )
        print("✅ 문서를 pgvector에 저장 완료")
    except Exception as e:
        print(f"❌ PGVector 초기화 오류: {e}")
        # 기존 컬렉션이 있을 수 있으므로 다시 시도
        vector_store = PGVector(
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
            connection_string=CONNECTION_STRING,
        )
        print("✅ 기존 PGVector 스토어 연결 완료")

    # 유사도 검색 테스트
    print("\n🔍 유사도 검색 테스트:")
    print("-" * 50)

    query = "LangChain이란 무엇인가요?"
    print(f"검색 쿼리: '{query}'")

    results: List[Document] = vector_store.similarity_search(query, k=2)

    print(f"\n📄 검색 결과 ({len(results)}개):")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.page_content}")
        print(f"   메타데이터: {doc.metadata}")

    # 점수와 함께 검색
    print("\n📊 점수와 함께 검색:")
    print("-" * 50)

    results_with_score = vector_store.similarity_search_with_score(query, k=2)

    for i, (doc, score) in enumerate(results_with_score, 1):
        print(f"\n{i}. [유사도: {score:.4f}] {doc.page_content}")

    print("\n" + "=" * 50)
    print("✅ Hello World 예제 완료!")
    print("=" * 50)


if __name__ == "__main__":
    main()

