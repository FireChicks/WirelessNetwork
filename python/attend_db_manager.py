import mysql.connector
from datetime import datetime

def read_file(dir):
    try:
        with open(f'{dir}', 'rb') as file:
            image_data = file.read()
        return image_data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except IOError as e:
        print("파일을 읽는 중 오류가 발생했습니다:", e)
    except Exception as e:
        print("알 수 없는 오류가 발생했습니다:", e)

def insert_attend_by_fp(stu_id, att_way, class_code):
    try:
        img = read_file('./finger_print_auth_img.png')
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }
        connection = mysql.connector.connect(**connection)

        if connection.is_connected():
            now = datetime.now()

            # 쿼리 실행
            cursor = connection.cursor()

            insert_query = "INSERT INTO att (class_code, stu_id, att_date, att_state, att_way, img) VALUES (%s, %s, NOW(), %s, %s, %s)"
            att_data = (class_code, stu_id, '1', att_way, img)
            cursor.execute(insert_query, att_data)

            connection.commit()
            print(f'데이터베이스에 성공적으로 {stu_id}의 출석을 입력 하였습니다.')
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

def insert_attend(stu_id, img, att_way, class_code):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }
        connection = mysql.connector.connect(**connection)

        if connection.is_connected():
            now = datetime.now()

            # 쿼리 실행
            cursor = connection.cursor()

            insert_query = "INSERT INTO att (class_code, stu_id, att_date, att_state, att_way, img) VALUES (%s, %s, NOW(), %s, %s, %s)"
            att_data = (class_code, stu_id, '1', att_way, img)
            cursor.execute(insert_query, att_data)

            connection.commit()
            print(f'데이터베이스에 성공적으로 {stu_id}의 출석을 입력 하였습니다.')
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
