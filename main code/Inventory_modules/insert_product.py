'here we will make a python program to insert a product in to mysql database'
import mysql.connector


  # Establish connection
conn = mysql.connector.connect(
    host="localhost",       # or your database host
    user="root",   # MySQL username
    password="Armaan", # MySQL password
    database="inventory" # Optional: specific database
)
cursor=conn.cursor()

# Verify connection
if conn.is_connected():
    print("Connected to MySQL database")


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

    try:
        # 4. Execute the query
        cursor.execute(query, values)
        
        # 5. Commit the transaction
        conn.commit()
        print(f"Record inserted successfully. ID: {cursor.lastrowid}")
        print("Thanks for using our software")
        
    except mysql.connector.Error as error:
        # Rollback in case of error
        conn.rollback()
        print(f"Failed to insert record: {error}")
    finally:
        # 6. Close resources
        if conn.is_connected():
            cursor.close()
            conn.close()

insert_product()