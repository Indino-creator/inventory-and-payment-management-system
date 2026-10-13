import mysql.connector # Or sqlite3 depending on what you are using

# 1. Create the connection at the top level
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Armaan",      # Replace with your MySQL password
    database="inventory"  # Replace with your database name
)

# 2. Create the cursor at the top level
cursor = conn.cursor()

# Optional: Keep your establish_conn function if you want a print message or extra checks
def establish_conn():
    if conn.is_connected():
        print("Database connected successfully!")