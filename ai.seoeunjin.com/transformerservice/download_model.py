"""
KoELECTRA 모델 다운로드 스크립트
허깅페이스에서 모델을 다운로드하여 로컬에 저장합니다.
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

# 모델 이름 (허깅페이스 모델 ID)
# 감성 분석용 fine-tuned 모델이 있다면 그 모델 ID를 사용하세요
# 예: "monologg/koelectra-base-v3-discriminator" 또는 fine-tuned 모델
MODEL_NAME = "monologg/koelectra-base-v3-discriminator"

# 저장 경로
SAVE_PATH = Path(__file__).parent / "app" / "koelectra" / "koelectra_model"
SAVE_PATH.mkdir(parents=True, exist_ok=True)

print(f"모델 다운로드 시작: {MODEL_NAME}")
print(f"저장 경로: {SAVE_PATH}")

try:
    # 토크나이저 다운로드
    print("토크나이저 다운로드 중...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(SAVE_PATH)
    print("✓ 토크나이저 다운로드 완료")
    
    # 모델 다운로드
    print("모델 다운로드 중... (시간이 걸릴 수 있습니다)")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.save_pretrained(SAVE_PATH)
    print("✓ 모델 다운로드 완료")
    
    print(f"\n모델이 성공적으로 다운로드되었습니다: {SAVE_PATH}")
    
except Exception as e:
    print(f"❌ 다운로드 실패: {str(e)}")
    print("\n참고: 감성 분석용 fine-tuned 모델이 필요할 수 있습니다.")
    print("허깅페이스에서 감성 분석용 KoELECTRA 모델을 찾아서 MODEL_NAME을 변경하세요.")
