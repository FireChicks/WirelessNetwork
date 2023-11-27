import React, { Component } from 'react';
import logo from './logo.png';
import logotxt from './logo.svg';
import Attendance from './Attendance';
import camera from './profile/camera.jpeg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      classStartTime: '', // 수업 시작 시간을 저장할 상태
      attendanceTimes: [], // 출석 시간 목록을 저장할 상태
    };
  }

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

    }
  };


  render() {
    const { attendanceTimes } = this.state;

    // 생성된 출석 시간 목록을 옵션으로 변환
    const attendanceOptions = attendanceTimes.map((time, index) => (
      <option key={index} value={index}>
        {time}
      </option>
    ));

    return (
      <div className="App">
        <div className="header">
          <img src={logotxt} className="main-logo" alt="logotxt" />
          <img src={logo} className="App-logo" alt="logo" />
        </div>
        <header className="App-header">
          <img src={camera} className="image" alt="camera" />
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
          </div>
          <Attendance classStartTime={this.state.classStartTime} />
        </header>
      </div>
    );
  }
}

export default App;
