import mysql.connector
from datetime import datetime

def insert_class(class_code, class_name, prof_id):
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

            insert_query = "INSERT INTO class (class_code, prof_id, class_name) VALUES (%s, %s, %s)"
            att_data = (class_code,prof_id, class_name)
            cursor.execute(insert_query, att_data)

            connection.commit()
            print(f'데이터베이스에 성공적으로 {class_name}의 수업을 입력 하였습니다.')
            print('')
            print(f'<-------------------------------------------------------------------->')
            print('주의) 출석을 실행하기전에 현재 존재하는 학생들의 모델학습을 업데이트하여야 합니다.')
            print(f'<-------------------------------------------------------------------->')
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


def check_class(class_code):
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
        query = "SELECT * FROM class WHERE class_code = %s;"
        cursor.execute(query, (class_code,))

        # 쿼리 결과 가져오기
        row = cursor.fetchone()

        # 결과 출력
        if row:
            return True
        else:
            print(f'주어진 class_code({class_code})에 해당하는 수업을 찾을 수 없습니다.')
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

def select_model(class_code):
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
        query = "SELECT * FROM class WHERE class_code = %s;"
        cursor.execute(query, (class_code,))

        # 쿼리 결과 가져오기
        row = cursor.fetchone()

        # 결과 출력
        if row[3] == None:
            print(f'주어진 수업의 모델을 찾을 수 없습니다. 먼저 모델 학습을 진행해 주세요.')
            return None
        else:
            return row[3]

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

def check_all_class():
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
        query = "SELECT * FROM class;"
        cursor.execute(query,)

        # 쿼리 결과 가져오기
        rows = cursor.fetchall()

        if rows == None:
            print(f'강의가 존재하지 않습니다.')
            return

        for row in rows:
            print(f'class_code : {row[0]}, class_name : {row[2]} ')



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

def update_model(class_model, class_code):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }

        connection = mysql.connector.connect(**connection)
        cursor = connection.cursor()

        update_query = "UPDATE class SET class_model = %s WHERE class_code = %s;"
        cursor.execute(update_query, (class_model,class_code))  # class_code와 class_model만 업데이트
        connection.commit()
        print(f"class_code :{class_code}의 모델이 업데이트되었습니다.")

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