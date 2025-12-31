import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO


def detect_faces(
    image_path: str, model_path: str = None, conf_threshold: float = 0.25
) -> tuple:
    """
    YOLO를 사용하여 이미지에서 얼굴을 디텍팅

    Args:
        image_path: 입력 이미지 경로
        model_path: YOLO 모델 경로 (None이면 기본 모델 사용)
        conf_threshold: 신뢰도 임계값 (0.0 ~ 1.0)

    Returns:
        tuple: (원본 이미지, 디텍션 결과 이미지, 디텍션 정보 리스트)
               디텍션 정보: [{'bbox': [x1, y1, x2, y2], 'confidence': float}, ...]
    """
    # 이미지 경로 확인
    image_path_obj = Path(image_path)
    if not image_path_obj.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    # 이미지 읽기
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")

    # YOLO 모델 경로 설정
    if model_path is None:
        # 현재 파일 위치 기준으로 모델 경로 찾기
        current_file = Path(__file__).resolve()
        model_dir = current_file.parent
        model_path = model_dir / "yolov8n.pt"

        # YOLOv8 face detection 모델이 없으면 일반 모델 사용
        # (실제로는 face detection 전용 모델을 다운로드해야 함)
        if not model_path.exists():
            print("⚠️ 로컬 모델을 찾을 수 없습니다. YOLOv8 기본 모델을 다운로드합니다.")
            model = YOLO("yolov8n.pt")
        else:
            model = YOLO(str(model_path))
    else:
        model = YOLO(str(model_path))

    # YOLO 디텍션 실행
    # 'person' 클래스를 디텍션 (얼굴은 person 내부에 있음)
    results = model(image, conf=conf_threshold, classes=[0])  # class 0 = person

    # 결과 이미지 복사
    result_image = image.copy()

    # 얼굴 디텍션 정보 저장
    detections = []

    # 디텍션 결과 처리
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 바운딩 박스 좌표
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # 신뢰도
            confidence = float(box.conf[0].cpu().numpy())

            # person 영역에서 얼굴 영역 추정 (상단 1/3 부분)
            face_height = int((y2 - y1) * 0.4)  # 얼굴은 상단 40% 정도
            face_y1 = y1
            face_y2 = y1 + face_height
            face_x1 = x1
            face_x2 = x2

            # 얼굴 영역 그리기
            cv2.rectangle(
                result_image, (face_x1, face_y1), (face_x2, face_y2), (0, 255, 0), 2
            )

            # 신뢰도 텍스트
            label = f"Face {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(
                result_image,
                (face_x1, face_y1 - label_size[1] - 10),
                (face_x1 + label_size[0], face_y1),
                (0, 255, 0),
                -1,
            )
            cv2.putText(
                result_image,
                label,
                (face_x1, face_y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                2,
            )

            # 디텍션 정보 저장
            detections.append(
                {
                    "bbox": [face_x1, face_y1, face_x2, face_y2],
                    "confidence": confidence,
                    "person_bbox": [int(x1), int(y1), int(x2), int(y2)],
                }
            )

    return image, result_image, detections


def detect_faces_with_haar_cascade(image_path: str) -> tuple:
    """
    OpenCV Haar Cascade를 사용하여 얼굴 디텍션 (대안 방법)

    Args:
        image_path: 입력 이미지 경로

    Returns:
        tuple: (원본 이미지, 디텍션 결과 이미지, 디텍션 정보 리스트)
    """
    # 이미지 읽기
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")

    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Haar Cascade 얼굴 디텍터 로드
    # OpenCV에 포함된 기본 얼굴 디텍터 사용
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # 얼굴 디텍션
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # 결과 이미지 복사
    result_image = image.copy()
    detections = []

    # 디텍션 결과 그리기
    for x, y, w, h in faces:
        # 얼굴 영역 그리기
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 레이블
        label = "Face"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(
            result_image,
            (x, y - label_size[1] - 10),
            (x + label_size[0], y),
            (0, 255, 0),
            -1,
        )
        cv2.putText(
            result_image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2
        )

        # 디텍션 정보 저장
        detections.append(
            {
                "bbox": [x, y, x + w, y + h],
                "confidence": 1.0,  # Haar Cascade는 신뢰도 제공 안 함
            }
        )

    return image, result_image, detections


def process_image_file(image_path: str, use_haar: bool = False) -> str:
    """
    이미지 파일을 처리하여 얼굴 디텍션 결과를 저장

    Args:
        image_path: 입력 이미지 경로
        use_haar: True면 Haar Cascade 사용, False면 YOLO 사용

    Returns:
        str: 저장된 결과 파일 경로
    """
    image_path_obj = Path(image_path)

    # 이미지 파일인지 확인
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    if image_path_obj.suffix.lower() not in valid_extensions:
        raise ValueError(f"지원하지 않는 이미지 형식입니다: {image_path_obj.suffix}")

    # 이미 처리된 파일인지 확인 (이미 -detected가 포함된 파일은 제외)
    if "-detected" in image_path_obj.stem:
        return None

    print(f"📷 이미지 처리 시작: {image_path_obj.name}")

    try:
        if use_haar:
            original, result, detections = detect_faces_with_haar_cascade(
                str(image_path)
            )
        else:
            original, result, detections = detect_faces(str(image_path))

        # 결과 파일 경로 생성: 원본파일명-detected.확장자
        output_path = (
            image_path_obj.parent
            / f"{image_path_obj.stem}-detected{image_path_obj.suffix}"
        )

        # 결과 이미지 저장
        cv2.imwrite(str(output_path), result)

        print(f"✅ 디텍션 완료: {len(detections)}개의 얼굴 발견")
        print(f"   결과 저장: {output_path.name}")

        return str(output_path)

    except Exception as e:
        print(f"❌ 이미지 처리 중 오류 발생: {e}")
        import traceback

        traceback.print_exc()
        return None


def main():
    """
    메인 함수: 3333.jpg 이미지에서 얼굴 디텍션
    """
    # 현재 파일 위치 기준으로 이미지 경로 찾기
    current_file = Path(__file__).resolve()
    base_dir = current_file.parent.parent.parent  # cv.seoeunjin.com
    image_path = base_dir / "app" / "data" / "yolo" / "3333.jpg"

    if not image_path.exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return

    print(f"📷 이미지 로드: {image_path}")

    try:
        # 방법 1: YOLO를 사용한 얼굴 디텍션
        print("\n🔍 YOLO를 사용한 얼굴 디텍션 시작...")
        original, result, detections = detect_faces(str(image_path))

        print(f"✅ {len(detections)}개의 얼굴을 디텍션했습니다.")
        for i, det in enumerate(detections, 1):
            print(
                f"   얼굴 {i}: bbox={det['bbox']}, confidence={det['confidence']:.2f}"
            )

        # 결과 저장
        output_path = process_image_file(str(image_path))

        # 방법 2: Haar Cascade를 사용한 얼굴 디텍션 (대안)
        print("\n🔍 Haar Cascade를 사용한 얼굴 디텍션 시작...")
        original2, result2, detections2 = detect_faces_with_haar_cascade(
            str(image_path)
        )

        print(f"✅ {len(detections2)}개의 얼굴을 디텍션했습니다.")
        for i, det in enumerate(detections2, 1):
            print(f"   얼굴 {i}: bbox={det['bbox']}")

        # 결과 저장
        output_path2 = process_image_file(str(image_path), use_haar=True)

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
