import mysql.connector
import studentVO

def insert_student(VO):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }

        if(VO.stu_pic == None or VO.stu_pic == None) :
            print('입력되지 않은 값이 있습니다.')
        else:
            connection = mysql.connector.connect(**connection)
            if connection.is_connected():
                # 쿼리 실행
                cursor = connection.cursor()

                # 예시 데이터를 사용하여 테이블에 데이터 삽입
                insert_query = "INSERT INTO student (stu_id, stu_name, stu_grade, stu_class, stu_dept, stu_pic, stu_finger_dat) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                student_data = (VO.stu_id, VO.stu_name, VO.stu_grade, VO.stu_class, VO.stu_dept, VO.stu_pic, VO.stu_finger_print)

                cursor.execute(insert_query, student_data)

                # 변경사항 커밋
                connection.commit()
                print('데이터베이스에 성공적으로 학생 정보를 입력 하였습니다.')

    except mysql.connector.Error as e:
        print('Datababase Error: ', e)
    finally:
        try:
            cursor.close()
        except NameError:
            pass

        try:
            connection.close()
        except mysql.connector.Error as e:
            print('Error occurred while closing the connection:', e)

        print('데이터베이스와의 연결을 종료하였습니다.')


def select_all_student(stu_id):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }

        connection = mysql.connector.connect(**connection)

        # 쿼리 실행
        cursor = connection.cursor()

        # 예시 쿼리: 모든 학생 정보 가져오기
        query = "SELECT * FROM student;"
        cursor.execute(query)

        # 쿼리 결과 가져오기
        rows = cursor.fetchall()

        # 결과 출력
        for row in rows:
            print(row)

    except mysql.connector.Error as error:
        print(f'MySQL 에러 발생: {error}')
    finally:
        try:
            cursor.close()
        except NameError:
            pass

        try:
            connection.close()
        except mysql.connector.Error as e:
            print('Error occurred while closing the connection:', e)

        print('데이터베이스와의 연결을 종료하였습니다.')


def select_student(stu_id):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }

        connection = mysql.connector.connect(**connection)

        # 쿼리 실행
        cursor = connection.cursor()

        # 예시 쿼리: 모든 학생 정보 가져오기
        query = "SELECT * FROM student WHERE stu_id = %s;"
        cursor.execute(query, (stu_id,))

        # 쿼리 결과 가져오기
        row = cursor.fetchone()

        # 결과 출력
        if row:
            return studentVO.StudentVO(row[1],row[2], row[3], row[0], row[4], row[5], row[6])
        else:
            print(f'주어진 stu_id({stu_id})에 해당하는 학생을 찾을 수 없습니다.')
            return None

    except mysql.connector.Error as error:
        print(f'MySQL 에러 발생: {error}')
    finally:
        try:
            cursor.close()
        except NameError:
            pass

        try:
            connection.close()
        except mysql.connector.Error as e:
            print('Error occurred while closing the connection:', e)

        print('데이터베이스와의 연결을 종료하였습니다.')
