from flask import (
    Flask,
    request,
    jsonify
)
import mysql.connector
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "test"

# example http://127.0.0.1:5000/addProduct?product_name=pencil&price=5&type=schoolgear
# you need to GET this page with the product_name, price, and type arguments
# spaces indicated by "%20"
@app.route('/addProduct')
def addProduct():
    print("addProduct")
    new_product_name = "'" + request.args.get('product_name') + "'"
    new_price = request.args.get('price')
    new_type = "'" + request.args.get('type') + "'"

    print("one: " + new_product_name + "\n")
    print("two: " + new_price + "\n")
    print("three: " + new_type + "\n")

    cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    query = "INSERT INTO Products (product_name, price, type) VALUES (" + new_product_name + ", " + str(new_price) + ", " + new_type + ");" # a query populated by the following if-statements
    print("query: " + query + "\n")
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    response = jsonify(message="OK")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


# example http://127.0.0.1:5000/addToCart?product_id=1&cust_id=2&quantity=5&total=100
# the "total" should be the quantity * price of the product_id in the Products table
# product_id should be an actual product_id that exists in Products table
# cust_id should be an actual cust_id that exists in Customers table
# spaces indicated by "%20"
@app.route('/addToCart')
def addToCart():
    print("addToCart")

    product_id = request.args.get('product_id')
    cust_id = request.args.get('cust_id')
    quantity = request.args.get('quantity')
    total = "'" + request.args.get('total') + "'"

    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')

    cursor = cnx.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")
    cursor.execute("INSERT INTO Cart_Item (total, quantity, product_id) VALUES(" + str(total) + ", " + str(quantity) + ", " + str(product_id) + ");")
    cursor.execute("SELECT MAX(cart_item_id) FROM Cart_Item;")
    current_id = -1
    for (cart_item_id) in cursor:
        current_id = str(cart_item_id)
    current_id = current_id.replace('(', '')
    current_id = current_id.replace(')', '')
    current_id = current_id.replace(',', '')
    print("current_id: " + str(current_id))
    cursor.execute("SELECT cart_id FROM Cart WHERE cust_id = " + cust_id)
    val = str(cursor.fetchall())
    if val == '[]':
        cursor.execute("INSERT INTO Cart (cart_item_id, cust_id) VALUES(" + str(current_id) + ", " + str(cust_id) + ");")
    else:
        val = val.replace('[', '')
        val = val.replace(']', '')
        val = val.split(',', 1)[0]
        val = val.replace('(', '')
        val = val.replace(')', '')
        cursor.execute(
            "INSERT INTO Cart (cart_id, cart_item_id, cust_id) VALUES(" + str(val) + ", " + str(current_id) + ", " + str(cust_id) + ");")
    cnx.commit()
    cursor.close()

    response = jsonify(message="OK")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response




# example http://127.0.0.1:5000/registerCustomer?username=vikasdorn&password=password1&address=557%20Cherrywood%20Lane&email_address=vikasdorn@gmail.com
# you need to GET this page with the username, password, address (where spaces are "%20"), and email_address arguments
@app.route('/registerCustomer')
def registerCustomer():
    print("registerCustomer")
    new_username = "'" + request.args.get('username') + "'"
    new_password = "'" + request.args.get('password') + "'"
    new_address =  "'" + request.args.get('address') + "'".replace("%20", " ") # replace b/c spaces are represented by %20
    new_email = "'" + request.args.get('email_address') + "'"
    print("one: " + new_username + "\n")
    print("two: " + new_password + "\n")
    print("three: " + new_address + "\n")
    print("four: " + new_email + "\n")

    cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    query = "INSERT INTO Customer (username, password, address, email_address) VALUES (" + new_username + ", " + new_password + ", " + new_address + ", " + new_email + ");" # a query populated by the following if-statements
    print("query: " + query + "\n")
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    response = jsonify(message="OK")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

# example http://127.0.0.1:5000/getProducts 
@app.route('/getProducts')
def getProducts():
    print("getProducts")

    cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()

    returnDict = {}
    query = "SELECT product_id, product_name, price FROM Products" # a query populated by the following if-statements
    cursor.execute(query)

    for (product_id, product_name, price) in cursor:
       returnDict[product_id] = [product_name, '{0:.2f}'.format(price)]
    cursor.close()
    response = jsonify(returnDict)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

  #the logic is right but I'm not sure how to integrate this in the backend
  #@app.route() what do I do here
  def getCustomerProducts(cust):
	cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
	cursor = cnx.cursor()
	sql_get_cart_item_id = “SELECT cart_item_id FROM Cart_Item WHERE cust_id =“ + str(cust.cust_id)
	cursor.execute(sql_get_cart_item_id)
	rows = cursor.fetchall()
	if(len(r) == 0):
		return
	product_ids = []
	for each r in rows:
		sql_get_productIds = “SELECT product_id FROM Cart_Item WHERE cart_item_id = “ + str(r)
		cursor.execute(sql_get_productIds)
	results = cursor.fetchall()
	if(len(results) == 0):
		continue
	product_ids.append(results[0])
	
	for p in product_ids:
		sql_get_product_name = “SELECT product_name FROM Products WHERE product_id = ” + str(p)
		cursor.execute(sql_get_product_name)
		results = cursor.fetchall()
		if(len(results) == 0):
			continue
		product_names.append(results[0])
      cursor.close()
      #do I convert product_names to dict to jsonify?
	return product_names

	
if __name__ == "__main__":
    app.run(debug=True)
