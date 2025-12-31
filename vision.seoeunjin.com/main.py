"""
메인 FastAPI 애플리케이션
- 파일 업로드 API
- CORS 설정 (Next.js 연동)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# 라우터 import
from app.api.routes.upload import router as upload_router

# FastAPI 앱 생성
app = FastAPI(
    title="CV API Server",
    description="Computer Vision 관련 API 서버 (파일 업로드, 이미지 처리 등)",
    version="1.0.0",
)

# CORS 설정 (Next.js와 통신용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js 기본 포트
        "http://localhost:3001",  # 추가 포트
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드된 파일 정적 서빙 (__file__ 기준 절대경로)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "app" / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# 라우터 등록
app.include_router(upload_router, prefix="/api", tags=["upload"])


# Health check 엔드포인트
@app.get("/")
async def root():
    return {"message": "CV API Server is running", "docs": "/docs", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
