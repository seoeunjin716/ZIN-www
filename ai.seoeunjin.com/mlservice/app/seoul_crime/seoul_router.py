"""
seoul ML Service 라우터
"""
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional

from .seoul_service import SeoulService

# 서비스 인스턴스 생성
seoul_service = SeoulService()


router = APIRouter(
    prefix="/seoul",
    tags=["seoul ML"]
)


@router.get("")
async def seoul_preprocess():
    """
    seoul 데이터 전처리 로그 조회
    
    Returns:
        전처리 완료 메시지 (로그는 터미널에 ic()로 출력됨)
    """
    try:
        seoul_service.preprocess()
        return {
            "status": "success",
            "message": "전처리 완료 - 로그는 서버 터미널에서 확인하세요"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전처리 중 오류 발생: {str(e)}")


@router.get("/preprocess")
async def preprocess_data():
    """
    데이터 전처리 정보 조회 (GET)
    
    Returns:
        Train과 Test 데이터의 전처리 정보 (타입, 컬럼, 샘플 데이터, null 개수 등)
    """
    try:
        result = seoul_service.preprocess()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전처리 중 오류 발생: {str(e)}")


@router.post("/preprocess")
async def preprocess_data_post():
    """
    데이터 전처리 및 파일 저장 (POST)
    
    POST 요청 시 crime 데이터에 주소와 자치구 컬럼을 추가하여 save 폴더에 저장합니다.
    
    Returns:
        전처리 결과 및 저장된 파일 정보
    """
    try:
        result = seoul_service.preprocess()
        # preprocess() 메서드 내부에서 이미 파일이 저장됨
        return {
            **result,
            "message": "전처리 완료 및 crime_with_address.csv 파일이 save 폴더에 저장되었습니다.",
            "saved_file": "crime_with_address.csv",
            "save_path": str(Path(seoul_service.data.sname) / "crime_with_address.csv")
        }
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
        "model_trained": seoul_service.model is not None,
        "available_endpoints": [
            "/seoul/predict",
            "/seoul/train",
            "/seoul/preprocess",
            "/seoul/analyze",
            "/seoul/feature-importance",
            "/seoul/cross-validate",
            "/seoul/status"
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
        seoul_service.preprocess()
        
        # 2. 모델링
        seoul_service.modeling()
        
        # 3. 학습
        seoul_service.learning()
        
        # 4. 평가
        results = seoul_service.evaluation()
        
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
        if not seoul_service.models:
            seoul_service.preprocess()
            seoul_service.modeling()
            seoul_service.learning()
            seoul_service.evaluation()
        
        # submission.csv 생성
        submission_path = seoul_service.submit(model_name=model_name)
        
        # 사용된 모델 이름 확인 (가장 좋은 모델이 자동 선택되었을 수 있음)
        actual_model = model_name or seoul_service.best_model_name or "random_forest"
        
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
            "model_accuracy": seoul_service.model_scores.get(actual_model) if actual_model in seoul_service.model_scores else None
        }
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=f"제출 파일 생성 중 오류 발생: {error_detail}")


@router.get("/files")
async def list_data_files():
    """
    data 폴더의 파일 목록 조회
    
    Returns:
        파일 목록과 각 파일의 메타데이터
    """
    try:
        files = [
            {
                "name": "cctv",
                "filename": "cctv.csv",
                "type": "csv",
                "description": "CCTV 설치 현황 데이터"
            },
            {
                "name": "crime",
                "filename": "crime.csv",
                "type": "csv",
                "description": "서울시 범죄 발생 및 검거 현황 데이터"
            },
            {
                "name": "pop",
                "filename": "pop.xls",
                "type": "excel",
                "description": "서울시 자치구별 인구 데이터"
            }
        ]
        
        return {
            "status": "success",
            "files": files,
            "total_count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 목록 조회 중 오류 발생: {str(e)}")


@router.get("/files/{file_name}")
async def get_data_file(file_name: str):
    """
    특정 데이터 파일 조회
    
    Args:
        file_name: cctv, crime, pop 중 하나
    
    Returns:
        해당 파일의 데이터 (JSON)
    """
    try:
        result = seoul_service.get_data_as_json(file_name)
        return {
            "status": "success",
            "file_name": file_name,
            **result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 조회 중 오류 발생: {str(e)}")


@router.get("/load")
async def load_all_data():
    """
    모든 데이터 파일을 한번에 조회
    
    Returns:
        CCTV, Crime, Population 데이터 전체
    """
    try:
        print("\n" + "="*50)
        print("=== 모든 데이터 로드 시작 ===")
        print("="*50)
        
        cctv_result = seoul_service.get_data_as_json('cctv')
        crime_result = seoul_service.get_data_as_json('crime')
        pop_result = seoul_service.get_data_as_json('pop')
        
        print("\n" + "="*50)
        print("=== 모든 데이터 로드 완료 ===")
        print("="*50)
        
        return {
            "status": "success",
            "cctv": {
                "file_name": "cctv",
                **cctv_result
            },
            "crime": {
                "file_name": "crime",
                **crime_result
            },
            "pop": {
                "file_name": "pop",
                **pop_result
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 로드 중 오류 발생: {str(e)}")


@router.get("/merged")
async def get_merged_data():
    """
    CCTV-POP 머지된 데이터 조회
    
    Returns:
        머지된 데이터
    """
    try:
        result = seoul_service.get_data_as_json('cctv_pop')
        return {
            "status": "success",
            "file_name": "cctv_pop",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"머지 데이터 조회 중 오류 발생: {str(e)}")


@router.get("/save/crime")
async def save_crime_with_address(filename: Optional[str] = Query(None, description="저장할 파일명 (기본값: crime_with_address.csv)")):
    """
    crime.csv에 주소와 자치구 컬럼을 추가하여 save 폴더에 CSV 파일로 저장
    
    Args:
        filename: 저장할 파일명 (선택사항, 기본값: crime_with_address.csv)
    
    Returns:
        저장 결과 및 파일 경로
    """
    try:
        output_filename = filename if filename else "crime_with_address.csv"
        file_path = seoul_service.save_crime_with_address(output_filename)
        return {
            "status": "success",
            "message": "Crime 데이터에 주소와 자치구 컬럼이 추가되어 저장되었습니다.",
            "file_path": file_path,
            "filename": output_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 저장 중 오류 발생: {str(e)}")


@router.get("/save/police-stations")
async def save_police_stations_info(filename: Optional[str] = Query(None, description="저장할 파일명 (기본값: police_stations.csv)")):
    """
    서울시 경찰서와 파출소 정보를 카카오맵 API로 검색하여 save 폴더에 CSV 파일로 저장
    
    Args:
        filename: 저장할 파일명 (선택사항, 기본값: police_stations.csv)
    
    Returns:
        저장 결과 및 파일 경로
    """
    try:
        output_filename = filename if filename else "police_stations.csv"
        file_path = seoul_service.save_police_stations_info(output_filename)
        return {
            "status": "success",
            "message": "서울시 경찰서/파출소 정보가 저장되었습니다.",
            "file_path": file_path,
            "filename": output_filename,
            "columns": ["경찰서이름", "경찰서주소", "관서"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"경찰서 정보 수집 중 오류 발생: {str(e)}")


@router.post("/save/police-stations")
async def save_police_stations_info_post(filename: Optional[str] = Query(None, description="저장할 파일명 (기본값: police_stations.csv)")):
    """
    서울시 경찰서와 파출소 정보를 카카오맵 API로 검색하여 save 폴더에 CSV 파일로 저장 (POST)
    
    Args:
        filename: 저장할 파일명 (선택사항, 기본값: police_stations.csv)
    
    Returns:
        저장 결과 및 파일 경로
    """
    try:
        output_filename = filename if filename else "police_stations.csv"
        file_path = seoul_service.save_police_stations_info(output_filename)
        return {
            "status": "success",
            "message": "서울시 경찰서/파출소 정보가 저장되었습니다.",
            "file_path": file_path,
            "filename": output_filename,
            "columns": ["경찰서이름", "경찰서주소", "관서"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"경찰서 정보 수집 중 오류 발생: {str(e)}")