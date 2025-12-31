import cv2
import os


class FaceDetect:
    def __init__(self):
        # 현재 파일의 디렉토리 경로를 기준으로 cascade 파일 경로 설정
        # app/opencv/face_detect.py -> app/data/opencv/haarcascade_frontalface_alt.xml
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cascade_path = os.path.join(
            current_dir, "..", "data", "opencv", "haarcascade_frontalface_alt.xml"
        )
        self._cascade = os.path.normpath(cascade_path)

    def read_file(self, image_path=None):
        cascade = cv2.CascadeClassifier(self._cascade)

        # 이미지 경로 설정 (기본값: app/data/opencv/girl.jpg)
        if image_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "data", "opencv", "girl.jpg")
            image_path = os.path.normpath(image_path)

        img = cv2.imread(image_path)

        # 이미지 로드 확인
        if img is None:
            print(f"이미지를 읽을 수 없습니다: {image_path}")
            print("파일 경로를 확인해주세요.")
            return

        face = cascade.detectMultiScale(img, minSize=(150, 150))

        if len(face) == 0:
            print("얼굴을 찾을 수 없습니다.")
            return
        for idx, (x, y, w, h) in enumerate(face):
            print("얼굴인식 인덱스 : ", idx)
            print("얼굴 좌표 : ", x, y, w, h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # 출력 파일 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(
            current_dir, "..", "data", "opencv", "face_detect.jpg"
        )
        output_path = os.path.normpath(output_path)

        cv2.imwrite(output_path, img)
        print(f"결과 이미지 저장: {output_path}")
        cv2.imshow("Face Detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def mosaic(img, rect, size):
        (x1, y1, x2, y2) = rect
        w = x2 - x1
        h = y2 - y1
        i_rect = img[y1:y2, x1:x2]
        i_small = cv2.resize(i_rect, (size, size))
        i_mos = cv2.resize(i_small, (w, h), interpolation=cv2.INTER_AREA)
        img2 = img.copy()
        img2[y1:y2, x1:x2] = i_mos
        return img2


if __name__ == "__main__":
    face_detect = FaceDetect()
    face_detect.read_file()
