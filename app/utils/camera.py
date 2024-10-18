import cv2
import numpy as np
import face_recognition
from .face_recognition import FaceRecognizer

class Camera:
    def __init__(self):
        self.camera = None
        self.face_recognizer = FaceRecognizer()

    def start(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("카메라를 열 수 없습니다.")
                return False
        return True

    def stop(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def get_frame(self):
        if self.camera is None or not self.camera.isOpened():
            return None
        ret, frame = self.camera.read()
        if not ret:
            return None
        return frame

    def analyze_face(self, image):
        face_locations, face_names = self.face_recognizer.recognize_face(image)
        
        if not face_locations:
            return image, "얼굴을 찾을 수 없습니다."

        face_landmarks = face_recognition.face_landmarks(image, face_locations)

        analysis = "당신의 얼굴은 "
        if len(face_landmarks[0]['left_eye']) > 5:
            analysis += "큰 눈을 가지고 있습니다. "
        if len(face_landmarks[0]['nose_bridge']) > 4:
            analysis += "높은 코를 가지고 있습니다. "
        if len(face_landmarks[0]['top_lip']) > 7:
            analysis += "두꺼운 입술을 가지고 있습니다. "

        for face_landmark in face_landmarks:
            for facial_feature in face_landmark.keys():
                pts = np.array(face_landmark[facial_feature], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 255, 0), 2)

        analysis += "못생겼습니다.🥲"

        return image, analysis

    def detect_faces(self, image):
        face_locations = face_recognition.face_locations(image)
        return len(face_locations) > 0

camera = Camera()
