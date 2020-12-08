from flask import (
    Flask,
    request,
    jsonify
)
import mysql.connector
import json

class ProductTable:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='',
                                      host='34.72.148.165',
                                      database='shop')
        self.cursor = self.cnx.cursor()

    def addProduct(self, new_product_name, new_price, new_type):
        self.cursor = self.cnx.cursor(prepared=True)
        prepared_statement = "INSERT INTO Products (product_name, price, type) VALUES ();"
        # query = "INSERT INTO Products (product_name, price, type) VALUES (" + new_product_name + ", " + str(
        #    new_price) + ", " + new_type + ");"  # a query populated by the following if-statements
        prepared_query = "INSERT INTO Products (product_name, price, type) VALUES (%s,%s,%s)"
        tup = (str(new_product_name), str(new_price), str(new_type))
        self.cursor.execute(prepared_query, tup)
        print("query: " + prepared_query + "\n")
        self.cnx.commit()


        response = jsonify(message="OK")
        response.headers.add("Access-Control-Allow-Origin", "*")



        return response

    def getProducts(self):
        returnDict = {}
        query = "SELECT product_id, product_name, price FROM Products"  # a query populated by the following if-statements
        self.cursor.execute(query)

        for (product_id, product_name, price) in self.cursor:
            returnDict[product_id] = [product_name, '{0:.2f}'.format(price), product_id]
        self.cursor.close()
        response = jsonify(returnDict)
        response.headers.add("Access-Control-Allow-Origin", "*")

        self.reset()

        return response

    def groupByType(self):
        product_group_query = "SELECT product_name, sum(price) FROM Products GROUP BY type";
        self.cursor.execute(product_group_query)
        rows_group = self.cursor.fetchall()
        if (len(rows_group) == 0):
            return
        productGroupRet = {}
        for row in product_group_query:
            productGroupRet[row[0]] = '{0:.2f}'.format(row[1])
        response = jsonify(productGroupRet)
        response.headers.add("Access-Control-Allow-Origin", "*")

        self.reset()

        return response
    def reset(self):
        self.__init__()

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

    tool = ProductTable()
    return tool.addProduct(new_product_name, new_price, new_type)


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
    cursor.execute(
        "INSERT INTO Cart_Item (total, quantity, product_id, cust_id) VALUES(" + str(total) + ", " + str(quantity) + ", " + str(
            product_id) + ", " + str(cust_id) + ");")
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
        cursor.execute(
            "INSERT INTO Cart (cart_item_id, cust_id) VALUES(" + str(current_id) + ", " + str(cust_id) + ");")
    else:
        val = val.replace('[', '')
        val = val.replace(']', '')
        val = val.split(',', 1)[0]
        val = val.replace('(', '')
        val = val.replace(')', '')
        cursor.execute(
            "INSERT INTO Cart (cart_id, cart_item_id, cust_id) VALUES(" + str(val) + ", " + str(
                current_id) + ", " + str(cust_id) + ");")
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
    new_address = "'" + request.args.get('address') + "'".replace("%20",
                                                                  " ")  # replace b/c spaces are represented by %20
    new_email = "'" + request.args.get('email_address') + "'"
    print("one: " + new_username + "\n")
    print("two: " + new_password + "\n")
    print("three: " + new_address + "\n")
    print("four: " + new_email + "\n")

    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    query = "INSERT INTO Customer (username, password, address, email_address) VALUES (" + new_username + ", " + new_password + ", " + new_address + ", " + new_email + ");"  # a query populated by the following if-statements
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

    tool = ProductTable()
    return tool.getProducts()

@app.route('/getCustomerTotals')
def getCustomerTotal():
    cust_id = request.args.get('cust_id')
    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cursor.execute("SELECT SUM(total), SUM(quantity) FROM Cart_Item WHERE cust_id = %s", [(str(cust_id))])
    rows = cursor.fetchall()
    toReturn = {}
    workString = str(rows[0])
    toReturn['totalPrice'] = workString.split(',')[0].replace('(Decimal(', '').replace(")\"", '\"').replace(')', '').replace("'", '')
    toReturn['totalQuantity'] = workString.split(',')[1].replace(' Decimal(', '').replace(')', '').replace("'", '')
    response = jsonify(toReturn)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# example http://127.0.0.1:5000/getCustomerProducts?cust_id=5
@app.route('/getCustomerProducts')
def getCustomerProducts():
    #executemany: https://stackoverflow.com/questions/53185081/error-1210-incorrect-number-of-arguments-executing-prepared-statement/53185175
    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cust_id = request.args.get('cust_id')
    #cursor = cnx.cursor()
    cursor = cnx.cursor(prepared=True)
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cursor.execute("SELECT cart_item_id FROM Cart_Item WHERE cust_id = %s", [(str(cust_id))])
    rows = cursor.fetchall()
    if(len(rows) == 0):
        response = jsonify(message="EMPTY")
        return response
    product_ids = []
    for r in rows:
        cursor.execute("SELECT product_id FROM Cart_Item WHERE cart_item_id = %s", [(str(r[0]))])
        results = cursor.fetchall()
        if len(results) == 0:
            continue
        product_ids.append(results[0])

    returnDict = {}
    for p in product_ids:
        cursor.execute("SELECT product_id, product_name, price FROM Products WHERE product_id = %s", [(str(p[0]))])
        for (product_id, product_name, price) in cursor:
            returnDict[product_id] = [product_name, '{0:.2f}'.format(price)]
        cursor.execute("SELECT product_id, quantity FROM Cart_Item WHERE cust_id = %s AND product_id = %s", (cust_id, str(p[0])))
        for (product_id, quantity) in cursor:
            returnDict[product_id].append(quantity)
    cursor.close()

    response = jsonify(returnDict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/bestSellers")
def bestSellers():
    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    cursor.execute("SELECT b.product_name, a.product_id, SUM(amount) AS num FROM Transaction a JOIN Products b ON a.product_id = b.product_id GROUP BY a.product_id ORDER BY num DESC")
    r = cursor.fetchall()
    print(r[0])
    toReturn = {}
    toReturn['firstBest'] = {"product_name": r[0][0], "product_id": r[0][1], "quantity": str(r[0][2])}
    toReturn['secondBest'] = {"product_name": r[1][0], "product_id": r[1][1], "quantity": str(r[1][2])}
    toReturn['thirdBest'] = {"product_name": r[2][0], "product_id": r[2][1], "quantity": str(r[2][2])}

    response = jsonify(toReturn)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# example http://127.0.0.1:5000/groupByType
@app.route("/groupByType")
def groupByType():

    tool = ProductTable()
    return tool.groupByType()

#example http://127.0.0.1:5000/login?username=random&password=thing
@app.route("/login")
def login():
    username = "'" + request.args.get('username') + "'"
    password = "'" + request.args.get('password') + "'"
    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()

    query = "SELECT * FROM Customer WHERE username = " + str(username) + " AND password = " + str(password)
    cursor.execute(query)
    resp = cursor.fetchall()

    if str(resp) == "[]":
        response = jsonify("Invalid Details")
        response.headers.add("Access-Control-Allow-Origin", "*")
    else:
        response = jsonify(resp)
        response.headers.add("Access-Control-Allow-Origin", "*")

    return response

#example http://127.0.0.1:5000/addTransaction?cust_id=something
@app.route("/addTransaction")
def addTransaction():
    cust_id = request.args.get('cust_id')
    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")
    query = "SELECT quantity, product_id FROM Cart_Item WHERE cust_id = " + str(cust_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    if(len(rows) == 0):
        response = jsonify(message="EMPTY")
        return response
    for r in rows:
        query = "INSERT INTO Transaction (amount, cust_id, product_id) VALUES (" + str(r[0]) + ", " + str(cust_id) + ", " + str(r[1]) + ");"
        cursor.execute(query)
        cnx.commit()
    
    delete_cart = "DELETE FROM Cart WHERE cust_id = " + str(cust_id)
    cursor.execute(delete_cart)
    cnx.commit()
    delete_cart_items = "DELETE FROM Cart_Item WHERE cust_id = " + str(cust_id)
    cursor.execute(delete_cart_items)
    cnx.commit()
    cursor.close()

    response = jsonify(message="OK")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

#example http://127.0.0.1:5000/getTransactions?cust_id=something
@app.route('/getTransactions')
def showCustomerTransactions():
    cust_id = request.args.get('cust_id')
    cnx = mysql.connector.connect(user='root', password='',
                                  host='34.72.148.165',
                                  database='shop')
    cursor = cnx.cursor()   
    #query = "SELECT product_name, price FROM Products WHERE product_id IN (SELECT product_id FROM Transaction WHERE cust_id = " + str(cust_id) + ") "  + \
    #" ORDER BY product_id" # this allows us to ensure that we get the right amounts for each product
    cursor.execute(query)
    result = cursor.fetchall()
    if(len(result) == 0):
        response = jsonify(message="ERROR")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    returnDict = {}
    for r in result:
        query = "SELECT amount FROM Transaction WHERE cust_id = " + cust_id + "ORDER BY product_id"
        cursor.execute(query)
        re = cursor.fetchall()
        returnDict[r[0]] = (re[0], r[1])
    response = jsonify(returnDict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True)
