import mysql.connector # Or sqlite3 depending on what you are using

# 1. Create the connection at the top level
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ar$$$",      # Replace with your MySQL password
    database="inventory"  # Replace with your database name
)

# 2. Create the cursor at the top level
cursor = conn.cursor()

# Optional: Keep your establish_conn function if you want a print message or extra checks
def establish_conn():
    if conn.is_connected():
        print("Database connected successfully!")
    else:
      try:
          cursor.exceute("""
            create database IF NOT EXIST Inventory
          """)
  
          cursor.excute("""
          CREATE TABLE IF NOT EXISTS products (
              product_id INT AUTO_INCREMENT PRIMARY KEY,
              product_brand VARCHAR(55) NOT NULL,
              product_name VARCHAR(55) NOT NULL,
              description VARCHAR(55),
              product_quantity INT NOT NULL,
              purchase_price INT NOT NULL,
              our_cost INT NOT NULL,
              selling_price INT NOT NULL,
              product_weight VARCHAR(55) NOT NULL,
              registration_date DATETIME,
              modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              ON UPDATE CURRENT_TIMESTAMP
          )
          """)    
  
          conn.commit()
  
          print("The Database is ready sir we are go to go ")

      except mysql.connector.Error as e:
          print("Mysql:",e)
      finally:
          if "cursor" in locals():
              cursor.close()
          if 'con' in locals and conn.is_connected():
              conn.close()       