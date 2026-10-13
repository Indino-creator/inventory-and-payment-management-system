# Here we will search for products in the inventory database

import os
import sys

# Add the parent folder to Python's search path to find database connections
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database_connections.database_connect import establish_conn, cursor, conn

# Establish database connection
establish_conn()

def find_stock():
    # Get the search term from the user
    search_term = input("Enter the product name or brand you want to search for: ")
    
    # Query checking all category tables using UNION ALL and LIKE for flexible searching
    query = """
        SELECT product_name, product_brand, product_quantity FROM groceries WHERE product_name LIKE %s OR product_brand LIKE %s
        UNION ALL
        SELECT product_name, product_brand, product_quantity FROM dairy_products WHERE product_name LIKE %s OR product_brand LIKE %s
        UNION ALL
        SELECT product_name, product_brand, product_quantity FROM household_products WHERE product_name LIKE %s OR product_brand LIKE %s
    """
    
    # Wrap the search term in wildcards (%) so partial names match too
    like_term = f"%{search_term}%"
    
    try:
        # Pass the search term for each placeholder (6 placeholders total: name & brand for 3 tables)
        cursor.execute(query, (like_term, like_term, like_term, like_term, like_term, like_term))
        results = cursor.fetchall()
        
        if not results:
            print(f"\nNo products found matching '{search_term}'.")
        else:
            print(f"\n🔍 SEARCH RESULTS FOR '{search_term}' 🔍")
            print("-" * 60)
            for item in results:
                product_name, brand, quantity = item
                print(f"Product: {product_name:<20} | Brand: {brand:<15} | Quantity: {quantity}")
            print("-" * 60)
                
    except Exception as e:
        print(f"Error searching stock: {e}")

# Run the function directly
find_stock()