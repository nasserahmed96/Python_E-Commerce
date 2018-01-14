import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, date

order_date_time = date.today()

try:
    cnx = mysql.connector.connect(user = 'root', password = 'Nasora44', host = '127.0.0.1', database = 'Medical_Device_Company_DB')
    cursor = cnx.cursor(buffered = True)
    product_id = 12
    user_id = 3
    query = ("SELECT p_name, p_price, order_id FROM product, user_product WHERE p_id IN ("
            "SELECT p_id FROM user_product WHERE u_id = 3)")
    cursor.execute(query)
    for product_name, product_price, order_id in cursor:
        print("Product name: {} Product price {} order_id: {}".format(product_name, product_price, order_id))
    cnx.commit()
    cnx.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
        print("DB Error")
    else:
        print(err)
else:
    print("It's ok")
    cnx.close()

