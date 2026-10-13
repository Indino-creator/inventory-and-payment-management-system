'here we will make a python program to insert a product in to mysql database'
import mysql.connector

import os
import sys

# 1. Add the root directory to path to access database connections
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connections.database_connect import establish_conn, cursor, conn
from database_connections.Database_end import end_connection

establish_conn()


def insert_product():
    Product_brand=input(str("Enter the brand of the product- "))
    Product_name=input(str("Enter the name of the product"))
    Product_description=input(str("Enter the description of the product"))
    Product_quantity=int(input("Enter the quantity of the product"))
    Purchase_price=int(input("Enter the price of the product you purchase from the distribuitor "))
    our_price=int(input("Enter how much cost you will add to the product- "))
    selling_price=int(input("Enter the selling price of the product-"))
    Product_weight=input(str("Enter the weight of the product"))


    query = '''
INSERT INTO groceries
(product_brand, product_name, desription, product_quantity,
 purchase_price, our_cost, selling_price, product_weight)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
'''
    values=(Product_brand,Product_name,Product_description,Product_quantity,Purchase_price,our_price,selling_price,Product_weight)
    end_connection(query,values)

insert_product()