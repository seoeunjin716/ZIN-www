#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
서울시 경찰서/파출소 정보 CSV 파일 생성 스크립트
"""
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.seoul_crime.seoul_service import SeoulService

if __name__ == "__main__":
    print("=" * 50)
    print("서울시 경찰서/파출소 정보 수집 시작")
    print("=" * 50)
    
    try:
        service = SeoulService()
        result = service.save_police_stations_info('police_stations.csv')
        print(f"\n✅ 파일 생성 완료: {result}")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

