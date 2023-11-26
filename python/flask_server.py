from flask import Flask, render_template, Response, request, send_file
import cv2
import finger_print as fp

app = Flask(__name__)

#영상 가로, 세로 크기, 프레임
frame_width = 1280
frame_height = 720

#지문 템플릿 저장 폴더
directory = './finger_prints/'

def generate_frames():
    camera = cv2.VideoCapture(0)  # 카메라 번호, 0은 기본 카메라
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    while True:    
        success, frame = camera.read()  # 카메라로부터 프레임 읽기
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  # 프레임을 JPEG 형식으로 인코딩         
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 전송

@app.route('/')
def index():
    return render_template('index.html')  # HTML 템플릿을 렌더링

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # 영상 스트리밍

@app.route('/register_fingerprint', methods=['POST'])
def register_fingerprint():
    if request.method == 'POST':
        student_id = request.form['student_id']
        
        fp.enroll_save_to_file(student_id)
        return send_file(f'{directory}template_{student_id}.dat', as_attachment=True)
    return 'Method Not Allowed', 405

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
