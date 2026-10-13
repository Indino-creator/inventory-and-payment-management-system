from payments_insert import loc
import mysql.connector
import os
import sys

# 1. Add the root project directory ('just a cs project') to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2. Import your database modules
from database_connections.Database_end import end_connection 
from database_connections.database_connect import establish_conn,cursor,conn

# Prompt user to enter a Payment ID dynamically
target_payment_id = loc

try:
    establish_conn()
    
    cursor = conn.cursor(dictionary=True)
    
    # 2. Fetch the live record from the database
    query = "SELECT * FROM payments WHERE PAYMENT_ID = %s"
    cursor.execute(query, (target_payment_id,))
    record = cursor.fetchone()
    
    if record:
        # 3. Print the bill using the fetched database values
        print("\n" + "=" * 45)
        print(f"{'OFFICIAL INVOICE / RECEIPT':^45}")
        print("=" * 45)
        print(f"Payment ID   : {record['PAYMENT_ID']}")
        print(f"Date         : {record['PAYMENT_DATE']}")
        print(f"Customer Name: {record['PERSON_NAME']}")
        print("-" * 45)
        print(f"Product      : {record['PRODUCT_NAME']} ({record['PRODUCT_BRAND']})")
        print(f"Payment Type : {record['PAYMENT_TYPE']}")
        print(f"Method       : {record['PAYMENT_METHOD']}")
        print(f"Description  : {record['DESCRIPTION']}")
        print("-" * 45)
        print(f"{'Amount Due/Paid:':<30} ${record['AMOUNT']:<10.2f}")
        print("=" * 45)
        print(f"{'Thank you for your business!':^45}")
        print("=" * 45)
    else:
        print(f"\nNo payment record found with ID: {target_payment_id}")

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
    
finally:
    # Close connection properly
    if 'connection' in locals() and conn.is_connected():
        cursor.close()
        conn.close()