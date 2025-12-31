import requests
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class KakaoMapConfig(BaseSettings):
    """카카오맵 API 설정"""
    kakao_rest_api_key: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class KakaoMapSingleton:
    _instance = None  # 싱글턴 인스턴스를 저장할 클래스 변수

    def __new__(cls):
        if cls._instance is None:  # 인스턴스가 없으면 생성
            cls._instance = super(KakaoMapSingleton, cls).__new__(cls)
            cls._instance._api_key = cls._instance._retrieve_api_key()  # API 키 가져오기
            cls._instance._base_url = "https://dapi.kakao.com/v2/local"  # 카카오맵 API 기본 URL
        return cls._instance  # 기존 인스턴스 반환

    def _retrieve_api_key(self):
        """API 키를 환경 변수에서 가져오는 내부 메서드"""
        # Docker Compose의 env_file 설정으로 .env 파일의 환경 변수가 자동으로 로드됨
        # 따라서 os.getenv로 직접 읽으면 됨
        
        # 정확한 변수명으로 먼저 시도
        api_key = os.getenv("KAKAO_REST_API_KEY", "")
        
        # 오타된 변수명도 지원 (KET -> KEY)
        if not api_key or not api_key.strip():
            api_key = os.getenv("KAKAO_REST_API_KET", "")
            if api_key and api_key.strip():
                print("⚠️ [WARNING] KAKAO_REST_API_KET를 사용 중입니다. KAKAO_REST_API_KEY로 변경해주세요.")
        
        if api_key and api_key.strip():
            return api_key.strip()
        
        # 환경 변수에 없으면 .env 파일에서 직접 읽기 시도 (로컬 개발용)
        try:
            # 루트 디렉토리 찾기 (프로젝트 루트)
            current_file = Path(__file__)
            # 컨테이너 내부: /app/app/seoul_crime/kakao_map_singletone.py
            # 로컬: ai.seoeunjin.com/mlservice/app/seoul_crime/kakao_map_singletone.py
            
            # 컨테이너 내부에서는 /app이 루트이므로 .env 파일이 없을 수 있음
            # 로컬 개발 환경을 위한 fallback
            root_dir = current_file.parent.parent.parent.parent.parent
            
            # .env 파일 경로
            env_file = root_dir / ".env"
            
            if env_file.exists():
                # pydantic_settings로 .env 파일 읽기
                config = KakaoMapConfig(_env_file=str(env_file))
                api_key = config.kakao_rest_api_key
                
                if api_key and api_key.strip():
                    return api_key.strip()
        except Exception as e:
            # .env 파일 읽기 실패는 무시 (환경 변수에서 이미 시도했으므로)
            pass
        
        raise ValueError("KAKAO_REST_API_KEY가 환경 변수나 .env 파일에 설정되지 않았습니다.")

    def get_api_key(self):
        """저장된 API 키 반환"""
        return self._api_key

    def geocode(self, address, language='ko'):
        """
        주소 또는 키워드를 위도, 경도로 변환하는 메서드 (Google Maps API와 호환)
        
        Args:
            address: 검색할 주소 또는 키워드 (예: "서울중부경찰서")
            language: 언어 (기본값: 'ko')
        
        Returns:
            Google Maps API와 유사한 형식의 응답 리스트
        """
        # 먼저 키워드 검색 시도 (장소명 검색용)
        keyword_url = f"{self._base_url}/search/keyword.json"
        headers = {
            "Authorization": f"KakaoAK {self._api_key}"
        }
        keyword_params = {
            "query": address,
            "size": 15  # 최대 15개 결과 가져오기
        }
        
        try:
            # 키워드 검색 시도
            response = requests.get(keyword_url, headers=headers, params=keyword_params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'documents' in data and len(data['documents']) > 0:
                for doc in data['documents']:
                    # 키워드 검색 결과 처리
                    place_name = doc.get('place_name', '')
                    address_name = doc.get('address_name', '')
                    road_address = doc.get('road_address', {})
                    road_address_name = road_address.get('address_name', '') if isinstance(road_address, dict) else ''
                    
                    # 주소 우선순위: 도로명 주소 > 지번 주소 > 장소명
                    formatted_address = road_address_name or address_name or place_name
                    
                    result = {
                        "name": place_name,  # 장소명 추가
                        "formatted_address": formatted_address,
                        "geometry": {
                            "location": {
                                "lat": float(doc.get('y', 0)),  # 위도
                                "lng": float(doc.get('x', 0))   # 경도
                            },
                            "location_type": "ROOFTOP"
                        },
                        "address_components": [
                            {
                                "long_name": formatted_address,
                                "short_name": formatted_address,
                                "types": ["establishment"]
                            }
                        ]
                    }
                    results.append(result)
                
                if results:
                    return results  # 키워드 검색 성공 시 결과 반환
            
            # 키워드 검색 실패 시 주소 검색 시도
            address_url = f"{self._base_url}/search/address.json"
            address_params = {
                "query": address
            }
            
            response = requests.get(address_url, headers=headers, params=address_params)
            response.raise_for_status()
            data = response.json()
            
            if 'documents' in data and len(data['documents']) > 0:
                for doc in data['documents']:
                    # 주소 정보 (도로명 주소 우선, 없으면 지번 주소)
                    road_address = doc.get('road_address', {})
                    address = doc.get('address', {})
                    
                    # 주소명 추출
                    road_address_name = road_address.get('address_name', '') if isinstance(road_address, dict) else ''
                    address_name = address.get('address_name', '') if isinstance(address, dict) else ''
                    formatted_address = road_address_name or address_name
                    
                    result = {
                        "name": formatted_address,  # 장소명 (주소 검색의 경우 주소가 이름)
                        "formatted_address": formatted_address,
                        "geometry": {
                            "location": {
                                "lat": float(doc.get('y', 0)),  # 위도
                                "lng": float(doc.get('x', 0))   # 경도
                            },
                            "location_type": "ROOFTOP" if road_address else "APPROXIMATE"
                        },
                        "address_components": [
                            {
                                "long_name": formatted_address,
                                "short_name": formatted_address,
                                "types": ["street_address"]
                            }
                        ]
                    }
                    results.append(result)
            
            return results
        except requests.exceptions.RequestException as e:
            # 에러 발생 시 상세 로그 출력
            print(f"🔥💧 [ERROR] 카카오맵 API 요청 실패: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"🔥💧 [ERROR] 응답 상태 코드: {e.response.status_code}")
                print(f"🔥💧 [ERROR] 응답 내용: {e.response.text}")
            # 에러 발생 시 빈 리스트 반환 (Google Maps API와 동일하게)
            return []

