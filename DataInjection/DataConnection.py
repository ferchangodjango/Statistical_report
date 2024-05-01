import mysql.connector

try:
    connection=mysql.connector.connect(
        host='192.168.1.200',
        port=3306,
        user='remoteuser',
        password='1234',
        db='Packed_company'
    )
    print("coneccion exitosa")

except Exception as ex:
    raise Exception(ex)

