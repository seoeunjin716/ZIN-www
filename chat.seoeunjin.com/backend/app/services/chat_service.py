"""QLoRA를 사용한 채팅 및 파인튜닝 서비스."""

import os
from pathlib import Path
from typing import List, Optional, Tuple

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    GenerationConfig,
    Trainer,
    TrainingArguments,
)


class ChatService:
    """QLoRA를 사용한 채팅 및 파인튜닝 서비스."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        use_quantization: bool = True,
        quantization_bits: int = 4,
    ):
        """ChatService 초기화.

        Args:
            model_path: 모델 경로. None이면 기본 경로 사용.
            use_quantization: 양자화 사용 여부 (기본값: True).
            quantization_bits: 양자화 비트 수 (4 또는 8, 기본값: 4).
        """
        if model_path is None:
            # 기본 경로: backend/app/models/midm
            current_dir = Path(__file__).parent
            model_path = str(current_dir.parent / "models" / "midm")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"모델 경로를 찾을 수 없습니다: {model_path}")

        self.model_path = model_path
        self.use_quantization = use_quantization
        self.quantization_bits = quantization_bits
        self.model: Optional[AutoModelForCausalLM] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.peft_model = None

    def load_model(
        self,
        use_lora: bool = False,
        lora_r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.05,
        lora_target_modules: Optional[List[str]] = None,
    ) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        """QLoRA 모델 로드.

        Args:
            use_lora: LoRA 어댑터 사용 여부 (학습 시 True).
            lora_r: LoRA rank (기본값: 16).
            lora_alpha: LoRA alpha (기본값: 32).
            lora_dropout: LoRA dropout (기본값: 0.05).
            lora_target_modules: LoRA를 적용할 모듈 목록. None이면 자동 선택.

        Returns:
            (model, tokenizer) 튜플.
        """
        print(f"📦 QLoRA 모델 로딩 중: {self.model_path}")

        # 양자화 설정
        quantization_config = None
        if self.use_quantization:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=(self.quantization_bits == 4),
                load_in_8bit=(self.quantization_bits == 8),
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        # 모델 로드
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16 if not self.use_quantization else None,
        )

        # 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # LoRA 설정 (학습 시)
        if use_lora:
            if lora_target_modules is None:
                # Midm 모델의 기본 타겟 모듈 (Llama 계열)
                lora_target_modules = [
                    "q_proj",
                    "k_proj",
                    "v_proj",
                    "o_proj",
                    "gate_proj",
                    "up_proj",
                    "down_proj",
                ]

            lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=lora_r,
                lora_alpha=lora_alpha,
                lora_dropout=lora_dropout,
                target_modules=lora_target_modules,
                bias="none",
            )

            self.peft_model = get_peft_model(self.model, lora_config)
            self.peft_model.print_trainable_parameters()
            print("✅ LoRA 어댑터 추가 완료")

        print("✅ 모델 로드 완료")
        return self.model, self.tokenizer

    def chat(
        self,
        message: str,
        history: Optional[List[dict]] = None,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        do_sample: bool = True,
        **generation_kwargs,
    ) -> str:
        """대화 생성.

        Args:
            message: 사용자 메시지.
            history: 대화 히스토리 (선택적).
            max_new_tokens: 최대 생성 토큰 수.
            temperature: 생성 온도.
            do_sample: 샘플링 사용 여부.
            **generation_kwargs: 추가 생성 파라미터.

        Returns:
            생성된 응답 텍스트.

        Raises:
            ValueError: 모델이 로드되지 않은 경우.
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError(
                "모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요."
            )

        # 대화 형식으로 메시지 구성
        messages = []

        # 시스템 메시지
        messages.append(
            {
                "role": "system",
                "content": "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 대화합니다.",
            }
        )

        # 대화 히스토리 추가
        if history:
            messages.extend(history)

        # 현재 사용자 메시지 추가
        messages.append({"role": "user", "content": message})

        # 토크나이저로 변환
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to(self.model.device)

        # Generation Config 로드 (있는 경우)
        generation_config = None
        generation_config_path = Path(self.model_path) / "generation_config.json"
        if generation_config_path.exists():
            generation_config = GenerationConfig.from_pretrained(self.model_path)

        # 텍스트 생성
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample,
                generation_config=generation_config,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
                **generation_kwargs,
            )

        # 응답 디코딩
        response = self.tokenizer.decode(
            outputs[0][input_ids.shape[1] :], skip_special_tokens=True
        )
        return response.strip()

    def train(
        self,
        dataset: Dataset,
        output_dir: str,
        num_train_epochs: int = 3,
        per_device_train_batch_size: int = 1,
        gradient_accumulation_steps: int = 4,
        learning_rate: float = 2e-4,
        warmup_steps: int = 100,
        logging_steps: int = 10,
        save_steps: int = 500,
        **training_kwargs,
    ) -> Trainer:
        """QLoRA 파인튜닝 실행.

        Args:
            dataset: 학습 데이터셋 (datasets.Dataset).
            output_dir: 모델 저장 경로.
            num_train_epochs: 학습 에폭 수.
            per_device_train_batch_size: 디바이스당 배치 크기.
            gradient_accumulation_steps: 그래디언트 누적 스텝 수.
            learning_rate: 학습률.
            warmup_steps: 워밍업 스텝 수.
            logging_steps: 로깅 스텝 간격.
            save_steps: 저장 스텝 간격.
            **training_kwargs: 추가 학습 파라미터.

        Returns:
            Trainer 인스턴스.

        Raises:
            ValueError: 모델이 로드되지 않았거나 LoRA가 설정되지 않은 경우.
        """
        if self.peft_model is None:
            raise ValueError(
                "LoRA 모델이 로드되지 않았습니다. load_model(use_lora=True)를 먼저 호출하세요."
            )

        # 데이터 전처리 함수
        def preprocess_function(examples):
            # 데이터셋 형식에 따라 수정 필요
            # 예: {"instruction": "...", "input": "...", "output": "..."}
            if "instruction" in examples:
                texts = []
                for i in range(len(examples["instruction"])):
                    instruction = examples["instruction"][i]
                    input_text = (
                        examples.get("input", [""])[i] if "input" in examples else ""
                    )
                    output = examples["output"][i]

                    if input_text:
                        text = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
                    else:
                        text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"

                    texts.append(text)
            else:
                # 간단한 텍스트 쌍 형식
                texts = examples.get("text", examples.get("input", []))

            # 토크나이징
            model_inputs = self.tokenizer(
                texts,
                max_length=512,
                truncation=True,
                padding="max_length",
            )
            model_inputs["labels"] = model_inputs["input_ids"].copy()
            return model_inputs

        # 데이터 전처리
        tokenized_dataset = dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=dataset.column_names,
        )

        # 학습 인자 설정
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            logging_steps=logging_steps,
            save_steps=save_steps,
            save_strategy="steps",
            evaluation_strategy="no",
            logging_dir=f"{output_dir}/logs",
            report_to="none",
            **training_kwargs,
        )

        # Trainer 생성 및 학습
        trainer = Trainer(
            model=self.peft_model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=lambda x: {
                "input_ids": torch.stack(
                    [torch.tensor(item["input_ids"]) for item in x]
                ),
                "attention_mask": torch.stack(
                    [torch.tensor(item["attention_mask"]) for item in x]
                ),
                "labels": torch.stack([torch.tensor(item["labels"]) for item in x]),
            },
        )

        print("🚀 학습 시작...")
        trainer.train()
        print(f"✅ 학습 완료! 모델이 {output_dir}에 저장되었습니다.")

        # 최종 모델 저장
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)

        return trainer

    def save_lora_adapter(self, output_dir: str) -> None:
        """LoRA 어댑터만 저장.

        Args:
            output_dir: 저장 경로.

        Raises:
            ValueError: LoRA 모델이 없는 경우.
        """
        if self.peft_model is None:
            raise ValueError("LoRA 모델이 없습니다.")

        self.peft_model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        print(f"✅ LoRA 어댑터가 {output_dir}에 저장되었습니다.")

    def load_lora_adapter(self, adapter_path: str) -> None:
        """LoRA 어댑터 로드.

        Args:
            adapter_path: 어댑터 경로.

        Raises:
            ValueError: 기본 모델이 로드되지 않은 경우.
        """
        if self.model is None:
            raise ValueError(
                "기본 모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요."
            )

        from peft import PeftModel

        self.peft_model = PeftModel.from_pretrained(self.model, adapter_path)
        print(f"✅ LoRA 어댑터가 {adapter_path}에서 로드되었습니다.")
