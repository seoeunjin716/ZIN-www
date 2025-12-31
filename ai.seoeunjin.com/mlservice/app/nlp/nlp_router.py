from __future__ import annotations

import pathlib
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from .emma.emma_wordcloud import EmmaWordCloud
from .samsung.samsung_wordcloud import SamsungWordCloud

router = APIRouter(prefix="/nlp", tags=["nlp"])

DEFAULT_SAVE = (
    pathlib.Path(__file__).resolve().parent / "save" / "emma_wordcloud.png"
)

DEFAULT_SAVE_SAMSUNG = (
    pathlib.Path(__file__).resolve().parent / "save" / "samsung_wordcloud.png"
)


@router.get("/emma")
def generate_emma_wordcloud(
    save: Optional[str] = Query(
        None, description="이미지 저장 경로 (기본: app/nlp/save/emma_wordcloud.png)"
    ),
    font_path: Optional[str] = Query(
        None, description="워드클라우드에 사용할 폰트 파일 경로 (옵션)"
    ),
) -> dict:
    """
    Generate an Emma word cloud and save it to the provided path (or default).
    """
    try:
        target_path = pathlib.Path(save) if save else DEFAULT_SAVE
        generator = EmmaWordCloud(font_path=font_path)
        output = generator.generate(str(target_path))
        return {"saved": str(output.resolve())}
    except Exception as exc:  # pragma: no cover - defensive
        import traceback
        error_detail = f"{str(exc)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/samsung")
def generate_samsung_wordcloud(
    save: Optional[str] = Query(
        None, description="이미지 저장 경로 (기본: app/nlp/save/samsung_wordcloud.png)"
    ),
) -> dict:
    """
    Generate a Samsung word cloud from Korean text and save it to the provided path (or default).
    워드클라우드는 app/nlp/save 폴더에 저장됩니다.
    """
    try:
        # save 파라미터가 제공되면 사용하고, 없으면 기본 경로 사용
        target_path = str(pathlib.Path(save)) if save else str(DEFAULT_SAVE_SAMSUNG)
        
        generator = SamsungWordCloud(quiet=True)
        
        # 워드클라우드 생성 및 저장 (emma와 동일한 방식)
        output = generator.save_wordcloud(output_path=target_path)
        
        return {"saved": str(output.resolve())}
    except Exception as exc:  # pragma: no cover - defensive
        import traceback
        error_detail = f"{str(exc)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)
