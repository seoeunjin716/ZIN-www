import sys
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any, Optional

from .seoul_method import SeoulMethod
from .seoul_data import SeoulData
from .kakao_map_singletone import KakaoMapSingleton

class SeoulService(object):

    def __init__(self):
        self.the_method = SeoulMethod()
        self.data = SeoulData()
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        self.logger = logging.getLogger(__name__)
        
        # 데이터 저장용
        self.cctv_df = None
        self.crime_df = None
        self.pop_df = None
        self.cctv_pop_df = None
        
        # 모델 관련
        self.model = None
        self.models = {}
        self.model_scores = {}
        self.best_model_name = None
    
    def preprocess(self) -> Dict[str, Any]:
        """
        Seoul 데이터 로드 및 전처리
        """
        try:
            self.logger.info("=== Seoul 데이터 전처리 시작 ===")
            
            # 데이터 로드
            self.cctv_df = self.data.cctv
            self.crime_df = self.data.crime
            self.pop_df = self.data.pop
            
            self.logger.info(f"CCTV 데이터 shape: {self.cctv_df.shape}")
            self.logger.info(f"Crime 데이터 shape: {self.crime_df.shape}")
            self.logger.info(f"Population 데이터 shape: {self.pop_df.shape}")
            
            # CCTV 컬럼 삭제: '2013년도 이전', '2014년', '2015년', '2016년' 제거
            self.cctv_df = self.cctv_df.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1)
            self.logger.info(f"CCTV 컬럼 삭제 후 shape: {self.cctv_df.shape}")
            self.logger.info(f"CCTV 컬럼: {list(self.cctv_df.columns)}")
            
            # pop 컬럼 편집: axis = 1 방향으로 자치구와 좌로부터 4번째 컬럼만 남기고 모두 삭제
            # 컬럼명 확인
            pop_columns = list(self.pop_df.columns)
            self.logger.info(f"POP 원본 컬럼: {pop_columns}")
            
            # 자치구 컬럼 찾기 (인덱스 1)
            # 좌로부터 4번째 컬럼 = 인덱스 3
            if len(pop_columns) >= 4:
                # 자치구와 4번째 컬럼(인덱스 3)만 남기기
                keep_columns = [pop_columns[1], pop_columns[3]]  # 자치구, 4번째 컬럼
                self.pop_df = self.pop_df[keep_columns]
                self.logger.info(f"POP 컬럼 편집 후 shape: {self.pop_df.shape}")
                self.logger.info(f"POP 남은 컬럼: {list(self.pop_df.columns)}")
            else:
                self.logger.warning(f"POP 데이터의 컬럼이 4개 미만입니다. 원본 유지: {pop_columns}")
            
            # 컬럼명 확인 및 중복 컬럼 체크
            cctv_cols = set(self.cctv_df.columns)
            pop_cols = set(self.pop_df.columns)
            common_cols = cctv_cols & pop_cols
            if common_cols:
                self.logger.info(f"중복 컬럼 발견: {common_cols}")
            else:
                self.logger.info("중복 컬럼 없음")

            # 터미널에 출력
            print("\n=== CCTV 데이터 ===")
            print(self.cctv_df.head())
            print("\n=== Crime 데이터 ===")
            print(self.crime_df.head())
            print("\n=== Population 데이터 ===")
            print(self.pop_df.head())
            
            # CCTV와 Population 데이터 머지
            self.logger.info("=== CCTV-POP 데이터 머지 시작 ===")
            cctv_pop = self.the_method.df_merge(
                self.cctv_df, 
                self.pop_df, 
                left_key='기관명',   # cctv의 키
                right_key='자치구'   # pop의 키
            )
            
            # 머지 결과 확인
            self.logger.info(f"CCTV-POP 머지 결과 shape: {cctv_pop.shape}")
            self.logger.info(f"CCTV-POP 머지 결과 columns: {list(cctv_pop.columns)}")
            
            # 터미널에 출력
            print("\n=== CCTV-POP 머지 결과 ===")
            print(f"Shape: {cctv_pop.shape}")
            print(f"Columns: {list(cctv_pop.columns)}")
            print(cctv_pop.head())
            
            # 머지된 데이터 저장
            self.cctv_pop_df = cctv_pop
            
            # crime 데이터에 주소와 자치구 추가하여 save 폴더에 저장
            try:
                self.logger.info("=== Crime 데이터에 주소/자치구 추가 및 저장 시작 ===")
                crime_file_path = self.save_crime_with_address("crime_with_address.csv")
                self.logger.info(f"Crime 파일 저장 완료: {crime_file_path}")
            except Exception as e:
                self.logger.warning(f"Crime 파일 저장 중 오류 발생 (전처리는 계속 진행): {str(e)}")
                # 파일 저장 실패해도 전처리는 계속 진행
            
            return {
                "cctv_shape": self.cctv_df.shape,
                "crime_shape": self.crime_df.shape,
                "pop_shape": self.pop_df.shape,
                "cctv_pop_shape": cctv_pop.shape,
                "cctv_columns": list(self.cctv_df.columns),
                "crime_columns": list(self.crime_df.columns),
                "pop_columns": list(self.pop_df.columns),
                "cctv_pop_columns": list(cctv_pop.columns)
            }
        except Exception as e:
            self.logger.error(f"전처리 중 오류: {str(e)}")
            raise

    def modeling(self):
        """모델 초기화 (향후 구현)"""
        pass
    
    def learning(self):
        """모델 학습 (향후 구현)"""
        pass
    
    def evaluation(self):
        """모델 평가 (향후 구현)"""
        pass
    
    def submit(self, model_name: Optional[str] = None) -> str:
        """제출 파일 생성 (향후 구현)"""
        pass
    
    def get_data_as_json(self, data_type: str) -> Dict[str, Any]:
        """
        데이터를 JSON 형식으로 반환
        
        Args:
            data_type: 'cctv', 'crime', 'pop', 'cctv_pop' 중 하나
        
        Returns:
            JSON 형식의 데이터
        """
        if data_type == 'cctv':
            df = self.data.cctv
            if df is None:
                raise ValueError("CCTV 데이터를 찾을 수 없습니다")
        elif data_type == 'crime':
            df = self.data.crime
            if df is None:
                raise ValueError("Crime 데이터를 찾을 수 없습니다")
        elif data_type == 'pop':
            df = self.data.pop
            if df is None:
                raise ValueError("Population 데이터를 찾을 수 없습니다")
        elif data_type == 'cctv_pop':
            # 전처리가 안 되어 있으면 실행
            if self.cctv_pop_df is None:
                self.preprocess()
            df = self.cctv_pop_df
            if df is None:
                raise ValueError("머지된 데이터를 찾을 수 없습니다")
        else:
            raise ValueError(f"알 수 없는 데이터 타입: {data_type}. 사용 가능: 'cctv', 'crime', 'pop', 'cctv_pop'")

        # crime 데이터 타입일 때만 관서명에 따른 경찰서 주소 찾기
        if data_type == 'crime':
            try:
                print("🔥💧 [DEBUG] crime 데이터 처리 시작")
                # 관서명에 따른 경찰서 주소 찾기
                station_names = []  # 경찰서 관서명 리스트
                for name in df['관서명']:
                    station_names.append('서울' + str(name[:-1]) + '경찰서')
                print(f"🔥💧경찰서 관서명 리스트: {station_names}")
                
                station_addrs = []
                station_lats = []
                station_lngs = []
                
                print("🔥💧 [DEBUG] KakaoMapSingleton 초기화 시작")
                try:
                    gmaps1 = KakaoMapSingleton()
                    gmaps2 = KakaoMapSingleton()
                    if gmaps1 is gmaps2:
                        print("동일한 객체 입니다.")
                    else:
                        print("다른 객체 입니다.")
                    gmaps = KakaoMapSingleton()  # 카카오맵 객체 생성
                    print("🔥💧 [DEBUG] KakaoMapSingleton 초기화 완료")
                except Exception as e:
                    print(f"🔥💧 [ERROR] KakaoMapSingleton 초기화 실패: {str(e)}")
                    self.logger.error(f"KakaoMapSingleton 초기화 실패: {str(e)}")
                    raise
                
                print(f"🔥💧 [DEBUG] 경찰서 주소 검색 시작 (총 {len(station_names)}개)")
                for i, name in enumerate(station_names):
                    try:
                        print(f"🔥💧 [DEBUG] {i+1}/{len(station_names)}: {name} 검색 중...")
                        tmp = gmaps.geocode(name, language='ko')
                        if tmp and len(tmp) > 0:
                            print(f"""{name}의 검색 결과: {tmp[0].get("formatted_address")}""")
                            station_addrs.append(tmp[0].get("formatted_address"))
                            tmp_loc = tmp[0].get("geometry")
                            station_lats.append(tmp_loc['location']['lat'])
                            station_lngs.append(tmp_loc['location']['lng'])
                        else:
                            print(f"""{name}의 검색 결과를 찾을 수 없습니다.""")
                            station_addrs.append("")
                            station_lats.append(0.0)
                            station_lngs.append(0.0)
                    except Exception as e:
                        print(f"🔥💧 [ERROR] {name} 검색 중 오류: {str(e)}")
                        self.logger.error(f"{name} 검색 중 오류: {str(e)}")
                        station_addrs.append("")
                        station_lats.append(0.0)
                        station_lngs.append(0.0)
                
                print(f"🔥💧자치구 리스트: {station_addrs}")
                print(f"🔥💧위도 리스트: {station_lats}")
                print(f"🔥💧경도 리스트: {station_lngs}")
                gu_names = []
                for addr in station_addrs:
                    if addr:
                        tmp = addr.split()
                        tmp_gu = [gu for gu in tmp if gu[-1] == '구']
                        if tmp_gu:
                            gu_names.append(tmp_gu[0])
                        else:
                            gu_names.append("")
                    else:
                        gu_names.append("")
                print(f"🔥💧자치구 리스트 2: {gu_names}")
                df['자치구'] = gu_names
                df['위도'] = station_lats
                df['경도'] = station_lngs
                print("🔥💧 [DEBUG] crime 데이터 처리 완료")
                print(f"🔥💧 [DEBUG] DataFrame에 추가된 컬럼: 자치구, 위도, 경도")
            except Exception as e:
                print(f"🔥💧 [ERROR] crime 데이터 처리 중 오류 발생: {str(e)}")
                self.logger.error(f"crime 데이터 처리 중 오류: {str(e)}")
                import traceback
                print(f"🔥💧 [ERROR] Traceback: {traceback.format_exc()}")
                # 에러가 발생해도 계속 진행 (자치구 컬럼 없이 반환)
                pass

        
        # NaN, inf, -inf 값을 JSON 호환 가능한 값으로 변환
        df_clean = df.copy()
        df_clean = df_clean.replace([float('inf'), float('-inf')], None)
        df_clean = df_clean.where(pd.notnull(df_clean), None)
        
        # 터미널에 출력
        print(f"\n=== {data_type.upper()} 데이터 ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(df_clean.head())
        
        return {
            "shape": list(df.shape),
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "data": df_clean.to_dict(orient='records'),
            "head": df_clean.head(5).to_dict(orient='records')
        }
    
    def save_crime_with_address(self, filename: str = "crime_with_address.csv") -> str:
        """
        crime.csv에 주소와 자치구 컬럼을 추가하여 save 폴더에 CSV 파일로 저장
        
        Args:
            filename: 저장할 파일명 (기본값: "crime_with_address.csv")
        
        Returns:
            저장된 파일의 전체 경로
        """
        try:
            self.logger.info("=== Crime 데이터에 주소/자치구 추가 및 저장 시작 ===")
            
            # crime 데이터 로드
            df = self.data.crime.copy()
            if df is None:
                raise ValueError("Crime 데이터를 찾을 수 없습니다")
            
            print("🔥💧 [DEBUG] crime 데이터 처리 시작")
            print(f"🔥💧 [DEBUG] 원본 관서명 샘플: {df['관서명'].head().tolist()}")
            
            # 관서명을 '서울XX경찰서' 형식으로 변환
            # 예: '중부서' -> '서울중부경찰서', '종로서' -> '서울종로경찰서'
            def convert_station_name(name):
                name_str = str(name).strip()
                if name_str.endswith('서'):
                    converted = '서울' + name_str[:-1] + '경찰서'
                    return converted
                return name_str
            
            # 관서명 변환 적용
            df['관서명'] = df['관서명'].apply(convert_station_name)
            print(f"🔥💧 [DEBUG] 변환된 관서명 샘플: {df['관서명'].head().tolist()}")
            print(f"🔥💧 [DEBUG] 변환 확인 - 첫 번째 관서명: {df['관서명'].iloc[0]}")
            
            # 관서명에 따른 경찰서 주소 찾기
            station_names = df['관서명'].tolist()  # 경찰서 관서명 리스트
            print(f"🔥💧경찰서 관서명 리스트: {station_names}")
            
            station_addrs = []
            station_lats = []
            station_lngs = []
            
            print("🔥💧 [DEBUG] KakaoMapSingleton 초기화 시작")
            try:
                gmaps = KakaoMapSingleton()  # 카카오맵 객체 생성
                print("🔥💧 [DEBUG] KakaoMapSingleton 초기화 완료")
            except Exception as e:
                print(f"🔥💧 [ERROR] KakaoMapSingleton 초기화 실패: {str(e)}")
                self.logger.error(f"KakaoMapSingleton 초기화 실패: {str(e)}")
                raise
            
            print(f"🔥💧 [DEBUG] 경찰서 주소 검색 시작 (총 {len(station_names)}개)")
            for i, name in enumerate(station_names):
                try:
                    print(f"🔥💧 [DEBUG] {i+1}/{len(station_names)}: {name} 검색 중...")
                    tmp = gmaps.geocode(name, language='ko')
                    if tmp and len(tmp) > 0:
                        print(f"""{name}의 검색 결과: {tmp[0].get("formatted_address")}""")
                        station_addrs.append(tmp[0].get("formatted_address"))
                        tmp_loc = tmp[0].get("geometry")
                        station_lats.append(tmp_loc['location']['lat'])
                        station_lngs.append(tmp_loc['location']['lng'])
                    else:
                        print(f"""{name}의 검색 결과를 찾을 수 없습니다.""")
                        station_addrs.append("")
                        station_lats.append(0.0)
                        station_lngs.append(0.0)
                except Exception as e:
                    print(f"🔥💧 [ERROR] {name} 검색 중 오류: {str(e)}")
                    self.logger.error(f"{name} 검색 중 오류: {str(e)}")
                    station_addrs.append("")
                    station_lats.append(0.0)
                    station_lngs.append(0.0)
            
            print(f"🔥💧자치구 리스트: {station_addrs}")
            print(f"🔥💧위도 리스트: {station_lats}")
            print(f"🔥💧경도 리스트: {station_lngs}")
            
            # 자치구 추출
            gu_names = []
            for addr in station_addrs:
                if addr:
                    tmp = addr.split()
                    tmp_gu = [gu for gu in tmp if gu[-1] == '구']
                    if tmp_gu:
                        gu_names.append(tmp_gu[0])
                    else:
                        gu_names.append("")
                else:
                    gu_names.append("")
            
            print(f"🔥💧자치구 리스트 2: {gu_names}")
            
            # DataFrame에 컬럼 추가
            df['주소'] = station_addrs
            df['자치구'] = gu_names
            df['위도'] = station_lats
            df['경도'] = station_lngs
            
            print("🔥💧 [DEBUG] crime 데이터 처리 완료")
            print(f"🔥💧 [DEBUG] DataFrame에 추가된 컬럼: 주소, 자치구, 위도, 경도")
            
            # 저장 전 관서명 최종 확인 및 강제 변환
            print(f"🔥💧 [DEBUG] 저장 전 관서명 확인: {df['관서명'].head().tolist()}")
            
            # 관서명 강제 변환 (안전장치)
            def force_convert(name):
                name_str = str(name).strip()
                # '서울'로 시작하지 않고 '서'로 끝나면 변환
                if not name_str.startswith('서울') and name_str.endswith('서'):
                    return '서울' + name_str[:-1] + '경찰서'
                # 이미 '서울'로 시작하고 '경찰서'로 끝나면 그대로
                elif name_str.startswith('서울') and name_str.endswith('경찰서'):
                    return name_str
                # '서울'로 시작하지만 '경찰서'가 없으면 추가
                elif name_str.startswith('서울') and not name_str.endswith('경찰서'):
                    if name_str.endswith('서'):
                        return name_str[:-1] + '경찰서'
                    return name_str + '경찰서'
                return name_str
            
            # 강제 변환 적용
            df['관서명'] = df['관서명'].apply(force_convert)
            print(f"🔥💧 [DEBUG] 강제 변환 후 관서명 확인: {df['관서명'].head().tolist()}")
            print(f"🔥💧 [DEBUG] 자치구 확인: {df['자치구'].head().tolist()}")
            
            # save 폴더 경로 확인
            save_path = Path(self.data.sname)
            save_path.mkdir(parents=True, exist_ok=True)
            
            # CSV 파일 저장
            output_file = save_path / filename
            
            # 저장 직전 최종 확인 및 최종 변환 (절대 안전장치)
            print(f"🔥💧 [DEBUG] 저장 직전 최종 관서명 (변환 전): {df['관서명'].iloc[0:5].tolist()}")
            
            # 모든 관서명을 강제로 변환 (inplace)
            for idx in df.index:
                current_name = str(df.at[idx, '관서명']).strip()
                if not current_name.startswith('서울') and current_name.endswith('서'):
                    df.at[idx, '관서명'] = '서울' + current_name[:-1] + '경찰서'
            
            print(f"🔥💧 [DEBUG] 저장 직전 최종 관서명 (변환 후): {df['관서명'].iloc[0:5].tolist()}")
            print(f"🔥💧 [DEBUG] 저장 직전 자치구: {df['자치구'].iloc[0:5].tolist()}")
            
            # 컬럼 순서: 관서명, 자치구, 주소, 위도, 경도, 나머지 컬럼들
            columns_order = ['관서명', '자치구', '주소', '위도', '경도'] + [col for col in df.columns if col not in ['관서명', '자치구', '주소', '위도', '경도']]
            df = df[columns_order]
            
            # 최종 저장 전 한 번 더 확인
            print(f"🔥💧 [DEBUG] 최종 저장 직전 관서명: {df['관서명'].iloc[0:3].values.tolist()}")
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            # 저장 후 검증 - 파일을 다시 읽어서 확인
            import pandas as pd
            saved_df = pd.read_csv(output_file)
            print(f"🔥💧 [DEBUG] 저장 완료! 파일에서 읽은 관서명: {saved_df['관서명'].head().tolist()}")
            
            # 저장 후 검증
            import pandas as pd
            saved_df = pd.read_csv(output_file)
            print(f"🔥💧 [DEBUG] 파일 저장 완료. 저장된 파일의 관서명 샘플: {saved_df['관서명'].head().tolist()}")
            
            self.logger.info(f"파일 저장 완료: {output_file}")
            print(f"🔥💧 [SUCCESS] 파일 저장 완료: {output_file}")
            print(f"🔥💧 [INFO] 저장된 데이터 shape: {df.shape}")
            print(f"🔥💧 [INFO] 저장된 컬럼: {list(df.columns)}")
            
            return str(output_file)
            
        except Exception as e:
            error_msg = f"Crime 데이터 저장 중 오류 발생: {str(e)}"
            self.logger.error(error_msg)
            print(f"🔥💧 [ERROR] {error_msg}")
            import traceback
            print(f"🔥💧 [ERROR] Traceback: {traceback.format_exc()}")
            raise
    
    def save_police_stations_info(self, filename: str = "police_stations.csv") -> str:
        """
        서울시 경찰서와 파출소 정보를 카카오맵 API로 검색하여 CSV 파일로 저장
        
        Args:
            filename: 저장할 파일명 (기본값: "police_stations.csv")
        
        Returns:
            저장된 파일의 전체 경로
        """
        try:
            self.logger.info("=== 서울시 경찰서/파출소 정보 수집 시작 ===")
            
            # 서울시 자치구 목록
            seoul_gu_list = [
                '종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', 
                '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', 
                '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', 
                '서초구', '강남구', '송파구', '강동구'
            ]
            
            # 검색 키워드 목록
            search_keywords = []
            
            # 각 자치구별로 경찰서와 파출소 검색 키워드 생성
            for gu in seoul_gu_list:
                search_keywords.append(f"서울 {gu} 경찰서")
                search_keywords.append(f"서울 {gu} 파출소")
            
            # 추가로 일반적인 경찰서 검색 키워드
            search_keywords.extend([
                "서울 경찰서",
                "서울 파출소",
                "서울중부경찰서", "서울종로경찰서", "서울남대문경찰서", "서울서대문경찰서",
                "서울혜화경찰서", "서울용산경찰서", "서울성북경찰서", "서울동대문경찰서",
                "서울마포경찰서", "서울영등포경찰서", "서울성동경찰서", "서울동작경찰서",
                "서울광진경찰서", "서울서부경찰서", "서울강북경찰서", "서울금천경찰서",
                "서울중랑경찰서", "서울강남경찰서", "서울관악경찰서", "서울강서경찰서",
                "서울강동경찰서", "서울종암경찰서", "서울구로경찰서", "서울서초경찰서",
                "서울양천경찰서", "서울송파경찰서", "서울노원경찰서", "서울방배경찰서",
                "서울은평경찰서", "서울도봉경찰서", "서울수서경찰서"
            ])
            
            print(f"🔥💧 [DEBUG] 총 {len(search_keywords)}개의 키워드로 검색 시작")
            
            # KakaoMapSingleton 초기화
            try:
                gmaps = KakaoMapSingleton()
                print("🔥💧 [DEBUG] KakaoMapSingleton 초기화 완료")
            except Exception as e:
                print(f"🔥💧 [ERROR] KakaoMapSingleton 초기화 실패: {str(e)}")
                self.logger.error(f"KakaoMapSingleton 초기화 실패: {str(e)}")
                raise
            
            # 결과 저장용 리스트
            police_stations = []
            seen_names = set()  # 중복 제거용
            
            # 각 키워드로 검색
            for i, keyword in enumerate(search_keywords):
                try:
                    print(f"🔥💧 [DEBUG] {i+1}/{len(search_keywords)}: '{keyword}' 검색 중...")
                    
                    # 카카오맵 API로 검색 (여러 결과 가져오기)
                    results = gmaps.geocode(keyword, language='ko')
                    
                    if results and len(results) > 0:
                        for result in results:
                            station_name = result.get("name", "")
                            formatted_address = result.get("formatted_address", "")
                            
                            # 중복 제거 (이름과 주소가 모두 같으면 제외)
                            key = (station_name, formatted_address)
                            if key in seen_names:
                                continue
                            seen_names.add(key)
                            
                            # "서울"이 포함된 결과만 수집
                            if "서울" in formatted_address or "서울" in station_name:
                                # 관서명 추출 (경찰서 이름에서)
                                office_name = station_name
                                
                                police_stations.append({
                                    "경찰서이름": station_name,
                                    "경찰서주소": formatted_address,
                                    "관서": office_name
                                })
                                
                                print(f"  ✓ {station_name}: {formatted_address}")
                    
                    # API 호출 제한을 고려한 딜레이 (필요시)
                    # time.sleep(0.1)
                    
                except Exception as e:
                    print(f"🔥💧 [ERROR] '{keyword}' 검색 중 오류: {str(e)}")
                    self.logger.warning(f"'{keyword}' 검색 중 오류: {str(e)}")
                    continue
            
            if not police_stations:
                raise ValueError("경찰서 정보를 찾을 수 없습니다.")
            
            # DataFrame 생성
            df = pd.DataFrame(police_stations)
            
            # 중복 제거 (경찰서이름 기준)
            df = df.drop_duplicates(subset=['경찰서이름'], keep='first')
            
            # 정렬 (경찰서이름 기준)
            df = df.sort_values(by='경찰서이름')
            
            print(f"🔥💧 [DEBUG] 총 {len(df)}개의 경찰서/파출소 정보 수집 완료")
            print(f"🔥💧 [DEBUG] 샘플 데이터:")
            print(df.head(10).to_string())
            
            # save 폴더 경로 확인
            save_path = Path(self.data.sname)
            save_path.mkdir(parents=True, exist_ok=True)
            
            # CSV 파일 저장
            output_file = save_path / filename
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"경찰서 정보 파일 저장 완료: {output_file}")
            print(f"🔥💧 [DEBUG] 파일 저장 완료: {output_file}")
            
            return str(output_file)
            
        except Exception as e:
            self.logger.error(f"경찰서 정보 수집 중 오류 발생: {str(e)}")
            print(f"🔥💧 [ERROR] 경찰서 정보 수집 중 오류: {str(e)}")
            raise
