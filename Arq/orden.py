import mysql.connector
from mysql.connector import errorcode
import cgi

data = cgi.FieldStorage()

nombre = data.getvalue('name')
apellido = data.getvalue('apellido')
direccion = data.getvalue('direccion')
email = data.getvalue('email')
fecha  = data.getvalue('fecha')
telefono = data.getvalue('phone')
cantidad = data.getvalue('Cantidad')
cantidad2 = data.getvalue('Cantidad2')
cantidad3 = data.getvalue('Cantidad3')
cantidad4 = data.getvalue('Cantidad4')

try:
    cnx = mysql.connector.connect(user='Juan', password='Juan2001', database='laperrada', host='127.0.0.1')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cur = cnx.cursor()
    print('Content-Type: text/html')
    print('')
    sql = ("insert into orden values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(nombre,apellido,direccion,email,fecha,telefono,cantidad,cantidad2,cantidad3,cantidad4))
    cur.execute(sql)
    cnx.commit()
    print('conectado')
cnx.close()
