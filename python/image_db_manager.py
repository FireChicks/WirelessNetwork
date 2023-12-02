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
def delete_img(stu_id):
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
        query = "DELETE FROM image WHERE stu_id = %s"

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

def select_img(stu_id):
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
        query = "SELECT * FROM image where stu_id = %s;"
        cursor.execute(query, (stu_id,))

        # 쿼리 결과 가져오기
        rows = cursor.fetchall()

        if rows == None:
            print(f'이미지가 존재하지 않습니다.')
            return

        for index, row in enumerate(rows):
            image_data = row[2]  # 이미지 데이터는 row[2]에 있다고 가정합니다

            # 파일 경로 생성
            file_path = f'./face_data/{row[1]}.{index}.jpg'  # 파일 경로 생성, row[3]는 이미지 확장자로 가정합니다

            # 이미지 데이터를 파일로 저장
            with open(file_path, 'wb') as file:
                file.write(image_data)

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