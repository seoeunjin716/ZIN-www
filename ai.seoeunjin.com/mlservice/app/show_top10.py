"""
Titanic 데이터셋의 상위 10명을 출력하는 스크립트
"""
import pandas as pd
from pathlib import Path

# 현재 파일의 디렉토리 경로
current_dir = Path(__file__).parent

# train.csv 파일 경로
csv_path = current_dir / "train.csv"

def show_top10_passengers():
    """train.csv 파일의 상위 10명 승객 정보를 출력합니다."""
    try:
        # CSV 파일 읽기
        df = pd.read_csv(csv_path)
        
        # 상위 10명 출력
        print("\n" + "="*100)
        print("타이타닉 승객 상위 10명")
        print("="*100 + "\n")
        
        top10 = df.head(10)
        
        # 보기 좋게 출력
        for idx, row in top10.iterrows():
            print(f"[{idx + 1}번째 승객]")
            print(f"  이름: {row['Name']}")
            print(f"  성별: {row['Sex']}")
            print(f"  나이: {row['Age']}")
            print(f"  객실 등급: {row['Pclass']}")
            print(f"  생존 여부: {'생존' if row['Survived'] == 1 else '사망'}")
            print(f"  요금: ${row['Fare']}")
            print(f"  승선 항구: {row['Embarked']}")
            print("-" * 100)
        
        print(f"\n전체 승객 수: {len(df)}명")
        print(f"생존자 수: {df['Survived'].sum()}명")
        print(f"사망자 수: {len(df) - df['Survived'].sum()}명\n")
        
    except FileNotFoundError:
        print(f"오류: {csv_path} 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    show_top10_passengers()

