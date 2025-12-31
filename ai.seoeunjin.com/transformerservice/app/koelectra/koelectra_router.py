"""
KoELECTRA 감성 분석 라우터
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

from .koelectra_service import KoELECTRAService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/koelectra", tags=["koelectra"])

# 서비스 인스턴스 (싱글톤)
_koelectra_service = None


def get_koelectra_service() -> KoELECTRAService:
    """KoELECTRA 서비스 인스턴스 반환 (의존성 주입)"""
    global _koelectra_service
    if _koelectra_service is None:
        _koelectra_service = KoELECTRAService()
        # 서비스 시작 시 모델 로드
        try:
            _koelectra_service.load_model()
        except FileNotFoundError as e:
            logger.error(f"모델 파일을 찾을 수 없습니다: {str(e)}")
            raise HTTPException(
                status_code=503, 
                detail="모델 파일이 없습니다. 모델을 다운로드하거나 모델 경로를 확인하세요. download_model.py를 실행하여 모델을 다운로드할 수 있습니다."
            )
        except Exception as e:
            logger.error(f"모델 로딩 실패: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"모델 로딩 실패: {str(e)}. 모델 파일이 손상되었거나 불완전할 수 있습니다."
            )
    return _koelectra_service


# 요청/응답 모델
class SentimentRequest(BaseModel):
    """감성 분석 요청 모델"""
    text: str = Field(..., description="분석할 텍스트", min_length=1, max_length=2000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "이 영화 정말 재미있었어요! 강력 추천합니다."
            }
        }


class BatchSentimentRequest(BaseModel):
    """배치 감성 분석 요청 모델"""
    texts: List[str] = Field(..., description="분석할 텍스트 리스트", min_items=1, max_items=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": [
                    "정말 최고의 영화예요!",
                    "별로 재미없었습니다."
                ]
            }
        }


class SentimentResponse(BaseModel):
    """감성 분석 응답 모델"""
    text: str
    sentiment: str
    confidence: dict
    score: float


class BatchSentimentResponse(BaseModel):
    """배치 감성 분석 응답 모델"""
    results: List[SentimentResponse]
    total: int


@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(
    request: SentimentRequest,
    service: KoELECTRAService = Depends(get_koelectra_service)
):
    """
    단일 텍스트의 감성 분석
    
    - **text**: 분석할 텍스트 (최대 2000자)
    
    Returns:
        감성 분석 결과 (positive/negative, 신뢰도 점수 포함)
    """
    try:
        result = service.analyze_sentiment(request.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"감성 분석 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"감성 분석 중 오류 발생: {str(e)}")


@router.post("/sentiment/batch", response_model=BatchSentimentResponse)
async def analyze_sentiment_batch(
    request: BatchSentimentRequest,
    service: KoELECTRAService = Depends(get_koelectra_service)
):
    """
    여러 텍스트의 배치 감성 분석
    
    - **texts**: 분석할 텍스트 리스트 (최대 100개)
    
    Returns:
        배치 감성 분석 결과 리스트
    """
    try:
        result = service.analyze_sentiment_batch(request.texts)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"배치 감성 분석 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"배치 감성 분석 중 오류 발생: {str(e)}")


@router.get("/model/info")
async def get_model_info(
    service: KoELECTRAService = Depends(get_koelectra_service)
):
    """
    모델 정보 조회
    
    Returns:
        모델 상태 및 정보
    """
    try:
        info = service.get_model_info()
        return info
    except Exception as e:
        logger.error(f"모델 정보 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"모델 정보 조회 중 오류 발생: {str(e)}")


@router.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "koelectra"}
