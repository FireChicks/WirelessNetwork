import React, { Component } from 'react';
import logo from './logo.png';
import logotxt from './logo.svg';
import Attendance from './Attendance';
import camera from './profile/camera.png';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      classStartTime: '', // 수업 시작 시간을 저장할 상태
      attendanceTimes: [], // 출석 시간 목록을 저장할 상태
      faceList: [], // facelist를 저장할 상태
    };
  }
  componentDidMount() {
    this.fetchFaceList(); // 컴포넌트가 마운트되면 facelist를 가져옴
    this.setDefaultImage(); // 기본 이미지 설정

  }

  fetchFaceList() {
    fetch('http://localhost:3008/users/sel_att')
      .then(response => response.json())
      .then(data => {
        // 서버에서 받은 데이터의 att_date 필드만 추출하여 배열에 추가
        const extractedDates = data.map(item => item.att_date);
  
        this.setState({ faceList: extractedDates });
      })
      .catch(error => console.error('Error:', error));
  }
  getFaceImage = async (date) => {
    try {
      const response = await fetch(`http://localhost:3008/users/sel_att`);
      const data = await response.json();
      
      const matchingImage = data.find(item => item.att_date === date);
  
      if (matchingImage) {
        return matchingImage.img;
      } else {
        return null;
      }
    } catch (error) {
      console.error('Error:', error);
      return null;
    }
  };
  
  handleStartClass = () => {
    // 입력된 시간 문자열 가져오기
    const timeInput = document.querySelector('input[name="time-setting"]');
    const timeString = timeInput.value;
  
    // 오늘의 날짜를 가져옴
    const today = new Date();
    const year = today.getFullYear();
    const month = ("0" + (today.getMonth() + 1)).slice(-2); // 월은 0부터 시작하므로 1을 더해줍니다.
    const day = ("0" + today.getDate()).slice(-2);
  
    // 시간 문자열을 Date 객체로 파싱
    const currentTime = new Date(`${year}-${month}-${day}T${timeString}:00`);
  
    // 유효한 Date 객체인지 확인
    if (isNaN(currentTime.getTime())) {
      // 유효하지 않은 경우 얼럿 창 띄우기
      alert('수업시작 시간을 설정하세요');
    } else {
      // 유효한 경우 콘솔에 시간 출력
      console.log('출석 시간 (Date 객체):', currentTime);
      this.setState({ classStartTime: currentTime }); // 수업 시작 시간 설정
      
      // faceList를 다시 가져오기 위해 fetchFaceList() 호출
      this.fetchFaceList();
    }
  };
  
  handleFaceListChange = async (event) => {
    const selectedOption = event.target.value;
    const faceUrl = await this.getFaceImage(selectedOption); // await를 사용하여 비동기 처리 기다림

  
    this.setState({ selectedImage: faceUrl });
  };

  setDefaultImage() {

    const defaultImageUrl = camera; // 기본 이미지 URL을 설정해주세요.
    this.setState({ selectedImage: defaultImageUrl });

  }



  render() {
    const { attendanceTimes, faceList, selectedImage } = this.state;

    // 생성된 출석 시간 목록을 옵션으로 변환
    const attendanceOptions = attendanceTimes.map((time, index) => (
      <option key={index} value={index}>
        {time}
      </option>
    ));

    // facelist를 옵션으로 변환
    const faceListOptions = faceList.map((face, index) => (
      <option key={index} value={face}>
        {face}
      </option>
    ));

    // 현재시간 가져오기
    const today = new Date();
    // 날짜 지정
    const formattedDate = `${today.getFullYear()}년 ${today.getMonth() + 1}월 ${today.getDate()}일 ${today.getHours()}시 ${today.getMinutes()}분`;


    return (
      <div className="App">
        <div className="header">
          <img src={logotxt} className="main-logo" alt="logotxt" />
          <img src={logo} className="App-logo" alt="logo" />
        </div>
        <header className="App-header">
          <div className="flex">
            <img src={selectedImage} className="image" alt="camera" /> {/* 선택된 이미지로 변경 */}
            <div className="top-container">
              <div>
                <p className="log-title">인증로그</p>
              </div>
              <select className="face-log" name="face-log" size="15" onChange={this.handleFaceListChange}>
                {faceListOptions}
              </select>
            </div>
          </div>
          <div className="setting-bar">
            <div className="setting-container">
              <div className="inline-box">
                <p>수업시작 시간 : </p>
                <input
                  name="time-setting"
                  type="time"
                  className="info"
                />
              </div>
            </div>
            <div>
              <button onClick={this.handleStartClass}>출석 확인</button>
            </div>
          </div>
          <div className="setting-bar">
            <h2>출석현황</h2>
            <a className="date-text">{formattedDate}</a>
          </div>
          <Attendance classStartTime={this.state.classStartTime} />
        </header>
      </div>
    );
  }
}

export default App;
