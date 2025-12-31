from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from datetime import datetime
from typing import List

router = APIRouter()

# 업로드 파일 저장 경로 (__file__ 기준 절대경로로 고정)
# 어떤 위치에서 실행해도 backend/app/data/uploads로 저장됨
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # app/api/routes -> app
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".doc", ".docx"}

# 최대 파일 크기 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    파일 업로드 엔드포인트
    - 파일을 app/data/uploads/ 디렉토리에 저장
    - 파일명에 타임스탬프 추가하여 중복 방지
    """
    try:
        # 파일 확장자 검증
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 파일 형식입니다. 허용: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # 파일 크기 검증
        file.file.seek(0, 2)  # 파일 끝으로 이동
        file_size = file.file.tell()  # 현재 위치 = 파일 크기
        file.file.seek(0)  # 파일 처음으로 되돌리기

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"파일 크기가 너무 큽니다. 최대 {MAX_FILE_SIZE / (1024 * 1024):.0f}MB",
            )

        # 파일명 안전하게 처리 (타임스탬프 추가)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = Path(file.filename).stem  # 확장자 제외한 파일명
        filename = f"{timestamp}_{safe_filename}{ext}"
        file_path = UPLOAD_DIR / filename

        # 파일 저장
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "success": True,
            "filename": filename,
            "original_filename": file.filename,
            "path": str(file_path),
            "size": file_size,
            "size_mb": round(file_size / (1024 * 1024), 2),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"업로드 실패: {str(e)}")
    finally:
        file.file.close()


@router.get("/files")
async def list_files():
    """
    업로드된 파일 목록 조회
    """
    files = []
    try:
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append(
                    {
                        "filename": file_path.name,
                        "size": stat.st_size,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }
                )

        # 최신순으로 정렬
        files.sort(key=lambda x: x["created"], reverse=True)

        return {"success": True, "count": len(files), "files": files}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 목록 조회 실패: {str(e)}")


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """
    업로드된 파일 삭제
    """
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다")

        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="유효하지 않은 파일입니다")

        file_path.unlink()

        return {"success": True, "message": f"파일 '{filename}'이(가) 삭제되었습니다"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 삭제 실패: {str(e)}")
