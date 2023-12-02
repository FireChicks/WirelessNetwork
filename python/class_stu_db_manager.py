import mysql.connector
from datetime import datetime

def is_enroll(class_code, stu_id):
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
        query = "SELECT * FROM class_stu WHERE class_code = %s AND stu_id = %s;"
        cursor.execute(query, (class_code, stu_id))

        # 쿼리 결과 가져오기
        row = cursor.fetchone()

        # 결과 출력
        if row:
            return False
        else:
            return True

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


def insert_class_stu(class_code, stu_id):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }
        connection = mysql.connector.connect(**connection)

        if connection.is_connected():
            # 쿼리 실행
            cursor = connection.cursor()

            insert_query = "INSERT INTO class_stu (class_code, stu_id) VALUES (%s, %s)"
            cls_stu_data = (class_code, stu_id)
            cursor.execute(insert_query, cls_stu_data)

            connection.commit()
            print(f'데이터베이스에 성공적으로 수강 정보를 입력 하였습니다.')
            return True
        else:
            return False
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

def check_students(class_code):
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
        query = "SELECT * FROM class_stu where class_code = %s;"
        cursor.execute(query,(class_code,))

        # 쿼리 결과 가져오기
        rows = cursor.fetchall()

        if rows == None:
            return None

        stu_ids = []

        for row in rows:
            stu_ids.append(row[2])
        return stu_ids


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


def check_prof(prof_id):
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
        query = "SELECT * FROM prof WHERE prof_id = %s;"
        cursor.execute(query, (prof_id,))

        # 쿼리 결과 가져오기
        row = cursor.fetchone()

        # 결과 출력
        if row:
            return True
        else:
            print(f'주어진 prof_id({prof_id})에 해당하는 교수를 찾을 수 없습니다.')
            return False

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
