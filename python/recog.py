import cv2
import numpy as np
import os
import PIL

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('train_data/train_model.yml')

cascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

path = "face_data"

id = 0
names = []

for image_name in os.listdir(path):
    id = image_name.split(".")[0]
    names.append(int(id))

names = list(set(names)) # 중복 제거, 정렬됨

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# minW = 0.1 * camera.get(cv2.CAP_PROP_FRAME_WIDTH)
# minH = 0.1 * camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
minW = 200
minH = 200

while True:
    ret, img = camera.read()
    img = cv2.flip(img, 1) # 거울모드
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 6,
        minSize = (int(minW), int(minH))
    )

    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y : y + h, x : x + w])
       
        # id = 현재 인식된 사람의 식별 id
        # confidence = 현재 인식된 사람과의 유사도
        # names = 식별 id의 전체 목록

        print(id, round(100 - confidence), names)

        if round(100 - confidence) < 70:
            id = "who are you?"

        # confidence가 0에 가까울수록 유사도가 높다
        confidence = "  {0}%".format(round(100 - confidence))

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
    
    cv2.imshow('camera', img)
    if cv2.waitKey(50) > 0 : break

print("\n [INFO] Exiting Program and cleanup stuff")
camera.release()
cv2.destroyAllWindows()

