import numpy as np
import pandas as pd
from pandas import DataFrame
import logging
from app.seoul_crime.seoul_data import SeoulData

logger = logging.getLogger(__name__)

class SeoulMethod(object):

    def __init__(self):
        self.dataset = SeoulData()

    def csv_to_df(self, fname: str) -> pd.DataFrame:
        return pd.read_csv(fname)

    def xlsx_to_df(self, fname: str) -> pd.DataFrame:
        """xlsx 파일을 데이터프레임으로 변환"""
        return pd.read_excel(fname)

    def cctv_pop_merge(self, a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
        return pd.merge(a, b, on='구별', how='left')

    def df_merge(self, left_df: pd.DataFrame, right_df: pd.DataFrame, 
                 left_key: str, right_key: str = None) -> pd.DataFrame:
        """
        두 DataFrame을 머지
        
        Args:
            left_df: 왼쪽 DataFrame (cctv)
            right_df: 오른쪽 DataFrame (pop)
            left_key: 왼쪽 키 컬럼명 ('기관명')
            right_key: 오른쪽 키 컬럼명 ('자치구'), None이면 left_key와 동일
        
        Returns:
            머지된 DataFrame
        """
        # 1. 키 컬럼 정규화
        left_df = left_df.copy()
        right_df = right_df.copy()
        
        left_df[left_key] = left_df[left_key].astype(str).str.strip()
        if right_key:
            right_df[right_key] = right_df[right_key].astype(str).str.strip()
        else:
            right_key = left_key
        
        # 2. 통일된 키 컬럼명으로 변경
        left_df = left_df.rename(columns={left_key: '구별'})
        right_df = right_df.rename(columns={right_key: '구별'})
        
        # 3. 중복 컬럼 확인 및 제거
        common_cols = set(left_df.columns) & set(right_df.columns)
        common_cols.discard('구별')  # 키 컬럼은 제외
        
        if common_cols:
            logger.warning(f"중복 컬럼 발견: {common_cols}")
            # 오른쪽 DataFrame의 중복 컬럼 제거
            right_df = right_df.drop(columns=list(common_cols))
        
        # 4. 머지 실행
        merged = pd.merge(left_df, right_df, on='구별', how='inner')
        
        # 5. 머지 결과 확인
        logger.info(f"머지 전 - CCTV: {len(left_df)}개, POP: {len(right_df)}개")
        logger.info(f"머지 후 - {len(merged)}개 (매칭 성공)")
        
        if len(merged) < len(left_df):
            unmatched = set(left_df['구별']) - set(merged['구별'])
            logger.warning(f"매칭 실패한 구: {unmatched}")
        
        return merged


    