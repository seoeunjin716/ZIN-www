"""백엔드 서버 실행 스크립트."""

import os
import sys
from pathlib import Path

import uvicorn

if __name__ == "__main__":
    # 현재 스크립트의 디렉토리
    current_dir = Path(__file__).parent.absolute()
    # 프로젝트 루트 디렉토리 (backend의 부모 디렉토리)
    project_root = current_dir.parent.absolute()

    # 프로젝트 루트를 Python 경로에 추가
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # 작업 디렉토리를 프로젝트 루트로 변경
    os.chdir(project_root)

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
