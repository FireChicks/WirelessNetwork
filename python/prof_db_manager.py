import mysql.connector
from datetime import datetime

def insert_prof(prof_id, prof_name):
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

            insert_query = "INSERT INTO prof (prof_id, prof_name) VALUES (%s, %s)"
            att_data = (prof_id, prof_name)
            cursor.execute(insert_query, att_data)

            connection.commit()
            print(f'데이터베이스에 성공적으로 {prof_id}의 정보를 입력 하였습니다.')
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
