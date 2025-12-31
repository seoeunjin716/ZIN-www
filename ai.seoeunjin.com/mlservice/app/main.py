"""
ML Service - FastAPI 애플리케이션
"""
import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import MLServiceConfig
from app.titanic import router as titanic_router  # titanic 패키지에서 router 임포트
from app.seoul_crime import router as seoul_router  # seoul_crime 패키지에서 router 임포트
from app.us_unemployment import router as usa_router  # us_unemployment 패키지에서 router 임포트
from app.nlp import nlp_router as nlp_router  # nlp 라우터
from common.middleware import LoggingMiddleware
from common.utils import setup_logging

# 설정 로드
config = MLServiceConfig()

# 로깅 설정
logger = setup_logging(config.service_name)

# FastAPI 앱 생성
app = FastAPI(
    title="ML Service API",
    description="머신러닝 서비스 API 문서 - Titanic 생존 예측",
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

# Titanic 라우터 등록
# app.titanic 모듈의 router를 FastAPI 앱에 포함
# 이제 /titanic/* 엔드포인트들이 사용 가능합니다
app.include_router(titanic_router)

# Seoul Crime 라우터 등록
# app.seoul_crime 모듈의 router를 FastAPI 앱에 포함
# 이제 /seoul/* 엔드포인트들이 사용 가능합니다
app.include_router(seoul_router)

# US Unemployment 라우터 등록
# app.us_unemployment 모듈의 router를 FastAPI 앱에 포함
# 이제 /usa/* 엔드포인트들이 사용 가능합니다
app.include_router(usa_router)

# NLP 라우터 등록
app.include_router(nlp_router.router)

# /api/ml prefix를 가진 라우터 그룹 생성 (Gateway 경로와 일치)
from fastapi import APIRouter
api_ml_router = APIRouter(prefix="/api/ml", tags=["ml"])

# Samsung 워드클라우드 엔드포인트 (직접 접근용)
@api_ml_router.get("/samsung")
async def generate_samsung_wordcloud_direct(
    save: Optional[str] = Query(
        None, description="이미지 저장 경로 (기본: app/nlp/save/samsung_wordcloud.png)"
    ),
):
    """
    Generate a Samsung word cloud from Korean text and save it to the save folder.
    /api/ml/samsung 경로로 접근 가능합니다.
    """
    from app.nlp.samsung.samsung_wordcloud import SamsungWordCloud
    import pathlib
    
    try:
        # save 파라미터가 제공되면 사용하고, 없으면 기본 경로 사용
        DEFAULT_SAVE_SAMSUNG = (
            pathlib.Path(__file__).parent / "nlp" / "save" / "samsung_wordcloud.png"
        )
        target_path = str(pathlib.Path(save)) if save else str(DEFAULT_SAVE_SAMSUNG)
        
        generator = SamsungWordCloud(quiet=True)
        
        # 워드클라우드 생성 및 저장
        output = generator.save_wordcloud(output_path=target_path)
        
        return {"saved": str(output.resolve())}
    except Exception as exc:
        import traceback
        error_detail = f"{str(exc)}\n{traceback.format_exc()}"
        logger.error(f"Samsung wordcloud error: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

# /api/ml 라우터 등록
app.include_router(api_ml_router)

# Samsung 워드클라우드 엔드포인트 (기존 경로 유지)
@app.get("/samsung")
async def generate_samsung_wordcloud_direct_legacy(
    save: Optional[str] = Query(
        None, description="이미지 저장 경로 (기본: app/nlp/save/samsung_wordcloud.png)"
    ),
):
    """
    Generate a Samsung word cloud from Korean text and save it to the save folder.
    /samsung 경로로 접근 가능합니다 (레거시 지원).
    """
    from app.nlp.samsung.samsung_wordcloud import SamsungWordCloud
    import pathlib
    
    try:
        # save 파라미터가 제공되면 사용하고, 없으면 기본 경로 사용
        DEFAULT_SAVE_SAMSUNG = (
            pathlib.Path(__file__).parent / "nlp" / "save" / "samsung_wordcloud.png"
        )
        target_path = str(pathlib.Path(save)) if save else str(DEFAULT_SAVE_SAMSUNG)
        
        generator = SamsungWordCloud(quiet=True)
        
        # 워드클라우드 생성 및 저장
        output = generator.save_wordcloud(output_path=target_path)
        
        return {"saved": str(output.resolve())}
    except Exception as exc:
        import traceback
        error_detail = f"{str(exc)}\n{traceback.format_exc()}"
        logger.error(f"Samsung wordcloud error: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": config.service_name,
        "version": config.service_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """서비스 시작 시 실행"""
    logger.info(f"{config.service_name} v{config.service_version} started on port {config.port}")


@app.on_event("shutdown")
async def shutdown_event():
    """서비스 종료 시 실행"""
    logger.info(f"{config.service_name} shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.port)
