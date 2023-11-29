#학생 클래스
class StudentVO:
    stu_name = ""
    stu_grade = ""
    stu_class = ""
    stu_id = ""
    stu_dept = ""
    stu_pic = bytes
    stu_finger_print: bytes
    finger_dir = './finger_prints/'

    def __init__(self, name, grade, cls, id, dept, pic, finger):
        self.stu_name = name
        self.stu_grade = grade
        self.stu_class = cls
        self.stu_id = id
        self.stu_dept = dept
        self.stu_pic = pic
        self.stu_finger_print = finger


    #지문 재등록시 사용 메서드
    def change_finger_print(self, finger_print):
        self.stu_finger_print = finger_print