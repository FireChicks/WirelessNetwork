import cv2
import numpy as np
import os
import requests
from PIL import Image #python imaging library
import time
import studentVO
import student_db_manager as stu_db_man
import image_db_manager as img_db_man
import attend_db_manager as att_db_man
import prof_db_manager as pro_db_man
import class_db_manager as cls_db_man
import class_stu_db_manager as cls_stu_db_man

#라즈베리파이 Flask 서버 ip 및 포트
streaming_url = 'http://192.168.123.117:5000'

cascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create()

userfaceDir = './user_face/'

detector = cv2.CascadeClassifier(cascadePath)
facePath = "face_data"
verifedPath = "./verified/"

id = 0
names = []

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


for image_name in os.listdir(facePath):
    id = image_name.split(".")[0]
    names.append(int(id))

names = list(set(names))  # 중복 제거, 정렬됨


def read_files_by_student_id(directory, student_id):
    matching_files_content = []

    # 해당 디렉토리 내의 모든 파일에 대해 확인
    for filename in os.listdir(directory):
        # 파일 이름에서 확장자를 제외한 부분을 가져옴
        name, extension = os.path.splitext(filename)
        # 파일 이름을 학번과 .을 기준으로 분리하여 학번 부분을 가져옴
        parts = name.split('.')
        if len(parts) > 1:
            file_student_id = parts[0]
            # 학번이 입력한 학번과 일치하면 해당 파일을 읽어서 리스트에 추가
            if file_student_id == student_id:
                matching_files_content.append(read_file(f'./{directory}/{name}{extension}'))

    return matching_files_content
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

def download_model(class_code):
    delete_files_in_directory('./train_data')
    class_model = cls_db_man.select_model(class_code)
    if class_model == None:
        return False
    with open('train_data/train_model.yml', 'wb') as file:
        file.write(class_model)
    recognizer.read('train_data/train_model.yml')
    return True

def check_face(class_code):
    if not download_model(class_code):
        return
    response = requests.get(f'{streaming_url}/video_feed', stream=True)
    conf = 0

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
                    id, confidence = recognizer.predict(gray[y: y + h, x: x + w])
                    if round(100 - confidence) < 70:
                        id = "Unknown"

                    if id != "Unknown":
                        return id

                    conf = 100 - confidence

                    confidence = "  {0}%".format(round(100 - confidence))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                    cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

                if conf > 70:
                    cv2.imwrite(f'{verifedPath}{id}.jpg', frame)
                    break

                cv2.imshow('Received Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

def check_face_auto(class_code):
    if not download_model(class_code):
        return

    response = requests.get(f'{streaming_url}/video_feed', stream=True)
    conf = 0
    id_list = []

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
                    id, confidence = recognizer.predict(gray[y: y + h, x: x + w])
                    if round(100 - confidence) < 70:
                        id = "Unknown"
                    conf = 100 - confidence

                    confidence = "  {0}%".format(round(100 - confidence))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                    cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

                if conf > 70:
                    if id not in id_list:
                        cv2.imwrite(f'{verifedPath}{id}.jpg', frame)
                        img = read_file(f'{verifedPath}{id}.jpg')
                        att_db_man.insert_attend(stu_id=id, att_way=2, img=img,class_code=class_code)
                        id_list.append(id)
                cv2.imshow('Received Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return 'exit'
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
                    if count == 1:
                        resized_face_user = cv2.resize(frame[y - 100:y + h + 150, x - 100:x + w + 100], (400, 400))
                        cv2.imwrite(user_face_path, resized_face_user)

                    file_path = os.path.join(facePath, f"{face_id}.{count}.jpg")
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
    delete_files_in_directory('./finger_print')
    print(f'{student_id}지문 등록을 시작합니다.')
    data = {'student_id': student_id}
    retries = 0

    while retries < MAX_RETRIES:
        try:
            response = requests.post(f'{streaming_url}/register_fingerprint', data=data)
            if response.status_code == 200:
                # 지문 데이터 수신 성공
                print('Fingerprint template received successfully.')
                return response.content
            else:
                print(f'Error: {response.status_code}')

            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)

    print("Maximum retries exceeded. Failed to register fingerprint.")
    return None

def send_finger_print(VO):
    # 요청 보내기
    url = f'{streaming_url}/check_fingerprint'
    files = {
        'stu_finger_print': VO.stu_finger_print
    }

    data = {
        'stu_id': VO.stu_id
    }
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        text = response.text
        if text == 'True':
            return True
        elif text == 'False':
            return False
        else :
            print(text)
    else:
        print(f'Error: {response.status_code}')
        return False
def train_model():
    print('\n [INFO] Training faces. It will take a few seconds. Wait ...')
    faces, ids = getImagesAndLabels(facePath)

    recognizer.train(faces, np.array(ids))  # 학습

    trained_file_path = 'train_data/train_model.yml'

    recognizer.write(trained_file_path)

    print('\n [INFO] {0} faces trained.'.format(len(np.unique(ids))))

def read_file(dir):
    try:
        with open(f'{dir}', 'rb') as file:
            image_data = file.read()
        return image_data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except IOError as e:
        print("파일을 읽는 중 오류가 발생했습니다:", e)
    except Exception as e:
        print("알 수 없는 오류가 발생했습니다:", e)


def delete_files_in_directory(directory):
    try:
        # 디렉토리 내부의 모든 파일 목록을 가져와서 삭제
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    except OSError as e:
        print(f"Error: {e.strerror}")


def check_class():
    cls_db_man.check_all_class()
    while True:
        class_code = input("확인할 강의의 code를 입력해주세요 > ")
        if cls_db_man.check_class(class_code):
            return class_code


while True:
    print('')
    print('실행하고자 하는 메뉴의 알파벳을 입력해주세요')
    print('-----------------------------')
    print('a) 출석 시작')
    print('s) 학생')
    print('p) 교수')
    print('q) 종료')
    print('-----------------------------')
    f = input("> ")


    #출석 시작
    if f == "a":
        print('')
        print('출석 방식을 선택해주세요')
        print('-----------------------------')
        print('a) 자동 얼굴 확인')
        print('c) 얼굴 확인')
        print('f) 지문 확인')
        print('-----------------------------')
        s = input("> ")

        if s == "a":
            class_code = check_class()
            print("자동 얼굴인식을 실행합니다. (q키를 눌러서 종료 가능합니다.)")
            check_face_auto(class_code)
            continue
        if s == "c":
            class_code = check_class()
            print("얼굴인식을 실행합니다.")

            stu_id = check_face(class_code)

            if stu_id == None:
                print("일치하는 학번이 없습니다.")
                continue

            # 출석 정보 입력
            img = read_file(f'{verifedPath}{stu_id}.jpg')
            att_db_man.insert_attend(stu_id=stu_id, img=img, att_way=2, class_code = class_code)

            print(f'{stu_id}님이 인증되었습니다.')

        elif s == "f":
            class_code = check_class()
            stu_num = input('지문을 체크할 학번을 입력해주세요 > ')
            student = stu_db_man.select_student(stu_num)
            if student == None:
                continue
            if send_finger_print(student):
                # 출석 정보 입력
                att_db_man.insert_attend_by_fp(stu_id=stu_num, att_way=2, class_code = class_code)
                print('인증된 지문입니다.')
            else:
                print('인증되지 않은 지문입니다.')

        else:
            print('지정된 알파벳을 소문자로 입력해주세요')
    #학생 정보 변경
    elif f == "s" :
        print('')
        print('실행할 메뉴를 선택해주세요')
        print('-----------------------------')
        print('e) 신규 등록')
        print('r) 지문 재 등록')
        print('i) 이미지 재 등록')
        print('c) 강의 수강 시작')
        print('-----------------------------')
        s = input("> ")

        if s == "r":
            stu_num = input('지문을 재설정할 학번을 입력해주세요')
            VO = stu_db_man.select_student(stu_num)
            VO.stu_finger_print = save_finger_print(student_id=stu_id)
            stu_db_man.update_student(VO)
            print('성공적으로 지문을 재등록했습니다.')

        elif s == "i":
            stu_id = input('등록할 학생의 id를 입력해주세요 >')
            if stu_db_man.select_student(stu_id) == None :
                print('존재하지 않는 학생 입니다.')
                break

            #모델학습 이미지 재등록
            img_db_man.delete_img(stu_id)
            face_collect(stu_id)
            images = read_files_by_student_id(facePath, stu_id)
            img_db_man.insert_images(stu_id, images)

            #대표 이미지 재등록
            VO = stu_db_man.select_student(stu_id)
            VO.stu_pic = read_file(f'{userfaceDir}{stu_id}.jpg')
            stu_db_man.update_student(VO)

            print('성공적으로 이미지를 재등록했습니다.')
        elif s == "e":
            valid_grade = True
            stu_grade = 0
            stu_name = input('이름을 입력해주세요 > ')
            while valid_grade:
                input_grade = input('학년을 입력해주세요 (1~4) > ')
                try:
                    stu_grade = int(input_grade)
                except ValueError:
                    stu_grade = 0
                if stu_grade >= 1 and stu_grade <= 4:
                    valid_grade = False

            stu_class = input('반을 입력해주세요 > ')
            stu_id = input('학번을 입력해주세요 > ')
            stu_dept = input('학부를 입력해주세요 > ')

            # 100장의 사진 수집
            print(f"{stu_id}님의 사진 저장을 시작합니다.")
            face_collect(stu_id)
            stu_finger = save_finger_print(student_id=stu_id)

            # 대표 이미지 가져오기
            print('대표 이미지를 불러옵니다...')
            stu_pic = read_file(f'{userfaceDir}{stu_id}.jpg')

            # 학생VO와 이미지 리스트 생성
            student = studentVO.StudentVO(name=stu_name, grade=str(stu_grade), cls=stu_class,
                                          id=stu_id, dept=stu_dept, pic=stu_pic, finger=stu_finger)
            images = read_files_by_student_id(facePath, stu_id)
            if images == None:
                print('사진저장이 제대로 되지 않았습니다.')
                pass
            # DB에 학생, 이미지들 순으로 입력
            stu_db_man.insert_student(student)
            img_db_man.insert_images(stu_id, images)
        elif s == "c":
            stu_id = input('등록할 학생의 id를 입력해주세요 >')
            if stu_db_man.select_student(stu_id) == None :
                print('존재하지 않는 학생 입니다.')
                break
            class_code = check_class()
            if not cls_db_man.check_class(class_code):
                print('존재하지 않는 수업 입니다.')
                break

            if not cls_stu_db_man.is_enroll(class_code, stu_id):
                print(f'이미 수강중인 강의입니다..')
                break

            cls_stu_db_man.insert_class_stu(class_code, stu_id)

        else:
            print('지정된 알파벳을 소문자로 입력해주세요')
    #교수
    elif f == "p":
        print('')
        print('실행할 메뉴를 선택해주세요')
        print('-----------------------------')
        print('e) 교수 등록')
        print('c) 강의 정보 입력')
        print('t) 수업 학생 모델 생성')
        print('-----------------------------')
        s = input("> ")

        if s == 'e':
            prof_id   = input('등록할 교수의 id를 입력해주세요 >')
            prof_name = input('등록할 교수의 이름을 입력해주세요 >')
            pro_db_man.insert_prof(prof_id, prof_name)
        elif s == 'c':
            prof_id = input('등록할 교수의 id를 입력해주세요 >')
            if pro_db_man.check_prof(prof_id):
                class_code = input('등록할 수업의 id를 입력해주세요 >')
                class_name = input('등록할 수업의 이름을 입력해주세요 >')

                cls_db_man.insert_class(class_code=class_code,
                                        class_name=class_name,
                                        prof_id=prof_id)
            else:
                print('존재하지않는 교수의 id입니다.')
        elif s == 't':
            class_code = check_class()
            if cls_db_man.check_class(class_code):
                delete_files_in_directory('./face_data')
                stu_ids = cls_stu_db_man.check_students(class_code)
                if stu_ids == None:
                    print("현재 강의를 수강하는 학생이 없습니다.")
                for stu_id in stu_ids:
                    img_db_man.select_img(stu_id)

                train_model()
                model = read_file('train_data/train_model.yml')
                cls_db_man.update_model(model,class_code)

                delete_files_in_directory('./face_data')
                delete_files_in_directory('./train_data')
            else:
                print('존재하지않는 강의의 id입니다.')
        else:
            print('지정된 알파벳을 소문자로 입력해주세요')

    elif f == "q":
        raise SystemExit

    else:
        print('지정된 알파벳을 소문자로 입력해주세요')

cv2.destroyAllWindows()
