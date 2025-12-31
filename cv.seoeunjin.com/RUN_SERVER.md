# 서버 실행 방법

## FastAPI 서버 실행

### 방법 1: Python으로 직접 실행
```bash
python main.py
```

### 방법 2: uvicorn으로 실행 (권장)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 서버 실행 확인

서버 실행 후 브라우저에서:

1. **API 문서 확인**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/health
3. **루트 엔드포인트**: http://localhost:8000

## 파일 업로드 테스트 (Swagger UI)

1. http://localhost:8000/docs 접속
2. `POST /api/upload` 엔드포인트 클릭
3. "Try it out" 클릭
4. 파일 선택 후 "Execute" 클릭
5. 응답 확인

## Next.js와 연동

### 1단계: Next.js 프로젝트에서
```bash
# Next.js 프로젝트 디렉토리로 이동
cd [Next.js 프로젝트 경로]

# .env.local 파일 생성
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Next.js 실행
npm run dev
```

### 2단계: 동시 실행
- **터미널 1**: FastAPI (이 프로젝트)
- **터미널 2**: Next.js

### 3단계: 브라우저에서
- http://localhost:3000/upload (Next.js 페이지)

## 업로드된 파일 확인

업로드된 파일 위치:
```
app/data/uploads/
```

브라우저에서 직접 접근:
```
http://localhost:8000/uploads/{파일명}
```

## 현재 설정

- **FastAPI 포트**: 8000
- **Next.js 포트**: 3000 (기본값)
- **업로드 디렉토리**: `app/data/uploads/`
- **최대 파일 크기**: 10MB
- **허용 확장자**: .jpg, .jpeg, .png, .gif, .pdf, .txt, .doc, .docx

## 로그 확인

FastAPI 실행 시 터미널에서 실시간 로그 확인 가능:
- 요청/응답 로그
- 에러 로그
- 파일 업로드 상태


