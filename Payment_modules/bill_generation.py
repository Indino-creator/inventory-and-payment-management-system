from payments_insert import loc
import mysql.connector

# Prompt user to enter a Payment ID dynamically
target_payment_id = loc

try:
    # 1. Connect to your MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # Replace with your MySQL username
        password="----",   # Replace with your MySQL password
        database="inventory" # Replace with your database name
    )
    
    cursor = connection.cursor(dictionary=True)
    
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
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()