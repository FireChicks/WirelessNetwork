import React, { Component } from 'react';
import profile from './profile/profile.png'; // 기본 프로필 이미지
import './App.css';

class Attendance extends Component {
    constructor(props) {
        super(props);
        this.state = {
            studentsData: [], // 학생 데이터를 저장할 배열
            authenticationStatus: 2, // 초기 인식 상태
            imagesList: [], // 서버에서 가져온 이미지 파일 목록
        };
    }

    // 학생 데이터를 불러오는 메소드
    fetchStudentsData() {
        const { classStartTime } = this.props;
        fetch('http://localhost:3008/users/combined_info', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            const updatedStudentsData = data.map(student => {
                if (classStartTime === "") {
                    student.att_state = 0;
                } else {
                    const studentAttTime = new Date(student.att_time);
                    if (studentAttTime <= classStartTime) {
                        student.att_state = 1; // 출석
                    } else {
                        const minutesDifference = (studentAttTime - classStartTime) / (1000 * 60);
                        student.att_state = minutesDifference <= 90 ? 2 : 3; // 지각 또는 결석
                    }
                }
                return student;
            });
            this.setState({ studentsData: updatedStudentsData });
        })
        .catch(error => console.error('Error:', error));
    }

    // 서버에서 이미지 목록을 가져오는 메소드
    fetchImagesList() {
        fetch('http://localhost:3008/images')
            .then(response => response.json())
            .then(data => this.setState({ imagesList: data }))
            .catch(error => console.error('Error:', error));
    }

    // 학생의 이미지 URL을 반환하는 메소드
    getStudentImage(student) {
        const imageName = `${student.stu_id}.png`;
        console.log(`http://localhost:3008/images/${imageName}`)
        if (this.state.imagesList.includes(imageName)) {
            const imageUrl = `http://localhost:3008/images/${imageName}`;
            console.log("Image URL:", imageUrl);
            return imageUrl;
        }
        return profile; // 기본 이미지
    }


    componentDidMount() {
        this.fetchStudentsData();
        this.fetchImagesList();
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
        const statusTexts = ['출석 전 ', '출석 ', '지각 ', '결석 '];

        if (student.att_state !== 0 && student.att_state !== 3) {
            const attTime = new Date(student.att_time); // 문자열을 Date 객체로 파싱
            const hours = attTime.getHours(); // 시간 추출
            const minutes = attTime.getMinutes(); // 분 추출
            const formattedTime = `${hours}:${minutes}`; // 시간 형식으로 포맷
    
            return statusTexts[student.att_state] + formattedTime;
        }
        return statusTexts[student.att_state];
    }

    getAuthenticationStatusText(student) {
        const authenticationStatusTexts = [
            '인증되지 않음', '지문인증', '얼굴인증', '지문/얼굴 인증',
        ];

        if(student.att_state == 0){
            return ""
        }
        return authenticationStatusTexts[student.att_way];
    }

    getStatusColorClass(student) {
        const statusColors = ['white-bg', 'blue-bg', 'yellow-bg', 'red-bg'];
        return statusColors[student.att_state] || 'default-bg';
    }

    render() {
        const { studentsData } = this.state;

        return (
            <div className="attendance">
                {studentsData.map((student) => (
                    <div key={student.stu_id} className={`profile-state ${this.getStatusColorClass(student)}`}>
                        <img src={this.getStudentImage(student)} className="profile" alt="profile" />
                        <p className='name'>{student.stu_name}</p>
                        <p className='student-id'>{student.stu_id}</p>
                        <p className='student-state'>{this.getStatusText(student)}</p>
                        <p className='student-state'>{this.getAuthenticationStatusText(student)}</p>
                    </div>
                ))}
            </div>
        );
    }
}

export default Attendance;
