"""
Transformer Service - FastAPI 애플리케이션
"""
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import TransformerServiceConfig
from app.koelectra import koelectra_router
from common.middleware import LoggingMiddleware
from common.utils import setup_logging

# 설정 로드
config = TransformerServiceConfig()

# 로깅 설정
logger = setup_logging(config.service_name)

# FastAPI 앱 생성
app = FastAPI(
    title="Transformer Service API",
    description="Transformer 기반 감성 분석 서비스 API 문서",
    version=config.service_version
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 미들웨어 추가
app.add_middleware(LoggingMiddleware)

# 라우터 등록
app.include_router(koelectra_router.router)


@app.on_event("startup")
async def startup_event():
    """서비스 시작 시 실행"""
    logger.info(f"{config.service_name} v{config.service_version} started")
    # KoELECTRA 모델 사전 로드
    try:
        from app.koelectra.koelectra_service import KoELECTRAService
        service = KoELECTRAService()
        service.load_model()
        logger.info("KoELECTRA 모델 로딩 완료")
    except Exception as e:
        logger.error(f"KoELECTRA 모델 로딩 실패: {str(e)}")
        # 모델 로딩 실패해도 서비스는 시작 (첫 요청 시 재시도)


@app.on_event("shutdown")
async def shutdown_event():
    """서비스 종료 시 실행"""
    logger.info(f"{config.service_name} shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.port)

