import React, { Component } from 'react';
import logo from './logo.png';
import logotxt from './logo.svg';
import Attendance from './Attendance';
import camera from './camera/camera.jpeg';
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
    // 현재 시간을 가져와서 출석 시간 목록에 추가
    const currentTime = new Date();

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
              <button onClick={this.handleStartClass}>출석 시작</button>
            </div>
          </div>

          <div className="setting-bar">
            <h2>출석현황</h2>
          </div>
          <Attendance />
          
        </header>
      </div>
    );
  }
}

export default App;
