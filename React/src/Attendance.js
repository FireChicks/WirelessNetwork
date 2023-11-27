import React, { Component } from 'react';
import profile from './profile/profile.png';
import './App.css';

class Attendance extends Component {
    constructor(props) {
        super(props);
        this.state = {
            studentsData: [], // 학생 데이터를 저장할 배열
            authenticationStatus: 2, // 초기 인식 상태 (0: 인증하지 않음, 1: 지문인증, 2: 얼굴인증, 3: 지문/얼굴 인증)
        };
    }
    getStudentImage(student) {
        const studentImage = `./camera/${student.stu_id}.png`;
        const defaultImage = profile; // 기본 이미지

        try {
            return require(studentImage); // 학생 이미지를 시도하여 불러옴
        } catch (error) {
            return defaultImage; // 오류 발생 시 기본 이미지 반환
        }
    }
    fetchStudentsData() {
        const { classStartTime } = this.props;
        // 전체 학생 정보 조회
        fetch('http://localhost:3008/users/combined_info', {
            method: 'GET', // GET 요청 방식을 사용
        })
            .then(response => response.json()) // 서버 응답을 JSON 형식으로 변환
            .then(data => {
                // API에서 받아온 데이터를 studentsData 배열에 추가
                const updatedStudentsData = data.map(student => {
                    // 수업 시작 시간이 null이라면 출석 상태를 0으로 설정
                    if (classStartTime === "") {
                        student.att_state = 0;
                    } else {
                        // 학생의 att_time 정보 가져오기
                        const studentAttTime = new Date(student.att_time);
                        // 학생의 출석 상태 계산
                        if (studentAttTime <= classStartTime) {
                            student.att_state = 1; // 출석
                        } else {
                            const minutesDifference = (studentAttTime - classStartTime) / (1000 * 60); // 분 단위로 차이 계산

                            if (minutesDifference <= 90) { //수업시작 90이내에 오면 지각처리
                                student.att_state = 2; // 지각
                            } else {
                                student.att_state = 3; // 결석
                            }
                        }
                    }
                    console.log(data)
                    return student;
                });

                // 업데이트된 출석 상태를 state에 설정
                this.setState({ studentsData: updatedStudentsData });
            })
            .catch(error => console.error('Error:', error)); // 오류 발생 시 콘솔에 오류 메시지 출력
    }


    componentDidMount() {
        this.fetchStudentsData();
    }

    componentDidUpdate(prevProps) {
        if (this.props.classStartTime !== prevProps.classStartTime) {
            this.fetchStudentsData();
        }
    }

    setAuthenticationStatus = (status) => {
        this.setState({ authenticationStatus: status });
    }

    getStatusText(student) {
        const statusTexts = ['출석 전', '출석', '지각', '결석'];
        const statusText = statusTexts[student.att_state];
        console.log(`Student status for ${student.stu_name}: ${statusText}`);
        return statusText;
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
        const status = student.att_state; // 'att_state' 속성을 사용하도록 수정

        if (status >= 0 && status < statusColors.length) {
            return statusColors[status];
        } else {
            return 'default-bg'; // 기본 배경색 클래스
        }
    }

    render() {
        const { authenticationStatus, studentsData } = this.state;

        return (
            <div className="attendance">
                {studentsData.map((student) => (
                    <div key={student.stu_id} className={`profile-state ${this.getStatusColorClass(student)}`}>
                        <img src={profile} className="profile" alt="profile" />
                        <p className='name'>{student.stu_name}</p>
                        <p className='student-id'>{student.stu_id}</p>
                        <p className='student-state'>{this.getStatusText(student)}</p>
                        <p className='student-state'>{this.getAuthenticationStatusText(student.att_way)}</p>
                    </div>
                ))}
            </div>
        );
    }
}

export default Attendance;
