# Next.js → FastAPI 파일 업로드 전략

## 📋 현재 상황

- **Next.js**: `www.seoeunjin.com` (포트 3000)
- **FastAPI**: `cv.seoeunjin.com/app/diffuzers/main.py` (포트 8000)
- **목표**: Next.js에서 파일 업로드 → FastAPI의 `app/data/yolo` 폴더에 저장

---

## 🎯 권장 전략: FastAPI를 통한 파일 저장

### 이유
1. **관심사 분리**: 파일 관리는 FastAPI가 담당
2. **확장성**: 나중에 인증, 검증, 처리 로직 추가 용이
3. **일관성**: 다른 API와 동일한 패턴
4. **보안**: FastAPI에서 파일 검증 및 처리 가능

---

## 🏗️ 구현 방법

### 방법 1: FastAPI 엔드포인트 생성 (권장)

#### 1.1 FastAPI에 파일 업로드 엔드포인트 추가

**파일**: `cv.seoeunjin.com/app/diffuzers/api/v1/routes/upload.py`

```python
from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    파일을 app/data/yolo 폴더에 저장
    """
    # 저장 경로 설정
    base_dir = Path(__file__).resolve().parents[4]  # cv.seoeunjin.com
    target_dir = base_dir / "app" / "data" / "yolo"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일 저장
    file_path = target_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "success": True,
        "message": "파일이 성공적으로 저장되었습니다.",
        "fileName": file.filename,
        "path": str(file_path)
    }
```

#### 1.2 FastAPI main.py에 라우터 등록

```python
from diffuzers.api.v1.routes.upload import router as upload_router

app.include_router(upload_router, prefix="/api/v1")
```

#### 1.3 Next.js에서 FastAPI 호출

**파일**: `www.seoeunjin.com/app/portpolio/page.tsx`

```typescript
const handleSaveToPortfolio = useCallback(async (fileItem: FileItem) => {
    setSaving(fileItem.id);
    
    try {
        const formData = new FormData();
        formData.append('file', fileItem.file);

        // FastAPI로 파일 전송
        const response = await fetch('http://localhost:8000/api/v1/upload', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            alert(`✅ 포트폴리오에 추가되었습니다!\n\n파일명: ${result.fileName}`);
        } else {
            alert(`❌ 저장 실패: ${result.error || '알 수 없는 오류'}`);
        }
    } catch (error) {
        console.error('파일 저장 오류:', error);
        alert(`❌ 파일 저장 중 오류가 발생했습니다: ${error}`);
    } finally {
        setSaving(null);
    }
}, []);
```

---

### 방법 2: 현재 방식 유지 (간단하지만 권장하지 않음)

**현재**: Next.js API Route에서 직접 파일 시스템에 저장

**장점**:
- 간단함
- 추가 HTTP 요청 없음

**단점**:
- Next.js가 파일 시스템에 직접 접근해야 함
- FastAPI와의 분리 부족
- 나중에 확장 어려움

---

## 🔧 환경 변수 설정

### Next.js 환경 변수

**파일**: `www.seoeunjin.com/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### FastAPI CORS 설정

**파일**: `cv.seoeunjin.com/app/diffuzers/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 데이터 흐름

### 방법 1 (권장)
```
[Next.js 프론트엔드]
    ↓ (파일 선택)
[Next.js API Route] (선택사항, 프록시 역할)
    ↓ (HTTP POST)
[FastAPI /api/v1/upload]
    ↓ (파일 저장)
[app/data/yolo/]
    ↓ (파일 감지)
[watch_folder.py]
    ↓ (얼굴 디텍션)
[app/data/yolo/원본파일명-detected.jpg]
```

### 방법 2 (현재)
```
[Next.js 프론트엔드]
    ↓ (파일 선택)
[Next.js API Route /api/portfolio/save]
    ↓ (직접 파일 시스템 접근)
[app/data/yolo/]
    ↓ (파일 감지)
[watch_folder.py]
    ↓ (얼굴 디텍션)
[app/data/yolo/원본파일명-detected.jpg]
```

---

## ✅ 권장 구현 순서

1. **FastAPI에 파일 업로드 엔드포인트 추가**
2. **CORS 설정 추가**
3. **Next.js에서 FastAPI 호출하도록 수정**
4. **기존 Next.js API Route 제거 또는 유지 (프록시로 사용 가능)**

---

## 🚀 실행 방법

### FastAPI 서버
```bash
cd cv.seoeunjin.com/app/diffuzers
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Next.js 서버
```bash
cd www.seoeunjin.com
npm run dev
```

### 폴더 감시 (선택사항)
```bash
cd cv.seoeunjin.com/app/yolo
python watch_folder.py
```

---

## 💡 결론

**권장**: 방법 1 (FastAPI를 통한 파일 저장)
- 더 나은 아키텍처
- 확장성과 유지보수성 향상
- 관심사 분리

**현재 방식도 작동하지만**, FastAPI를 통해 저장하는 것이 장기적으로 더 좋습니다.

