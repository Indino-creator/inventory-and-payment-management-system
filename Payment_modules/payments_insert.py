# Here we will input the payment that customers made during the day

# All the payment will be registered by the shop keeper at the time of the payment
import os
import sys

# 1. Add the root project directory ('just a cs project') to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2. Import your database modules
from main_code.database_connections.database_connect import establish_conn, cursor, conn
from main_code.database_connections.Database_end import end_connection
establish_conn()

# Initialize global variable to prevent potential NameErrors
data_location = None

def insert_payment():
    global data_location
    person_name = str(input("Enter the name of the person- "))
    product_name = str(input("Enter the product name "))
    product_brand = str(input("Enter the product brand- "))
    payment_type = str(input("Enter type of the payment (paid/pending)- "))
    amount = int(input("Enter the amount of the payment- "))
    payment_method = str(input("Enter the method of the payment- "))
    description = str(input("Enter the description of the payments "))

    query = """INSERT INTO payments(
        PERSON_NAME,
        PRODUCT_NAME,
        PRODUCT_BRAND,
        PAYMENT_TYPE,
        AMOUNT,
        PAYMENT_METHOD,
        DESCRIPTION
    ) values(%s,%s,%s,%s,%s,%s,%s)"""

    values = (person_name, product_name, product_brand, payment_type, amount, payment_method, description)

    end_connection(query, values)
    
    # Capture the last inserted row id
    data_location = cursor.lastrowid
    return 

# Run the function
insert_payment()            

# Here we will store the bill data so that we can pass it for the bill generation
loc = data_location