import mysql.connector

cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
# cursor = cnx.cursor()
# query = "INSERT INTO Cart_Item (total, quantity, product_id) VALUES('100.00', 2, 1)"
# cursor.execute(query)
# cnx.commit()
# cursor.close()
#
# cursor = cnx.cursor()
# query = "SELECT cart_item_id FROM Cart_Item" # a query populated by the following if-statements
# cursor.execute(query)

# cursor = cnx.cursor()
# query = "INSERT INTO Cart (cart_item_id, cust_id) VALUES(6, 1)"
# cursor.execute(query)
# cnx.commit()
# cursor.close()
cursor = cnx.cursor()
query = "SELECT cart_id FROM Cart" # a query populated by the following if-statements
cursor.execute(query)


for (cart_id) in cursor:
    print(str(cart_id))
cursor.close()