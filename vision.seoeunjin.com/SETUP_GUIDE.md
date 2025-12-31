# 파일 업로드 시스템 설정 가이드

## 1. FastAPI 설정 (완료)

### 설치된 파일:
- `main.py` - 메인 FastAPI 애플리케이션
- `app/api/routes/upload.py` - 파일 업로드 라우터
- `app/data/uploads/` - 업로드 파일 저장 디렉토리

### FastAPI 실행:

```bash
# 방법 1: Python으로 직접 실행
python main.py

# 방법 2: uvicorn으로 실행 (권장)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

서버 실행 후 접속:
- API 문서: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 2. Next.js 설정

### 1단계: Next.js 프로젝트에 파일 복사

`NEXTJS_FILE_UPLOAD_COMPONENT.tsx` 파일을 Next.js 프로젝트에 복사:

```bash
# Next.js 프로젝트 디렉토리에서
cp NEXTJS_FILE_UPLOAD_COMPONENT.tsx components/FileUpload.tsx
```

### 2단계: 환경 변수 설정

Next.js 프로젝트 루트에 `.env.local` 파일 생성:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3단계: 페이지에서 사용

```tsx
// app/upload/page.tsx 또는 pages/upload.tsx
import FileUpload from '@/components/FileUpload';

export default function UploadPage() {
  return (
    <div>
      <FileUpload />
    </div>
  );
}
```

### 4단계: Next.js 실행

```bash
npm run dev
# 또는
yarn dev
```

서버 실행 후 접속:
- http://localhost:3000/upload

## 3. 동시 실행 방법

### 터미널 1 - FastAPI
```bash
cd C:\Users\hi\Documents\seoeunjin\seoeunjin.com\cv.seoeunjin.com
python main.py
```

### 터미널 2 - Next.js
```bash
cd [Next.js 프로젝트 경로]
npm run dev
```

## 4. API 엔드포인트

### 파일 업로드
```
POST http://localhost:8000/api/upload
Content-Type: multipart/form-data

Body: file (파일)
```

### 파일 목록 조회
```
GET http://localhost:8000/api/files
```

### 파일 삭제
```
DELETE http://localhost:8000/api/files/{filename}
```

### 업로드된 파일 다운로드
```
GET http://localhost:8000/uploads/{filename}
```

## 5. 허용된 파일 형식

현재 설정된 허용 확장자:
- 이미지: `.jpg`, `.jpeg`, `.png`, `.gif`
- 문서: `.pdf`, `.txt`, `.doc`, `.docx`

최대 파일 크기: 10MB

## 6. 디렉토리 구조

```
cv.seoeunjin.com/
├── main.py                    # FastAPI 메인 (실행파일)
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── upload.py      # 업로드 라우터
│   └── data/
│       └── uploads/           # 업로드된 파일 저장
│
nextjs-app/                    # Next.js 프로젝트
├── components/
│   └── FileUpload.tsx         # 업로드 컴포넌트
├── app/
│   └── upload/
│       └── page.tsx           # 업로드 페이지
└── .env.local                 # 환경 변수
```

## 7. 테스트

### FastAPI 테스트 (curl)
```bash
# 파일 업로드
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.jpg"

# 파일 목록 조회
curl http://localhost:8000/api/files

# 파일 삭제
curl -X DELETE http://localhost:8000/api/files/20241231_120000_test.jpg
```

### FastAPI 테스트 (브라우저)
http://localhost:8000/docs 에서 Swagger UI로 테스트 가능

## 8. 문제 해결

### CORS 오류
- FastAPI의 `main.py`에서 Next.js 주소가 올바른지 확인
- 브라우저 콘솔에서 오류 확인

### 파일 업로드 실패
- 파일 크기 확인 (10MB 이하)
- 파일 확장자 확인
- FastAPI 로그 확인

### 파일 저장 경로 오류
- `app/data/uploads/` 디렉토리가 자동 생성되는지 확인
- 쓰기 권한 확인

## 9. 추가 기능 (선택사항)

### 다중 파일 업로드
```python
# app/api/routes/upload.py에 추가
@router.post("/upload/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        # 업로드 로직
        ...
    return results
```

### 이미지 썸네일 생성
```python
from PIL import Image

# 썸네일 생성
img = Image.open(file_path)
img.thumbnail((200, 200))
thumbnail_path = file_path.with_suffix('.thumb.jpg')
img.save(thumbnail_path)
```

## 10. 보안 고려사항

1. **파일 타입 검증**: 현재 확장자만 검증. MIME 타입도 검증 권장
2. **파일명 새니타이징**: 타임스탬프 추가로 기본 보안
3. **크기 제한**: 10MB로 제한됨
4. **경로 탐색 공격 방지**: Path 객체 사용으로 방어
5. **프로덕션**: HTTPS 사용 권장

## 완료!

이제 Next.js에서 파일을 업로드하면 FastAPI의 `app/data/uploads/` 디렉토리에 저장됩니다.

