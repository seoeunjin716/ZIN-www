import shutil
from pathlib import Path


def save_file_to_yolo_data(source_path: str, file_name: str = None) -> bool:
    """
    파일을 app/data/yolo 폴더로 저장

    Args:
        source_path: 소스 파일 경로
        file_name: 저장할 파일명 (None이면 원본 파일명 사용)

    Returns:
        bool: 성공 여부
    """
    source_path_obj = Path(source_path)

    # 소스 파일이 존재하는지 확인
    if not source_path_obj.exists():
        print(f"❌ 소스 파일을 찾을 수 없습니다: {source_path}")
        return False

    # 현재 파일의 위치를 기준으로 상대 경로 계산
    # main.py 위치: cv.seoeunjin.com/app/yolo/main.py
    # 대상 폴더: cv.seoeunjin.com/app/data/yolo
    current_file = Path(__file__).resolve()
    base_dir = current_file.parent.parent.parent  # cv.seoeunjin.com
    target_dir = base_dir / "app" / "data" / "yolo"

    # 대상 폴더가 없으면 생성
    target_dir.mkdir(parents=True, exist_ok=True)

    # 저장할 파일명 결정
    if file_name:
        target_file_name = file_name
    else:
        target_file_name = source_path_obj.name

    # 대상 파일 경로
    target_path = target_dir / target_file_name

    try:
        # 파일 복사 (원본은 유지)
        shutil.copy2(str(source_path_obj), str(target_path))
        print(f"✅ 파일 저장 완료!")
        print(f"   소스: {source_path}")
        print(f"   대상: {target_path}")
        return True
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {e}")
        return False


def move_image_to_yolo_data():
    """
    Downloads 폴더의 family.jpg를 app/data/yolo 폴더로 이동 (기존 함수 유지)
    """
    source_path = Path(r"C:\Users\hi\Downloads\family.jpg")

    if not source_path.exists():
        print(f"❌ 소스 파일을 찾을 수 없습니다: {source_path}")
        return False

    return save_file_to_yolo_data(str(source_path), "family.jpg")


if __name__ == "__main__":
    move_image_to_yolo_data()
