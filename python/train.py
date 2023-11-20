import cv2
import numpy as np #배열 계산 용이
from PIL import Image #python imaging library
import os

imagePath = 'face_data' #경로 (dataset 폴더)
recognizer = cv2.face.LBPHFaceRecognizer_create()
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cascade_path)

def getImagesAndLabels(imagePath):
    imagePaths = []
    faceSamples = []
    ids = []

    for fileName in os.listdir(imagePath):
        imagePaths.append(os.path.join(imagePath, fileName))
    #listdir : 해당 디렉토리 내 파일 리스트
    #path + file Name : 경로 list 만들기

    for faceImage in imagePaths:#각 파일마다
        #흑백 변환 
        PIL_img = Image.open(faceImage).convert('L') #L : 8 bit pixel, bw
        img_numpy = np.array(PIL_img, 'uint8')

        #user id
        id = int(os.path.split(faceImage)[-1].split(".")[0]) #마지막 index : -1

        #얼굴 샘플
        faces = detector.detectMultiScale(img_numpy)

        for(x, y, w, h) in faces:
            faceSamples.append(img_numpy[y : y + h, x : x + w])
            ids.append(id)

    return faceSamples, ids

print('\n [INFO] Training faces. It will take a few seconds. Wait ...')
faces, ids = getImagesAndLabels(imagePath)

recognizer.train(faces, np.array(ids)) #학습

trained_file_path = 'train_data/train_model.yml'

recognizer.write(trained_file_path)

print('\n [INFO] {0} faces trained. Exiting Program'.format(len(np.unique(ids))))

