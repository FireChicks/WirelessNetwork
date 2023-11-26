import cv2
import numpy as np
import os
import requests
from PIL import Image #python imaging library

#라즈베리파이 Flask 서버 ip 및 포트
streaming_url = 'http://192.168.123.110:5000'

cascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create()

#모델 로드
recognizer.read('train_data/train_model.yml')

detector = cv2.CascadeClassifier(cascadePath)
path = "face_data"
id = 0
names = []

#학생 클래스
class Student:
    stu_name = ""
    stu_grade = ""
    stu_class = ""
    stu_id = ""
    stu_dept = ""
    stu_finger_print: bytes
    finger_dir = './finger_prints/'

    def __init__(self, name, grade, cls, id, dept, finger_print):
        self.stu_name = name
        self.stu_grade = grade
        self.stu_class = cls
        self.stu_id = id
        self.stu_dept = dept
        self.stu_finger_print = finger_print
        with open(f'{self.finger_dir}{self.stu_id}.dat', 'wb') as file:
            file.write(self.stu_finger_print)

    #지문 재등록시 사용 메서드
    def change_finger_print(self, finger_print):
        self.stu_finger_print = finger_print


for image_name in os.listdir(path):
    id = image_name.split(".")[0]
    names.append(int(id))

names = list(set(names))  # 중복 제거, 정렬됨


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
def check_face():
    response = requests.get(f'{streaming_url}/video_feed', stream=True)
    if response.status_code == 200:
        bytes_data = bytes()
        for chunk in response.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_data[a:b + 2]
                bytes_data = bytes_data[b + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6, minSize=(200, 200))

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    id, confidence = recognizer.predict(gray[y : y + h, x : x + w])
                    if round(100 - confidence) < 70:
                        id = "Unknown"

                    confidence = "  {0}%".format(round(100 - confidence))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                    cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

                cv2.imshow('Received Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

def face_collect(face_id):
    user_face_folder = 'user_face'  # 사용자 얼굴
    user_face_path = os.path.join(user_face_folder, f"{face_id}.jpg")
    # 영상 스트리밍 데이터를 받아옴
    response = requests.get(f'{streaming_url}/video_feed', stream=True)

    if response.status_code == 200:
        bytes_data = bytes()
        count = 0  # 캡처된 이미지 수
        while True:
            bytes_data += response.raw.read(1024)
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_data[a:b + 2]
                bytes_data = bytes_data[b + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.05,
                    minNeighbors=6,
                    minSize=(200, 200)
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    count += 1
                    file_path = os.path.join(path, f"{face_id}.{count}.jpg")
                    cv2.imwrite(file_path, gray[y:y + h, x:x + w])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(count), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                cv2.imshow('Received Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    # 종료 조건
                elif count >= 100:
                    break

def save_finger_print(student_id):
    print(f'{student_id}지문 등록을 시작합니다.')
    data = {'student_id': student_id}
    try:
        response = requests.post(f'{streaming_url}/register_fingerprint', data=data)
        if response.status_code == 200:
            # 지문 데이터 수신 성공
            print('Fingerprint template received successfully.')
            return response.content
        else:
            print(f'Error: {response.status_code}')
    except requests.RequestException as e:
        print(f'An error occurred: {e}')

def train_model():
    print('\n [INFO] Training faces. It will take a few seconds. Wait ...')
    faces, ids = getImagesAndLabels(path)

    recognizer.train(faces, np.array(ids))  # 학습

    trained_file_path = 'train_data/train_model.yml'

    recognizer.write(trained_file_path)

    print('\n [INFO] {0} faces trained.'.format(len(np.unique(ids))))

while True:
    print('-----------------------------')
    print('c) 얼굴 확인')
    print('e) 신규 등록')
    print('t) 모델 학습')
    print('q) 종료')
    print('-----------------------------')
    c = input(">")

    if c == "c":
        check_face()
    elif c == "e":
        valid_grade = True
        stu_name = input('이름을 입력해주세요 > ')
        while valid_grade :
            input_grade = input('학년을 입력해주세요 (1~4) > ')
            try:
                stu_grade = int(input_grade)
            except ValueError:
                stu_grade = 0
            if stu_grade >= 1 and stu_grade <= 4 :
                valid_grade = False

        stu_class = input('반을 입력해주세요 > ')
        stu_id = input('학번을 입력해주세요 > ')
        stu_dept = input('학부를 입력해주세요 > ')

        print(f"{stu_id}님의 사진 저장을 시작합니다.")
        face_collect(stu_id)
        stu_finger = save_finger_print(student_id=stu_id)

        student = Student(name=stu_name, grade=str(stu_grade), cls=stu_class, id=stu_id,dept=stu_dept,finger_print=stu_finger)

    elif c == "f":
        train_model()

    elif c == "q":
        raise SystemExit

cv2.destroyAllWindows()
