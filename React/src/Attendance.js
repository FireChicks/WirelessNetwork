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
        // 서버에서 학생 데이터를 가져오는 API 호출 (시뮬레이션)
        // 실제 API 호출을 사용하려면 Axios 또는 fetch 등을 사용해야 합니다.
        // 여기에서는 시뮬레이션을 위해 하드코딩된 데이터를 사용합니다.
        const simulatedStudentsData = [
            {
                name: '김이름',
                studentNumber: '2019440931',
                status: 0,
                authenticationStatus: 2,
                attendanceTime: '10:00',
            },
            {
                name: '김이름',
                studentNumber: '2019440932',
                status: 0,
                authenticationStatus: 3,
                attendanceTime: '9:55',
            },
            // ... 다른 학생 데이터 추가
        ];

        this.setState({ studentsData: simulatedStudentsData });
    }

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
