from flask import (
    Flask,
    request
)
import mysql.connector
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "test"

# example http://127.0.0.1:5000/addProduct?product_name=pencil&price=5
# you need to GET this page with the product_name and price arguments
@app.route('/addProduct')
def addProduct():
    print("addProduct")
    new_product_name = "'" + request.args.get('product_name') + "'"
    new_price = request.args.get('price')

    print("one: " + new_product_name + "\n")
    print("two: " + new_price + "\n")

    cnx = mysql.connector.connect(user='root', password= '',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    query = "INSERT INTO Products (product_name, price) VALUES (" + new_product_name + ", " + new_price + ");" # a query populated by the following if-statements
    print("query: " + query + "\n")
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    return 'OK'


# example http://127.0.0.1:5000/registerCustomer?username=vikasdorn&password=password1&address=557%20Cherrywood%20Lane&email_address=vikasdorn@gmail.com
# you need to GET this page with the product_name and price arguments
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

    return 'OK'

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

    return json.dumps(returnDict)



if __name__ == "__main__":
    app.run(debug=True)