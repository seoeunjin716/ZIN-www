# KoELECTRA 감성 분석 서비스 아키텍처 전략

## 📋 목차
1. [개요](#개요)
2. [아키텍처 설계](#아키텍처-설계)
3. [폴더 구조](#폴더-구조)
4. [모델 로딩 전략](#모델-로딩-전략)
5. [API 설계](#api-설계)
6. [구현 단계](#구현-단계)

---

## 개요

### 목표
- KoELECTRA 모델을 사용하여 영화 리뷰 텍스트의 긍정/부정 감성을 분석하는 서비스
- 허깅페이스(Hugging Face)에서 사전 학습된 모델 활용
- FastAPI 기반 RESTful API 제공

### 기술 스택
- **모델**: KoELECTRA (monologg/koelectra-base-v3-discriminator)
- **프레임워크**: Transformers (Hugging Face)
- **API**: FastAPI
- **언어**: Python 3.x

---

## 아키텍처 설계

### 1. 계층 구조 (Layered Architecture)

```
┌─────────────────────────────────────┐
│      API Layer (Router)             │
│  - FastAPI 엔드포인트 정의           │
│  - 요청/응답 검증                    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Service Layer                  │
│  - 비즈니스 로직 처리                │
│  - 전처리/후처리                     │
│  - 에러 처리                         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Model Layer (Singleton)        │
│  - 모델 로딩 및 관리                 │
│  - 추론(Inference) 실행              │
│  - 모델 캐싱                         │
└─────────────────────────────────────┘
```

### 2. 모델 싱글톤 패턴

**이유**: 
- 대규모 Transformer 모델은 메모리 사용량이 큼 (약 500MB~1GB)
- 서버 시작 시 한 번만 로드하여 메모리 효율성 확보
- 요청마다 모델을 로드하면 응답 시간이 매우 느려짐

**구현 방식**:
- 앱 시작 시 모델을 한 번만 로드
- 전역 변수 또는 클래스 변수로 모델 인스턴스 관리
- Lazy Loading: 첫 요청 시 로드 (선택적)

---

## 폴더 구조

```
mlservice/
└── app/
    └── nlp/
        └── review/
            ├── __init__.py
            ├── emotion_model.py       # 모델 로딩 및 추론 (Singleton)
            ├── emotion_service.py     # 비즈니스 로직
            ├── emotion_router.py      # FastAPI 라우터
            └── corpus/                # 학습 데이터 (기존)
                └── *.json
```

### 파일별 역할

#### 1. `emotion_model.py`
- **역할**: KoELECTRA 모델 로딩 및 추론
- **주요 기능**:
  - 허깅페이스 모델 다운로드 및 로드
  - 텍스트 전처리 (토크나이징)
  - 감성 분석 추론 실행
  - 싱글톤 패턴으로 모델 인스턴스 관리

#### 2. `emotion_service.py`
- **역할**: 비즈니스 로직 및 서비스 레이어
- **주요 기능**:
  - 입력 검증
  - 텍스트 전처리 (필요시)
  - 모델 호출
  - 결과 후처리 및 포맷팅
  - 에러 처리

#### 3. `emotion_router.py`
- **역할**: FastAPI 라우터 정의
- **주요 기능**:
  - API 엔드포인트 정의
  - 요청/응답 모델 정의 (Pydantic)
  - 서비스 레이어 호출

---

## 모델 로딩 전략

### 1. 허깅페이스 모델 선택

**추천 모델**:
- `monologg/koelectra-base-v3-discriminator`
- `monologg/koelectra-small-v3-discriminator` (경량 버전)

**모델 다운로드 위치**:
- 로컬: `~/.cache/huggingface/transformers/` (기본)
- 커스텀: 환경 변수로 경로 지정 가능

### 2. 모델 로딩 코드 구조

```python
# emotion_model.py 예시 구조

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class EmotionModel:
    _instance = None
    _model = None
    _tokenizer = None
    _is_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_model(self, model_name: str = "monologg/koelectra-base-v3-discriminator"):
        """모델 및 토크나이저 로드 (한 번만 실행)"""
        if self._is_loaded:
            return
        
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self._model.eval()  # 평가 모드
        self._is_loaded = True
    
    def predict(self, text: str) -> dict:
        """감성 분석 추론"""
        # 토크나이징
        # 추론 실행
        # 결과 반환
```

### 3. 메모리 최적화 고려사항

- **GPU 사용**: CUDA 사용 가능 시 GPU 메모리 활용
- **모델 양자화**: INT8 양자화로 메모리 사용량 감소 (선택적)
- **배치 처리**: 여러 텍스트를 한 번에 처리 (효율성 향상)

---

## API 설계

### 엔드포인트

#### 1. 단일 텍스트 감성 분석
```
POST /api/ml/review/sentiment
GET  /api/ml/review/sentiment?text={리뷰}
```

**요청**:
```json
{
  "text": "이 영화 정말 재미있었어요! 강력 추천합니다."
}
```

**응답**:
```json
{
  "text": "이 영화 정말 재미있었어요! 강력 추천합니다.",
  "sentiment": "positive",
  "confidence": {
    "positive": 0.95,
    "negative": 0.05
  },
  "score": 0.95
}
```

#### 2. 배치 감성 분석
```
POST /api/ml/review/sentiment/batch
```

**요청**:
```json
{
  "texts": [
    "정말 최고의 영화예요!",
    "별로 재미없었습니다."
  ]
}
```

**응답**:
```json
{
  "results": [
    {
      "text": "정말 최고의 영화예요!",
      "sentiment": "positive",
      "confidence": {"positive": 0.98, "negative": 0.02},
      "score": 0.98
    },
    {
      "text": "별로 재미없었습니다.",
      "sentiment": "negative",
      "confidence": {"positive": 0.15, "negative": 0.85},
      "score": 0.85
    }
  ],
  "total": 2
}
```

#### 3. 모델 정보 조회
```
GET /api/ml/review/model/info
```

**응답**:
```json
{
  "model_name": "monologg/koelectra-base-v3-discriminator",
  "status": "loaded",
  "loaded_at": "2025-12-15T12:00:00Z"
}
```

### 요청/응답 모델 (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Dict

class SentimentRequest(BaseModel):
    text: str

class BatchSentimentRequest(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    sentiment: str  # "positive" or "negative"
    confidence: Dict[str, float]
    score: float
```

---

## 구현 단계

### Phase 1: 기본 구조 설정
1. ✅ 폴더 구조 생성
2. ✅ `emotion_model.py` 기본 클래스 작성
3. ✅ 싱글톤 패턴 구현
4. ✅ 모델 로딩 함수 작성

### Phase 2: 모델 통합
1. Transformers 라이브러리 설치
2. KoELECTRA 모델 다운로드 및 로드
3. 토크나이저 설정
4. 추론 함수 구현

### Phase 3: 서비스 레이어 구현
1. `emotion_service.py` 작성
2. 전처리 로직 (필요시)
3. 후처리 및 포맷팅
4. 에러 핸들링

### Phase 4: API 구현
1. `emotion_router.py` 작성
2. Pydantic 모델 정의
3. 엔드포인트 구현
4. `nlp_router.py`에 통합

### Phase 5: 최적화 및 테스트
1. 성능 테스트
2. 메모리 사용량 모니터링
3. 에러 처리 개선
4. 로깅 추가

---

## 의존성 추가

### requirements.txt에 추가할 패키지

```txt
# Transformers 및 관련 패키지
transformers>=4.30.0
torch>=2.0.0
sentencepiece>=0.1.99  # KoELECTRA 토크나이저용
```

### 설치 명령

```bash
pip install transformers torch sentencepiece
# 또는
conda install -c pytorch pytorch
pip install transformers sentencepiece
```

---

## 성능 고려사항

### 1. 응답 시간
- **모델 로딩**: 서버 시작 시 1회 (약 5-10초)
- **단일 추론**: 약 50-200ms (CPU 기준)
- **배치 추론**: 배치 크기에 따라 선형 증가

### 2. 메모리 사용량
- **모델 크기**: 약 500MB~1GB
- **추론 시**: 입력 길이에 따라 추가 메모리 사용

### 3. 최적화 전략
- **GPU 사용**: CUDA 사용 가능 시 10-50배 속도 향상
- **배치 처리**: 여러 요청을 배치로 묶어 처리
- **모델 캐싱**: 모델을 메모리에 유지

---

## 보안 및 에러 처리

### 1. 입력 검증
- 텍스트 길이 제한 (예: 최대 512 토큰)
- 특수 문자 및 악성 코드 필터링
- 빈 문자열 처리

### 2. 에러 처리
- 모델 로딩 실패 시 적절한 에러 메시지
- 추론 중 오류 발생 시 로깅 및 사용자 친화적 응답
- 타임아웃 처리

### 3. 로깅
- 요청 로깅
- 추론 시간 측정
- 에러 로깅

---

## 테스트 전략

### 1. 단위 테스트
- 모델 로딩 테스트
- 추론 함수 테스트
- 전처리/후처리 테스트

### 2. 통합 테스트
- API 엔드포인트 테스트
- 배치 처리 테스트
- 에러 케이스 테스트

### 3. 성능 테스트
- 동시 요청 처리 능력
- 메모리 누수 확인
- 응답 시간 측정

---

## 배포 고려사항

### 1. Docker
- 모델을 이미지에 포함할지, 볼륨 마운트할지 결정
- 메모리 제한 설정

### 2. 환경 변수
- 모델 경로 설정
- GPU 사용 여부
- 배치 크기 설정

### 3. 모니터링
- 메모리 사용량 모니터링
- 응답 시간 모니터링
- 에러율 추적

---

## 참고 자료

- [KoELECTRA GitHub](https://github.com/monologg/KoELECTRA)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [FastAPI 문서](https://fastapi.tiangolo.com/)

---

## 다음 단계

1. 기본 구조 파일 생성
2. 모델 로딩 코드 구현
3. 추론 함수 구현
4. API 엔드포인트 구현
5. 테스트 및 최적화
