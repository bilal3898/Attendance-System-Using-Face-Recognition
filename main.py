import face_recognition
import cv2
import os
import pandas as pd
from datetime import datetime

# Load student images and encodings
path = "students"
known_faces = []
students = []

for file in os.listdir(path):
    img = face_recognition.load_image_file(f"{path}/{file}")
    img_encoding = face_recognition.face_encodings(img)[0]
    known_faces.append(img_encoding)
    students.append(os.path.splitext(file)[0])

# Test image folder
test_image_folder = "test_images"

for file in os.listdir(test_image_folder):
    test_image = face_recognition.load_image_file(f"{test_image_folder}/{file}")
    test_image_rgb = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

    # Detect faces in test image
    face_locations = face_recognition.face_locations(test_image_rgb)
    face_encodings = face_recognition.face_encodings(test_image_rgb, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        if True in matches:
            match_idx = matches.index(True)
            name = students[match_idx]
            print(f"Attendance marked for {name}")

# Save attendance
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            df = pd.DataFrame({"Name": [name], "Date": [date], "Time": [time]})

            with pd.ExcelWriter("attendance/attendance.xlsx", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, header=not writer.sheets)
        else:
            print("Unknown face detected.")