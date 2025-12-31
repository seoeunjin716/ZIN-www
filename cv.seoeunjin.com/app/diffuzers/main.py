# FastAPI 엔트리 + 정적 파일 서빙(/outputs/...)
# + 라우팅 등록입니다.
import sys
from pathlib import Path

# app 폴더를 Python 경로에 추가 (uvicorn multiprocessing 이슈 해결)
app_dir = Path(__file__).resolve().parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from diffuzers.api.v1.routes.generate import router as generate_router
from diffuzers.core.config import OUTPUTS_DIR

app = FastAPI(title="Diffusers API", version="1.0.0")

# outputs 디렉토리 생성 (없으면 생성)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# outputs 정적 서빙 (로컬 개발/단독 서버에서 편리)
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")

app.include_router(generate_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"ok": True}
