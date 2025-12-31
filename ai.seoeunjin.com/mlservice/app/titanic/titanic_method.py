from pathlib import Path
import numpy as np
import pandas as pd
from pandas import DataFrame
from .titanic_datasets import DataSets as TitanicDatasets
from icecream import ic

class TitanicMethod(object): 

    def __init__(self):
        self.dataset = TitanicDatasets()

    def new_model(self, fname: str) -> pd.DataFrame:
        """CSV 파일을 읽어 DataFrame으로 반환"""
        # 상대 경로인 경우 현재 파일 기준으로 경로 찾기
        if not Path(fname).is_absolute():
            # titanic_method.py 파일의 디렉토리 기준으로 경로 찾기
            base_path = Path(__file__).parent
            fname = str(base_path / fname)
        return pd.read_csv(fname)
    def read_data(self, fname: str) -> pd.DataFrame:
        return pd.read_csv(fname)

    def create_train(self, df: pd.DataFrame, label: str) -> pd.DataFrame:
        return df.drop(columns=[label])

    def create_label(self, df: pd.DataFrame, label: str) -> pd.DataFrame:
        return df[[label]]

    def drop_feature(self, df_or_this, *feature: str):
        """
        피처 삭제 메서드
        - DataFrame을 받으면 DataFrame을 반환 (현재 titanic_service.py에서 사용)
        - DataSets 객체(this)를 받으면 원래 구조대로 this.train, this.test 수정 후 this 반환
        """
        feature_list = [f for f in feature]
        
        # DataFrame인 경우 (현재 titanic_service.py에서 사용)
        if isinstance(df_or_this, pd.DataFrame):
            return df_or_this.drop(columns=feature_list)
        
        # DataSets 객체인 경우 (원래 구조)
        this = df_or_this
        [i.drop(j, axis=1, inplace=True) for j in feature_list for i in [this.train, this.test]]
        return this

    def check_null(self, df_or_this) -> int:
        """
        null 개수 확인 메서드
        - DataFrame을 받으면 해당 DataFrame의 null 개수 반환 (현재 titanic_service.py에서 사용)
        - DataSets 객체(this)를 받으면 원래 구조대로 this.train과 this.test의 null 개수 합산
        """
        # DataFrame인 경우 (현재 titanic_service.py에서 사용)
        if isinstance(df_or_this, pd.DataFrame):
            return int(df_or_this.isnull().sum().sum())
        
        # DataSets 객체인 경우 (원래 구조)
        this = df_or_this
        [print(i.isnull().sum()) for i in [this.train, this.test]]
        null_count = 0
        for i in [this.train, this.test]:
            if i is not None:
                null_count += int(i.isnull().sum().sum())
        return null_count
    

    def null_check(self, df: pd.DataFrame) -> int:
        return int(df.isnull().sum().sum())

    def pclass_ordinal(self, df: DataFrame) -> pd.DataFrame:
        """
        Pclass: 객실 등급 (1, 2, 3)
        - 서열형 척도(ordinal)로 처리합니다.
        - 1등석 > 2등석 > 3등석이므로, 생존률 관점에서 1이 가장 좋고 3이 가장 안 좋습니다.
        - 기존 Pclass를 그대로 사용하되, category 타입으로 변환하여 명시적으로 ordinal임을 표시합니다.
        """
        df = df.copy()
        # Pclass를 category 타입으로 변환 (ordinal 의미 명시)
        df["Pclass"] = df["Pclass"].astype("category")
        return df
    
    def fare_ordinal(self, df: DataFrame) -> pd.DataFrame:
        """
        Fare: 요금 (연속형 ratio 척도이지만, 여기서는 구간화하여 서열형으로 사용)
        - 결측치가 있으면 중앙값으로 채웁니다.
        - Fare를 사분위수로 binning 하여 ordinal 피처를 만듭니다.
        - 원래 Fare 컬럼은 그대로 유지하고, Fare_band 컬럼만 추가합니다.
        """
        df = df.copy()
        # 결측치를 중앙값으로 채우기
        if df["Fare"].isnull().any():
            median_fare = df["Fare"].median()
            df["Fare"].fillna(median_fare, inplace=True)
        
        # 사분위수로 binning (4개 구간)
        df["Fare_band"] = pd.qcut(df["Fare"], q=4, labels=[0, 1, 2, 3], duplicates='drop')
        # qcut이 실패할 경우 (중복값 등) cut으로 대체
        if df["Fare_band"].isnull().any():
            df["Fare_band"] = pd.cut(df["Fare"], bins=4, labels=[0, 1, 2, 3], duplicates='drop')
        df["Fare_band"] = df["Fare_band"].astype("category")
        return df
    
    def embarked_ordinal(self, df: DataFrame) -> pd.DataFrame:
        """
        Embarked: 탑승 항구 (C, Q, S)
        - 본질적으로는 nominal(명목) 척도이므로 one-hot encoding을 사용합니다.
        - 결측치는 가장 많이 등장하는 값으로 채웁니다 (mode).
        - 원래 "Embarked" 컬럼은 유지하고, one-hot 컬럼을 추가합니다.
        """
        df = df.copy()
        # 결측치를 mode로 채우기
        if df["Embarked"].isnull().any():
            mode_embarked = df["Embarked"].mode()[0] if not df["Embarked"].mode().empty else "S"
            df["Embarked"].fillna(mode_embarked, inplace=True)
        
        # one-hot encoding
        embarked_dummies = pd.get_dummies(df["Embarked"], prefix="Embarked")
        df = pd.concat([df, embarked_dummies], axis=1)
        return df
    
    def gender_nominal(self, df: DataFrame) -> pd.DataFrame:
        """
        Gender: 성별 (male, female)
        - nominal 척도입니다.
        - male을 0, female을 1로 매핑합니다.
        - "Sex" 컬럼을 "Gender" 컬럼으로 변환합니다 (0 또는 1 값).
        """
        df = df.copy()
        # male을 0, female을 1로 매핑
        df["Gender"] = df["Sex"].map({"male": 0, "female": 1})
        # Sex 컬럼 제거
        df = df.drop(columns=["Sex"])
        return df
    
    def age_ratio(self, df: DataFrame) -> pd.DataFrame:
        """
        Age: 나이
        - 원래는 ratio 척도지만, 나이를 구간으로 나눈 ordinal 피처를 만듭니다.
        - Age 결측치는 중앙값으로 채웁니다.
        - bins를 사용해서 나이를 구간화합니다.
        - 원본 Age 컬럼은 유지하고, Age_band 컬럼을 추가합니다.
        
        bins 의미:
        - (-1, 0]: 미출생/신생아
        - (0, 5]: 유아
        - (5, 12]: 어린이
        - (12, 18]: 청소년
        - (18, 24]: 청년
        - (24, 35]: 성인 초기
        - (35, 60]: 성인
        - (60, inf]: 노년
        """
        df = df.copy()
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = ["infant", "toddler", "child", "teen", "young_adult", "adult", "middle_age", "senior"]
        
        # 결측치를 중앙값으로 채우기
        if df["Age"].isnull().any():
            median_age = df["Age"].median()
            df["Age"].fillna(median_age, inplace=True)
        
        # 나이를 구간화
        df["Age_band"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)
        df["Age_band"] = df["Age_band"].astype("category")
        # 수치형 인덱스도 추가 (0부터 시작)
        df["Age_band_ordinal"] = pd.cut(df["Age"], bins=bins, labels=False, right=True)
        return df
    
    def title_nominal(self, df: DataFrame) -> pd.DataFrame:
        """
        Title: 명칭 (Mr, Mrs, Miss, Master, Dr, etc.)
        - Name 컬럼에서 추출한 타이틀입니다.
        - nominal 척도입니다.
        - 희소한 타이틀은 "Rare" 그룹으로 묶습니다.
        - one-hot encoding으로 변환합니다.
        """
        df = df.copy()
        # Name에서 Title 추출 (예: "Braund, Mr. Owen Harris" -> "Mr")
        df["Title"] = df["Name"].str.extract(r',\s*([^\.]+)\.', expand=False)
        
        # 희소한 타이틀을 "Rare"로 묶기
        # 일반적인 타이틀: Mr, Mrs, Miss, Master
        # 그 외는 Rare로 처리
        common_titles = ["Mr", "Mrs", "Miss", "Master"]
        df["Title"] = df["Title"].apply(lambda x: x if x in common_titles else "Rare")
        
        # 결측치 처리 (혹시 모를 경우를 대비)
        if df["Title"].isnull().any():
            df["Title"].fillna("Rare", inplace=True)
        
        # one-hot encoding
        title_dummies = pd.get_dummies(df["Title"], prefix="Title")
        df = pd.concat([df, title_dummies], axis=1)
        return df