# 무선네트워크 A반 3조 팀 프로젝트
라즈베리 파이, 카메라 센서를 활용한 얼굴인식 출결관리 시스템

## 프로젝트 소개
라즈베리 파이와 카메라를 통해 얼굴을 인식하고 데이터베이스에 저장되어있는 얼굴과 비교하여 일치할 시
출석체크가 되도록하는 출결관리 시스템을 개발합니다.

## 멤버구성
``` 
김지민, 이재윤, 유태영, 김강민, 구민규, 김현빈
```

## 구조
1. 라즈베리 파이 + 카메라 센서
2. 얼굴인식 모델
3. 사진 데이터베이스 저장 및 모델과 비교, 출석 체크
4. 출결관리 UI

## 주요기능

#### 얼굴인식
- 얼굴 촬영 후 등록된 데이터베이스의 얼굴과 비교 후 관리자에게 촬영한 얼굴과 가장 비슷한 얼굴을 확인을 하여 출석체크
- 얼굴 인식이 힘들 시 지정되어있는 학번을 통해 로그인 하는 것도 가능

### 프로젝트 진행상황
1. 참고자료 토대로 모델 학습(이미지 전처리) 진행 중
<img width="973" alt="ㅁㅗㄷㅔㄹㅅㅐㅇㅅㅓㅇ" src="https://github.com/JiminGod/WirelessNetwork/assets/129360388/5191915b-b4bf-4864-9045-5725281af161">
<img width="968" alt="ㅇㅣㅁㅣㅈㅣㅈㅓㄴㅊㅓㄹㅣ" src="https://github.com/JiminGod/WirelessNetwork/assets/129360388/fafd1f80-a386-401e-bc12-4d990cf91b9e">
<img width="971" alt="얼굴확인" src="https://github.com/JiminGod/WirelessNetwork/assets/129360388/40f0bc1a-003f-4b36-97d8-911dc297fd03">

![KakaoTalk_Photo_2023-11-14-10-22-20](https://github.com/JiminGod/WirelessNetwork/assets/129360388/b8fc3480-dd85-4e14-bd0d-f70552b1e473)


## 참고자료
- https://yunwoong.tistory.com/92
- https://wondangcom.tistory.com/2446
