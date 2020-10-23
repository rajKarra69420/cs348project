import mysql.connector

cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
cursor = cnx.cursor()
query = "SELECT product_id, product_name, price FROM Products" # a query populated by the following if-statements
cursor.execute(query)

for (product_id, product_name, price) in cursor:
    print(str(product_id) + ", " + str(product_name) + ", " + str(price))
cursor.close()