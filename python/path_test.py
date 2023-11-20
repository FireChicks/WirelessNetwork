import os
path = "face_data"
names = []

for image_name in os.listdir(path):
    names.append(image_name.split(".")[0])

names = list(names) # 중복 제거, 정렬됨