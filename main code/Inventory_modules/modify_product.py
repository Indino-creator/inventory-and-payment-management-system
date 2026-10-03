# Here we will enter the product that are sold during the day 

import mysql.connector

# Here we will try connecting to database 
try:
    connection = mysql.connector.connect(
        host="localhost",
        database="inventory",
        user="root",
        password="Armaan"
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # we will get the user input to modify the product details
        new_value = input("Enter the new value: ")
        direction = input("Enter the name of the product you want to update the quantity")
        
        # here we will make the sql query which will be ran eventually
        sql_update_query = f"""UPDATE groceries
                              SET product_quantity = %s 
                              WHERE product_name = %s"""
        
        # excution of the query
        input_data = (new_value, direction)
        cursor.execute(sql_update_query, input_data)
        
        # we will commit here
        connection.commit()
        print(f"Record updated successfully. {cursor.rowcount} record(s) affected.")
        
except mysql.connector.Error as error:
    print("Failed to update record: {}".format(error))
    
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")   
        # And finally we will close the connection 