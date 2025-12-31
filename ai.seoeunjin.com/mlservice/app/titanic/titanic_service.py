"""
Titanic ML Service - 머신러닝 모델 학습 및 예측 서비스
"""
import pandas as pd
import numpy as np

from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from icecream import ic
import logging

# scikit-learn 임포트
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)

# 로컬 모델 임포트 (필요시 주석 해제)
# from .model import TitanicPassenger, TitanicPredictionRequest, TitanicPredictionResponse

# Titanic 메서드 임포트
from .titanic_method import TitanicMethod
from .titanic_datasets import DataSets as TitanicDatasets


class TitanicMLService:
    """타이타닉 생존 예측 머신러닝 서비스"""
    
    def __init__(self):
        """서비스 초기화"""
        # resources/titanic 폴더 경로 설정
        self.data_path = Path(__file__).parent.parent / "resources" / "titanic"
        self.train_df: Optional[pd.DataFrame] = None
        self.test_df: Optional[pd.DataFrame] = None
        self.processed_train: Optional[pd.DataFrame] = None
        self.processed_test: Optional[pd.DataFrame] = None
        self.train_labels: Optional[pd.DataFrame] = None
        self.models: Dict[str, Any] = {}
        self.model_scores: Dict[str, float] = {}  # 모델별 정확도 저장
        self.best_model_name: Optional[str] = None  # 가장 좋은 모델 이름
        self.logger = logging.getLogger(__name__)
        ic("TitanicMLService 초기화 완료")
    
    def load_train_data(self) -> pd.DataFrame:
        """
        train.csv 파일을 DataFrame으로 로드
        
        Returns:
            pandas DataFrame
        """
        train_file = self.data_path / "train.csv"
        ic(f"train.csv 로드 중: {train_file}")
        
        if not train_file.exists():
            raise FileNotFoundError(f"train.csv 파일을 찾을 수 없습니다: {train_file}")
        
        self.train_df = pd.read_csv(train_file)
        ic(f"train.csv 로드 완료: {len(self.train_df)} 행, {len(self.train_df.columns)} 열")
        ic(f"컬럼: {list(self.train_df.columns)}")
        
        return self.train_df
    
    def load_test_data(self) -> pd.DataFrame:
        """
        test.csv 파일을 DataFrame으로 로드
        
        Returns:
            pandas DataFrame
        """
        test_file = self.data_path / "test.csv"
        ic(f"test.csv 로드 중: {test_file}")
        
        if not test_file.exists():
            raise FileNotFoundError(f"test.csv 파일을 찾을 수 없습니다: {test_file}")
        
        self.test_df = pd.read_csv(test_file)
        ic(f"test.csv 로드 완료: {len(self.test_df)} 행, {len(self.test_df.columns)} 열")
        
        return self.test_df
    
    def get_train_df(self) -> Optional[pd.DataFrame]:
        """
        로드된 train DataFrame 반환
        
        Returns:
            pandas DataFrame 또는 None
        """
        if self.train_df is None:
            ic("train DataFrame이 로드되지 않았습니다. load_train_data()를 먼저 호출하세요.")
        return self.train_df
    
    def get_test_df(self) -> Optional[pd.DataFrame]:
        """
        로드된 test DataFrame 반환
        
        Returns:
            pandas DataFrame 또는 None
        """
        if self.test_df is None:
            ic("test DataFrame이 로드되지 않았습니다. load_test_data()를 먼저 호출하세요.")
        return self.test_df
    
    def _get_data_path(self, filename: str) -> Path:
        """
        데이터 파일 경로 반환
        
        Args:
            filename: 파일명 (예: 'train.csv', 'test.csv')
            
        Returns:
            Path 객체
        """
        file_path = self.data_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        return file_path
    
    def _apply_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        train과 test에 공통으로 적용할 전처리 파이프라인
        
        Args:
            df: 전처리할 DataFrame
            
        Returns:
            전처리된 DataFrame
        """
        the_method = TitanicMethod()
        
        # 1. 불필요한 피처 삭제
        drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
        df = the_method.drop_feature(df, *drop_features)
        
        # 2. 전처리 파이프라인 적용
        df = the_method.pclass_ordinal(df)
        df = the_method.fare_ordinal(df)
        df = the_method.embarked_ordinal(df)
        df = the_method.gender_nominal(df)
        df = the_method.age_ratio(df)
        df = the_method.title_nominal(df)
        
        # 3. Name 컬럼 제거
        df = the_method.drop_feature(df, 'Name')
        
        return df
    
    def preprocess(self):
        ic("😎😎 전처리 시작")
        the_method = TitanicMethod()
        
        # ========== TRAIN 전처리 ==========
        train_csv_path = self._get_data_path('train.csv')
        ic(f'[TRAIN] train.csv 경로: {train_csv_path}')
        df_train = the_method.new_model(str(train_csv_path))
        
        # Survived 컬럼 제거 (train에만 존재)
        this_train = the_method.create_train(df_train, 'Survived')
        ic(f'[TRAIN 원본] type: {type(this_train)}')
        ic(f'[TRAIN 원본] 컬럼: {this_train.columns.tolist()}')
        ic(f'[TRAIN 원본] 상위 5개 행:\n{this_train.head(5)}')
        ic(f'[TRAIN 원본] null 개수: {the_method.check_null(this_train)}개')
        
        # 공통 전처리 적용
        this_train = self._apply_preprocessing(this_train)
        ic(f'[TRAIN 완료] type: {type(this_train)}')
        ic(f'[TRAIN 완료] 컬럼: {this_train.columns.tolist()}')
        # Gender 컬럼을 앞쪽에 배치해서 명확히 보이도록 출력
        display_cols = ['PassengerId', 'Pclass', 'Gender', 'Age', 'Fare', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
        # DataFrame을 예쁘게 한 줄로 출력
        train_display = this_train[display_cols].head(5).to_string(index=True)
        ic(f'[TRAIN 완료] 상위 5개 행 (Gender 포함):\n{train_display}')
        ic(f'[TRAIN 완료] null 개수: {the_method.check_null(this_train)}개')
        
        # ========== TEST 전처리 ==========
        test_csv_path = self._get_data_path('test.csv')
        ic(f'[TEST] test.csv 경로: {test_csv_path}')
        df_test = the_method.new_model(str(test_csv_path))
        
        # test에는 Survived 컬럼이 없으므로 그냥 복사
        this_test = df_test.copy()
        ic(f'[TEST 원본] type: {type(this_test)}')
        ic(f'[TEST 원본] 컬럼: {this_test.columns.tolist()}')
        ic(f'[TEST 원본] 상위 5개 행:\n{this_test.head(5)}')
        ic(f'[TEST 원본] null 개수: {the_method.check_null(this_test)}개')
        
        # 공통 전처리 적용 (train과 동일)
        this_test = self._apply_preprocessing(this_test)
        ic(f'[TEST 완료] type: {type(this_test)}')
        ic(f'[TEST 완료] 컬럼: {this_test.columns.tolist()}')
        # Gender 컬럼을 앞쪽에 배치해서 명확히 보이도록 출력
        display_cols = ['PassengerId', 'Pclass', 'Gender', 'Age', 'Fare', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
        # DataFrame을 예쁘게 한 줄로 출력
        test_display = this_test[display_cols].head(5).to_string(index=True)
        ic(f'[TEST 완료] 상위 5개 행 (Gender 포함):\n{test_display}')
        ic(f'[TEST 완료] null 개수: {the_method.check_null(this_test)}개')
        
        ic("😎😎 전처리 완료")
        
        # 전처리된 데이터 저장
        self.processed_train = this_train
        self.processed_test = this_test
        
        # Survived 라벨 저장 (학습용)
        self.train_labels = df_train[['Survived']]
        
        dataset = TitanicDatasets()


    def modeling(self):
        """모델 초기화"""
        ic("모델링 시작")
        
        # 학습에 사용할 모델들 초기화
        self.models = {
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'naive_bayes': GaussianNB(),
            'svm': SVC(random_state=42, probability=True),
            'knn': KNeighborsClassifier(n_neighbors=5)
        }
        
        ic("모델링 완료")

    def learning(self):
        """모델 학습"""
        self.logger.info("학습 시작")
        
        if self.processed_train is None or self.train_labels is None:
            raise ValueError("전처리가 완료되지 않았습니다. preprocess()를 먼저 실행하세요.")
        
        # 학습 데이터 준비 (문자열/카테고리 컬럼 제외)
        # 제거할 컬럼: PassengerId, 원본 문자열 컬럼들, 카테고리 컬럼들
        drop_cols = ['PassengerId', 'Embarked', 'Fare_band', 'Age_band', 'Title']
        X_train = self.processed_train.drop(columns=drop_cols, errors='ignore')
        
        # 카테고리 컬럼을 수치형으로 변환 (Age_band_ordinal은 이미 수치형)
        # boolean 컬럼들을 int로 변환
        for col in X_train.columns:
            if X_train[col].dtype == 'bool':
                X_train[col] = X_train[col].astype(int)
            elif X_train[col].dtype.name == 'category':
                X_train[col] = X_train[col].astype(int)
        
        y_train = self.train_labels.values.ravel()
        
        # 각 모델 학습
        for model_name, model in self.models.items():
            self.logger.info(f"{model_name} 학습 중...")
            model.fit(X_train, y_train)
            self.logger.info(f"{model_name} 학습 완료")
        
        self.logger.info("학습 완료")

    def evaluation(self) -> Dict[str, float]:
        """모델 평가"""
        self.logger.info("평가 시작")
        
        if self.processed_train is None or self.train_labels is None:
            raise ValueError("전처리가 완료되지 않았습니다. preprocess()를 먼저 실행하세요.")
        
        if not self.models:
            raise ValueError("모델이 학습되지 않았습니다. learning()을 먼저 실행하세요.")
        
        # 평가 데이터 준비 (문자열/카테고리 컬럼 제외)
        # 제거할 컬럼: PassengerId, 원본 문자열 컬럼들, 카테고리 컬럼들
        drop_cols = ['PassengerId', 'Embarked', 'Fare_band', 'Age_band', 'Title']
        X_train = self.processed_train.drop(columns=drop_cols, errors='ignore')
        
        # 카테고리 컬럼을 수치형으로 변환
        for col in X_train.columns:
            if X_train[col].dtype == 'bool':
                X_train[col] = X_train[col].astype(int)
            elif X_train[col].dtype.name == 'category':
                X_train[col] = X_train[col].astype(int)
        
        y_train = self.train_labels.values.ravel()
        
        # 학습 데이터를 train/validation으로 분할
        X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
        )
        
        results = {}
        
        # 각 모델 평가
        for model_name, model in self.models.items():
            # 검증 데이터로 예측
            y_pred = model.predict(X_val_split)
            accuracy = accuracy_score(y_val_split, y_pred)
            results[model_name] = accuracy
            self.model_scores[model_name] = accuracy  # 점수 저장
            self.logger.info(f'{model_name} 활용한 검증 정확도: {accuracy:.4f}')
        
        # 가장 좋은 모델 선택
        if self.model_scores:
            self.best_model_name = max(self.model_scores, key=self.model_scores.get)
            self.logger.info(f'최고 성능 모델: {self.best_model_name} (정확도: {self.model_scores[self.best_model_name]:.4f})')
        
        # LightGBM은 별도 라이브러리이므로 주석 처리
        # try:
        #     import lightgbm as lgb
        #     lgb_model = lgb.LGBMClassifier(random_state=42)
        #     lgb_model.fit(X_train_split, y_train_split)
        #     y_pred_lgb = lgb_model.predict(X_val_split)
        #     accuracy_lgb = accuracy_score(y_val_split, y_pred_lgb)
        #     results['lightgbm'] = accuracy_lgb
        #     self.logger.info(f'LightGBM 활용한 검증 정확도: {accuracy_lgb:.4f}')
        # except ImportError:
        #     self.logger.warning("LightGBM이 설치되지 않아 평가를 건너뜁니다.")
        self.logger.info("LightGBM 활용한 검증 정확도: (LightGBM 미설치로 건너뜀)")
        
        self.logger.info("평가 완료")
        return results

    def postprocess(self):
        ic("후처리 시작")
        ic("후처리 완료")

    def submit(self, model_name: Optional[str] = None) -> str:
        """
        Kaggle 제출용 submission.csv 파일 생성
        
        Args:
            model_name: 사용할 모델 이름 (None이면 랜덤 포레스트 사용)
                        사용 가능: logistic_regression, random_forest, naive_bayes, svm, knn
            
        Returns:
            생성된 CSV 파일 경로
        """
        ic("제출 시작")
        self.logger.info("Kaggle 제출용 submission.csv 생성 시작")
        ic(f"processed_test is None: {self.processed_test is None}")
        ic(f"models is empty: {not self.models}")
        
        if self.processed_test is None:
            self.logger.error("전처리가 완료되지 않았습니다. preprocess()를 먼저 실행하세요.")
            raise ValueError("전처리가 완료되지 않았습니다. preprocess()를 먼저 실행하세요.")
        
        if not self.models:
            self.logger.error("모델이 학습되지 않았습니다. learning()을 먼저 실행하세요.")
            raise ValueError("모델이 학습되지 않았습니다. learning()을 먼저 실행하세요.")
        
        # 사용할 모델 선택
        if model_name is None:
            if self.best_model_name is not None:
                model_name = self.best_model_name  # 평가 결과에서 가장 좋은 모델 사용
                self.logger.info(f"평가 결과 기반으로 최고 성능 모델 '{model_name}' 사용")
            else:
                model_name = 'random_forest'  # 평가가 안 되어 있으면 랜덤 포레스트 사용
                self.logger.warning("평가가 완료되지 않아 랜덤 포레스트를 사용합니다.")
        
        if model_name not in self.models:
            raise ValueError(f"모델 '{model_name}'을 찾을 수 없습니다. 사용 가능한 모델: {list(self.models.keys())}")
        
        model = self.models[model_name]
        self.logger.info(f"예측에 사용할 모델: {model_name}")
        
        # test 데이터 준비 (학습 시와 동일한 전처리)
        drop_cols = ['PassengerId', 'Embarked', 'Fare_band', 'Age_band', 'Title']
        X_test = self.processed_test.drop(columns=drop_cols, errors='ignore')
        
        # 카테고리 컬럼을 수치형으로 변환
        for col in X_test.columns:
            if X_test[col].dtype == 'bool':
                X_test[col] = X_test[col].astype(int)
            elif X_test[col].dtype.name == 'category':
                X_test[col] = X_test[col].astype(int)
        
        # 예측 수행
        self.logger.info("test 데이터 예측 중...")
        predictions = model.predict(X_test)
        
        # PassengerId 가져오기
        passenger_ids = self.processed_test['PassengerId'].values
        
        # submission DataFrame 생성
        submission_df = pd.DataFrame({
            'PassengerId': passenger_ids,
            'Survived': predictions.astype(int)
        })
        
        # download 폴더에 저장 (컨테이너 내부 /app/download/)
        # 컨테이너 내부 경로: /app/download/submission.csv
        download_dir = Path('/app/download')
        download_dir.mkdir(exist_ok=True)  # 폴더가 없으면 생성
        
        submission_path = download_dir / 'submission.csv'
        ic(f"파일 저장 경로: {submission_path}")
        ic(f"폴더 존재 여부: {download_dir.exists()}")
        ic(f"파일 저장 전 행 수: {len(submission_df)}")
        
        submission_df.to_csv(submission_path, index=False)
        
        ic(f"파일 저장 후 존재 여부: {submission_path.exists()}")
        ic(f"파일 크기: {submission_path.stat().st_size if submission_path.exists() else '파일 없음'}")
        self.logger.info(f"submission.csv 파일 생성 완료: {submission_path}")
        self.logger.info(f"예측 결과 요약:")
        self.logger.info(f"  - 총 예측 수: {len(predictions)}")
        self.logger.info(f"  - 생존 예측: {predictions.sum()}명")
        self.logger.info(f"  - 사망 예측: {len(predictions) - predictions.sum()}명")
        
        ic("제출 완료")
        return str(submission_path)

