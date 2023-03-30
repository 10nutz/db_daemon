from datetime import timezone
import mysql.connector
import jwt
import datetime



try:
    connection = mysql.connector.connect(host='aws.connect.psdb.cloud',
                                        database='userdatabase',
                                        user='r7h5k8v6c56bvaby4nve',
                                        password='pscale_pw_G54UIDrFMiD3Me9T9bv6OFPPyFtImGb87AvgQ3pQE9p')
    
    sql_Select_query = """select token from refreshtoken"""
    sql_Select_query2 = """select expiration_date from codes"""
    sql_Delete_query = "delete from refreshtoken where token = %s"
    sql_Delete_query2 = "delete from codes where expiration_date = %s"

    records_to_delete = []
    records_to_delete2 = []
    cursor = connection.cursor()
    cursor2= connection.cursor()

    cursor.execute(sql_Select_query)
    records = cursor.fetchall()

    cursor2.execute(sql_Select_query2)
    records2 = cursor2.fetchall()

    for token in records:
        decoded = jwt.decode(''.join(token).lstrip('(\'').rstrip('\',)'), options={"verify_signature": False})
        if(decoded['exp'] < datetime.datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()):
            records_to_delete.append(token)

    for token in records_to_delete:
        cursor.executemany(sql_Delete_query, (token, ))
        
    connection.commit()
    if not records_to_delete:
        print( " Record Deleted successfully")

    for exp_date in records2:
        if(float(str(exp_date)[1:-2]) < datetime.datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()*1000):
            records_to_delete2.append(exp_date)

    for exp_date in records_to_delete2:
        cursor.executemany(sql_Delete_query2, (exp_date, ))
    connection.commit()
    if not records_to_delete2:
        print( " Record Deleted successfully")

except mysql.connector.Error as error:
    print("Failed to Delete records from MySQL table: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
