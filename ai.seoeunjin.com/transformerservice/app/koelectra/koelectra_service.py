"""
KoELECTRA 감성 분석 서비스
"""
import os
import torch
from pathlib import Path
from typing import Dict, Optional, List
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification

logger = logging.getLogger(__name__)


class KoELECTRAService:
    """
    KoELECTRA 모델을 사용한 감성 분석 서비스
    싱글톤 패턴으로 모델을 한 번만 로드
    """
    _instance = None
    _model = None
    _tokenizer = None
    _is_loaded = False
    _model_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_model(self, model_path: Optional[str] = None) -> None:
        """
        KoELECTRA 모델 및 토크나이저 로드
        
        Args:
            model_path: 모델 경로 (None이면 기본 경로 사용)
        """
        if self._is_loaded:
            logger.info("모델이 이미 로드되어 있습니다.")
            return
        
        try:
            # 모델 경로 설정
            if model_path is None:
                # 기본 경로: 현재 파일 기준 상대 경로
                base_dir = Path(__file__).parent
                model_path = str(base_dir / "koelectra_model")
            
            self._model_path = model_path
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"모델 경로를 찾을 수 없습니다: {model_path}")
            
            logger.info(f"모델 로딩 시작: {model_path}")
            
            # 토크나이저 로드
            logger.info("토크나이저 로딩 중...")
            self._tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # 모델 로드
            logger.info("모델 로딩 중...")
            self._model = AutoModelForSequenceClassification.from_pretrained(model_path)
            
            # 평가 모드로 설정
            self._model.eval()
            
            # GPU 사용 가능 여부 확인
            device = "cuda" if torch.cuda.is_available() and self._use_gpu() else "cpu"
            if device == "cuda":
                self._model = self._model.to(device)
                logger.info(f"GPU 사용: {device}")
            else:
                logger.info("CPU 사용")
            
            self._is_loaded = True
            logger.info("모델 로딩 완료")
            
        except Exception as e:
            logger.error(f"모델 로딩 실패: {str(e)}")
            raise
    
    def _use_gpu(self) -> bool:
        """GPU 사용 여부 확인 (환경 변수 또는 기본값)"""
        return os.getenv("USE_GPU", "false").lower() == "true"
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        단일 텍스트의 감성 분석
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            감성 분석 결과 딕셔너리
            {
                "text": 원본 텍스트,
                "sentiment": "positive" or "negative",
                "confidence": {
                    "positive": 확률,
                    "negative": 확률
                },
                "score": 신뢰도 점수 (0.0 ~ 1.0)
            }
        """
        if not self._is_loaded:
            raise RuntimeError("모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")
        
        if not text or not text.strip():
            raise ValueError("텍스트가 비어있습니다.")
        
        try:
            # 텍스트 전처리
            text = text.strip()
            
            # 토크나이징
            inputs = self._tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # GPU 사용 시 입력을 GPU로 이동
            device = next(self._model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # 추론 실행
            with torch.no_grad():
                outputs = self._model(**inputs)
                logits = outputs.logits
            
            # 소프트맥스 적용하여 확률 계산
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
            # 결과 추출
            probs = probabilities[0].cpu().tolist()
            
            # 라벨 매핑 (일반적으로 0: negative, 1: positive)
            # 모델에 따라 다를 수 있으므로 확인 필요
            negative_score = probs[0]
            positive_score = probs[1]
            
            # 감성 결정
            if positive_score > negative_score:
                sentiment = "positive"
                score = positive_score
            else:
                sentiment = "negative"
                score = negative_score
            
            result = {
                "text": text,
                "sentiment": sentiment,
                "confidence": {
                    "positive": round(positive_score, 4),
                    "negative": round(negative_score, 4)
                },
                "score": round(score, 4)
            }
            
            logger.debug(f"감성 분석 결과: {result}")
            return result
            
        except Exception as e:
            logger.error(f"감성 분석 중 오류 발생: {str(e)}")
            raise
    
    def analyze_sentiment_batch(self, texts: List[str]) -> Dict:
        """
        여러 텍스트의 배치 감성 분석
        
        Args:
            texts: 분석할 텍스트 리스트
            
        Returns:
            배치 분석 결과
            {
                "results": [결과 리스트],
                "total": 총 개수
            }
        """
        if not texts:
            raise ValueError("텍스트 리스트가 비어있습니다.")
        
        results = []
        for text in texts:
            try:
                result = self.analyze_sentiment(text)
                results.append(result)
            except Exception as e:
                logger.error(f"텍스트 분석 실패: {text[:50]}... - {str(e)}")
                results.append({
                    "text": text,
                    "sentiment": "error",
                    "confidence": {"positive": 0.0, "negative": 0.0},
                    "score": 0.0,
                    "error": str(e)
                })
        
        return {
            "results": results,
            "total": len(results)
        }
    
    def get_model_info(self) -> Dict:
        """
        모델 정보 조회
        
        Returns:
            모델 정보 딕셔너리
        """
        return {
            "model_path": self._model_path,
            "status": "loaded" if self._is_loaded else "not_loaded",
            "device": str(next(self._model.parameters()).device) if self._is_loaded else None
        }
