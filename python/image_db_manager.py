import mysql.connector
import studentVO

def insert_images(stu_id, images):
    try:
        connection = {'host': '127.0.0.1',
                      'database': 'attend_board',
                      'user': 'root',
                      'password': 'root'
                      }
        connection = mysql.connector.connect(**connection)

        if connection.is_connected():
            print('MySQL 데이터베이스에 연결되었습니다.')

            # 쿼리 실행
            cursor = connection.cursor()
            for image in images :
                # 예시 데이터를 사용하여 테이블에 데이터 삽입
                insert_query = "INSERT INTO image (stu_id, img) VALUES (%s, %s)"
                image_data = (stu_id, image)
                cursor.execute(insert_query, image_data)
            # 변경사항 커밋
            connection.commit()
            print('데이터베이스에 성공적으로 이미지들을 입력 하였습니다.')
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

        print('데이터베이스와의 연결을 종료하였습니다.')