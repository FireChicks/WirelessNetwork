import os
import cv2 

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0) 
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #CAP_PROP_FRAME_WIDTH == 3
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #CAP_PROP_FRAME_HEIGHT == 4

# minW = 0.1 * camera.get(cv2.CAP_PROP_FRAME_WIDTH)
# minH = 0.1 * camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
minW = 200
minH = 200

#console message
face_id = input('\n enter user id end press <return> ==> ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

face_data_path = 'face_data'
count = 0 # # of caputre face images

user_face_folder = 'user_face' #사용자 얼굴 
user_face_path = os.path.join(user_face_folder, f"{face_id}.jpg")

#영상 처리 및 출력
while True: 
    ret, frame = camera.read() #카메라 상태 및 프레임
    frame = cv2.flip(frame, 1) # 거울모드
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #흑백으로
    
    faces = faceCascade.detectMultiScale(
        gray, # 검출하고자 하는 원본이미지
        scaleFactor = 1.1, # 검색 윈도우 확대 비율, 1보다 커야 한다
        minNeighbors = 6, # 얼굴 사이 최소 간격(픽셀)
        minSize = (int(minW), int(minH)) # 얼굴 최소 크기, 이것보다 작으면 무시
    )

    #얼굴에 대해 rectangle 출력
    for (x, y, w, h) in faces:
#        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0, 0), -1)
        count += 1

        if count == 1:
            
            resized_face_user = cv2.resize(frame[y-100:y + h+150, x-100:x + w+100], (400, 400))
            cv2.imwrite(user_face_path, resized_face_user)
        
        file_path = os.path.join(face_data_path, f"{face_id}.{count}.jpg")
        cv2.imwrite(file_path, gray[y:y + h, x:x + w])

    cv2.imshow('image', frame)

    #종료 조건
    if cv2.waitKey(1) > 0 : break 
    elif count >= 100 : break 

print("\n [INFO] Exiting Program and cleanup stuff")

camera.release() 
cv2.destroyAllWindows()

