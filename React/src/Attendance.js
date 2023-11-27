import React, { Component } from 'react';
import profile from './profile_1.png';
import './App.css';

class Attendance extends Component {
    constructor(props) {
        super(props);
        this.state = {
            studentsData: [], // 학생 데이터를 저장할 배열
            authenticationStatus: 2, // 초기 인식 상태 (0: 인증하지 않음, 1: 지문인증, 2: 얼굴인증, 3: 지문/얼굴 인증)
        };
    }

    componentDidMount() {
        // 전체 학생 정보 조회
        fetch('http://localhost:3008/users/combined_info', {
            method: 'GET', // GET 요청 방식을 사용
        })
        .then(response => response.json()) // 서버 응답을 JSON 형식으로 변환
        .then(data => console.log(data)) // 변환된 데이터를 콘솔에 출력
        .catch(error => console.error('Error:', error)); // 오류 발생 시 콘솔에 오류 메시지 출력
    }
    
    // componentDidMount() {
    //     // 전체 학생 정보 조회
    //     fetch('http://localhost:3008/users/sel_stu', {
    //         method: 'POST', // POST 요청 방식을 사용
    //         headers: {
    //             'Content-Type': 'application/json', // 요청 본문이 JSON 형태임을 나타냄
    //         }
    //     })
    //     .then(response => response.json()) // 서버 응답을 JSON 형식으로 변환
    //     .then(data => console.log(data)) // 변환된 데이터를 콘솔에 출력
    //     .catch(error => console.error('Error:', error)); // 오류 발생 시 콘솔에 오류 메시지 출력
    // }


    setAuthenticationStatus = (status) => {
        this.setState({ authenticationStatus: status });
    }

    getStatusText(student) {
        const statusTexts = ['출석 전', '출석', '지각', '결석'];
        return statusTexts[student.status];
    }

    getAuthenticationStatusText(student) {
        const authenticationStatusTexts = [
            '인증되지 않음',
            '지문인증',
            '얼굴인증',
            '지문/얼굴 인증',
        ];
        return authenticationStatusTexts[student];
    }

    getStatusColorClass(student) {
        const statusColors = ['white-bg', 'blue-bg', 'yellow-bg', 'red-bg'];
        return statusColors[student.status];
    }
    render() {
        const { authenticationStatus, studentsData } = this.state;

        return (
            <div className="attendance">
                {studentsData.map((student) => (
                    <div key={student.studentNumber} className={`profile-state ${this.getStatusColorClass(student)}`}>
                        <img src={profile} className="profile" alt="profile" />
                        <p className='name'>{student.name}</p>
                        <p className='student-id'>{student.studentNumber}</p>
                        <p className='student-state'>{this.getStatusText(student)}</p>
                        <p className='student-state'>{this.getAuthenticationStatusText(student.authenticationStatus)}</p>
                    </div>
                ))}
            </div>
        );
    }

}

export default Attendance;
