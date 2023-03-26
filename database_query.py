from datetime import timezone
import mysql.connector
import jwt
import datetime

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='example',
                                         user='root',
                                         password='root')
    
    sql_Select_query = """select token from refreshtoken"""
    sql_Delete_query = "delete from refreshtoken where token = %s"

    records_to_delete = []
    cursor = connection.cursor()

    cursor.execute(sql_Select_query)
    records = cursor.fetchall()

    for token in records:
        decoded = jwt.decode(''.join(token).lstrip('(\'').rstrip('\',)'), options={"verify_signature": False})
        if(decoded['exp'] < datetime.datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()):
            cursor.executemany(sql_Delete_query, (token, ))

    for token in records_to_delete:
        cursor.executemany(sql_Delete_query, (token, ))
    connection.commit()
    print( " Record Deleted successfully")

except mysql.connector.Error as error:
    print("Failed to Delete records from MySQL table: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
