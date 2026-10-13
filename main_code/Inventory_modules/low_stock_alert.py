import os
import sys

# Add the 'main code' folder to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# NOW import from database_connections
from database_connections.database_connect import establish_conn, cursor, conn

establish_conn()

def check_low_stock():
    threshold = 5
    
    # Use UNION ALL to query each category table separately without ambiguity
    query = """
        SELECT product_name, product_brand, product_quantity FROM groceries WHERE product_quantity <= %s
        UNION ALL
        SELECT product_name, product_brand, product_quantity FROM dairy_products WHERE product_quantity <= %s
        UNION ALL
        SELECT product_name, product_brand, product_quantity FROM household_products WHERE product_quantity <= %s
    """
    
    try:
        # Pass the threshold value three times (once for each %s placeholder)
        cursor.execute(query, (threshold, threshold, threshold))
        low_stock_items = cursor.fetchall()
        
        if not low_stock_items:
            print("Stock levels are healthy. No items are running low.")
        else:
            print("\n⚠️ LOW STOCK ALERT ⚠️")
            print("-" * 50)
            for item in low_stock_items:
                product_name, brand, quantity = item
                print(f"Product: {product_name} | Brand: {brand} | Remaining: {quantity}")
            print("-" * 50)
                
    except Exception as e:
        print(f"Error checking stock: {e}")

check_low_stock()