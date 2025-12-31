"""
폴더 감시 스크립트: app/data/yolo 폴더에 새 이미지가 추가되면 자동으로 얼굴 디텍션 실행
watchdog 없이 polling 방식으로 작동
"""

import time
from pathlib import Path
from yolo_detection import process_image_file


def get_image_files(folder: Path):
    """폴더에서 이미지 파일 목록 가져오기"""
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    image_files = []

    for ext in valid_extensions:
        image_files.extend(list(folder.glob(f"*{ext}")))
        image_files.extend(list(folder.glob(f"*{ext.upper()}")))

    return image_files


def is_file_ready(file_path: Path, max_wait: float = 2.0) -> bool:
    """
    파일이 완전히 쓰여졌는지 확인

    Args:
        file_path: 확인할 파일 경로
        max_wait: 최대 대기 시간 (초)

    Returns:
        bool: 파일이 준비되었는지 여부
    """
    if not file_path.exists():
        return False

    file_size = -1
    check_count = 0
    max_checks = int(max_wait * 10)  # 0.1초 간격으로 확인

    while check_count < max_checks:
        try:
            current_size = file_path.stat().st_size
            if current_size == file_size and current_size > 0:
                # 파일 크기가 안정적이고 0보다 크면 준비됨
                return True
            file_size = current_size
            time.sleep(0.1)
            check_count += 1
        except (OSError, FileNotFoundError):
            time.sleep(0.1)
            check_count += 1
            continue

    # 최대 대기 시간 후에도 파일이 존재하고 크기가 0보다 크면 준비된 것으로 간주
    return file_path.exists() and file_path.stat().st_size > 0


def watch_folder(folder_path: str = None, check_interval: float = 1.0):
    """
    폴더 감시 시작 (polling 방식)

    Args:
        folder_path: 감시할 폴더 경로 (None이면 app/data/yolo 사용)
        check_interval: 폴더 확인 간격 (초)
    """
    if folder_path is None:
        # 현재 파일 위치 기준으로 폴더 경로 찾기
        current_file = Path(__file__).resolve()
        base_dir = current_file.parent.parent.parent  # cv.seoeunjin.com
        watch_dir = base_dir / "app" / "data" / "yolo"
    else:
        watch_dir = Path(folder_path)

    if not watch_dir.exists():
        print(f"❌ 감시할 폴더가 존재하지 않습니다: {watch_dir}")
        print(f"   폴더를 생성합니다...")
        watch_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 폴더 감시 시작: {watch_dir}")
    print(f"   새 이미지 파일이 추가되면 자동으로 얼굴 디텍션을 실행합니다.")
    print(f"   확인 간격: {check_interval}초")
    print(f"   종료하려면 Ctrl+C를 누르세요.\n")

    # 이미 처리된 파일 추적
    processed_files = set()

    try:
        # 기존 파일들 확인
        print("📋 기존 이미지 파일 확인 중...")
        existing_images = get_image_files(watch_dir)
        for img_file in existing_images:
            if "-detected" not in img_file.stem:
                print(f"   발견: {img_file.name} (처리 안 됨)")

        print(f"\n⏳ 새 파일을 기다리는 중... (매 {check_interval}초마다 확인)\n")

        # 무한 루프로 폴더 감시
        while True:
            # 현재 폴더의 이미지 파일 목록 가져오기
            current_images = get_image_files(watch_dir)

            for img_file in current_images:
                # 이미 처리된 파일이거나 결과 파일이면 무시
                if "-detected" in img_file.stem:
                    continue

                file_key = str(img_file)

                # 아직 처리하지 않은 파일인지 확인
                if file_key not in processed_files:
                    # 파일이 완전히 쓰여졌는지 확인
                    if is_file_ready(img_file):
                        print(f"\n🆕 새 이미지 파일 감지: {img_file.name}")
                        processed_files.add(file_key)

                        # 얼굴 디텍션 실행
                        try:
                            result_path = process_image_file(str(img_file))
                            if result_path:
                                print(f"✅ 처리 완료: {Path(result_path).name}\n")
                        except Exception as e:
                            print(f"❌ 처리 실패: {e}\n")

            # 다음 확인까지 대기
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n\n🛑 폴더 감시를 중지합니다...")

    print("✅ 종료되었습니다.")


if __name__ == "__main__":
    watch_folder()
