# Here we will enter the product that are sold during the day 
import os
import sys

# Add the 'main code' folder to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database_connections.database_connect import establish_conn, cursor, conn
from database_connections.Database_end import end_connection

# Here we will try connecting to database 
establish_conn()

# Get user input with correct variable names and data types
new_value = int(input("Enter the new quantity value: "))
product_name = input("Enter the name of the product you want to update the quantity: ")

# SQL update query
sql_update_query = """UPDATE groceries
                      SET product_quantity = %s
                      WHERE product_name = %s"""

# Pass the query and the parameters tuple correctly
end_connection(sql_update_query, (new_value, product_name))