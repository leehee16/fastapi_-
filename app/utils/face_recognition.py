import face_recognition
import os
from pathlib import Path

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        example_faces_dir = Path("app/static/example_faces")
        for image_file in example_faces_dir.glob("*.jpg"):
            name = image_file.stem
            image = face_recognition.load_image_file(str(image_file))
            encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(name)

    def recognize_face(self, image):
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]

            face_names.append(name)

        return face_locations, face_names
