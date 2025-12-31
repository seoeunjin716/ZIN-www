"""
US Unemployment ML Service 라우터
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

# 서비스 인스턴스는 나중에 필요시 생성
# from .service import USUnemploymentService
# us_unemployment_service = USUnemploymentService()

router = APIRouter(
    prefix="/usa",
    tags=["US Unemployment"]
)


@router.get("")
async def usa_root():
    """
    US Unemployment 서비스 루트 엔드포인트
    
    Returns:
        서비스 정보
    """
    return {
        "service": "US Unemployment ML Service",
        "status": "running",
        "description": "미국 실업률 데이터 시각화 서비스"
    }


@router.get("/health")
async def usa_health_check():
    """
    헬스 체크 엔드포인트
    
    Returns:
        헬스 상태
    """
    return {"status": "healthy"}

