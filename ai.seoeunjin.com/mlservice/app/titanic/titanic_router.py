"""
Titanic ML Service 라우터
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional

from .titanic_service import TitanicMLService

# 서비스 인스턴스 생성
titanic_service = TitanicMLService()

router = APIRouter(
    prefix="/titanic",
    tags=["Titanic ML"]
)


@router.get("")
async def titanic_preprocess():
    """
    Titanic 데이터 전처리 로그 조회
    
    Returns:
        전처리 완료 메시지 (로그는 터미널에 ic()로 출력됨)
    """
    try:
        titanic_service.preprocess()
        return {
            "status": "success",
            "message": "전처리 완료 - 로그는 서버 터미널에서 확인하세요"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전처리 중 오류 발생: {str(e)}")


@router.get("/preprocess")
async def preprocess_data():
    """
    데이터 전처리 정보 조회
    
    Returns:
        Train과 Test 데이터의 전처리 정보 (타입, 컬럼, 샘플 데이터, null 개수 등)
    """
    try:
        result = titanic_service.preprocess()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전처리 중 오류 발생: {str(e)}")


@router.get("/status")
async def get_status():
    """
    서비스 상태 확인
    
    Returns:
        서비스 상태 정보
    """
    return {
        "status": "running",
        "model_trained": titanic_service.model is not None,
        "available_endpoints": [
            "/titanic/predict",
            "/titanic/train",
            "/titanic/preprocess",
            "/titanic/analyze",
            "/titanic/feature-importance",
            "/titanic/cross-validate",
            "/titanic/status"
        ]
    }

@router.get("/evaluate")
async def evaluate_model():
    """
    모델 평가 실행
    후 모델 평가 결과 반환
    """
    try:
        # 1. 전처리
        titanic_service.preprocess()
        
        # 2. 모델링
        titanic_service.modeling()
        
        # 3. 학습
        titanic_service.learning()
        
        # 4. 평가
        results = titanic_service.evaluation()
        
        return {
            "status": "success",
            "message": "모델 평가 완료",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"평가 중 오류 발생: {str(e)}")


@router.get("/submit")
async def submit_prediction(model_name: Optional[str] = Query(None, description="사용할 모델 이름 (선택사항)")):
    """
    Kaggle 제출용 submission.csv 파일 생성
    
    Args:
        model_name: 사용할 모델 이름 (쿼리 파라미터, 선택사항)
                    None이면 random_forest 사용
                    사용 가능: logistic_regression, random_forest, naive_bayes, svm, knn
    
    Returns:
        생성된 submission.csv 파일 정보
    """
    try:
        # 모델이 학습되지 않았으면 전체 파이프라인 실행
        if not titanic_service.models:
            titanic_service.preprocess()
            titanic_service.modeling()
            titanic_service.learning()
            titanic_service.evaluation()
        
        # submission.csv 생성
        submission_path = titanic_service.submit(model_name=model_name)
        
        # 사용된 모델 이름 확인 (가장 좋은 모델이 자동 선택되었을 수 있음)
        actual_model = model_name or titanic_service.best_model_name or "random_forest"
        
        # 파일이 실제로 생성되었는지 확인
        from pathlib import Path
        file_path = Path(submission_path)
        file_exists = file_path.exists()
        
        return {
            "status": "success",
            "message": "submission.csv 파일 생성 완료",
            "file_path": submission_path,
            "file_exists": file_exists,
            "file_size": file_path.stat().st_size if file_exists else 0,
            "model_used": actual_model,
            "model_accuracy": titanic_service.model_scores.get(actual_model) if actual_model in titanic_service.model_scores else None
        }
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=f"제출 파일 생성 중 오류 발생: {error_detail}")