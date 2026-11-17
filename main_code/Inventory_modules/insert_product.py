import os
import sys
import difflib
import mysql.connector

# Add the root project directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main_code.database_connections.database_connect import establish_conn, cursor, conn
from main_code.database_connections.Database_end import end_connection

print("--- INVENTORY MANAGEMENT SYSTEM ---")

while True:
    print("\n==============================")
    print("1. Insert Product")
    print("2. Modify Product")
    print("3. Exit")
    print("==============================")
    
    choice = input("Choose an option (1-3): ").strip()
    
    if choice == '1':
        print("\n--- Insert New Product ---")
        print("Available tables: groceries, dairy_products, household_products")
        table_name = input("Enter the table name: ").strip().lower()

        product_brand = input("Enter the brand of the product: ").strip()
        product_name = input("Enter the name of the product: ").strip()
        product_description = input("Enter the description of the product: ").strip()
        product_quantity = int(input("Enter the quantity of the product: "))
        purchase_price = int(input("Enter purchase price from distributor: "))
        our_cost = int(input("Enter cost added to the product: "))
        selling_price = int(input("Enter selling price of the product: "))
        product_weight = input("Enter the weight of the product: ").strip()

        query = f"""
        INSERT INTO {table_name}
        (product_brand, product_name, desription, product_quantity,
         purchase_price, our_cost, selling_price, product_weight)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            product_brand, product_name, product_description, product_quantity,
            purchase_price, our_cost, selling_price, product_weight
        )
        
        establish_conn()
        end_connection(query, values)
        print("Product successfully inserted!")

    elif choice == '2':
        print("\n--- Modify Existing Product ---")
        print("Available tables: groceries, dairy_products, household_products")
        table_name = input("Enter the table name: ").strip().lower()

        search_name = input("Enter the product name you want to modify: ").strip()
        
        # Fetch existing product names for fuzzy matching / typo check
        cur = None
        all_names = []
        try:
            establish_conn()
            cur = conn.cursor()
            cur.execute(f"SELECT product_name FROM {table_name}")
            rows = cur.fetchall()
            all_names = [row[0] for row in rows]
        except Exception as e:
            print(f"Error fetching product list: {e}")
        finally:
            if cur is not None:
                cur.close()

        if not all_names:
            print("No products found in this table.")
            continue

        target_name = search_name
        if search_name not in all_names:
            matches = difflib.get_close_matches(search_name, all_names, n=1, cutoff=0.4)
            if matches:
                suggestion = matches[0]
                typo_choice = input(f"Product '{search_name}' not found exactly. Did you mean '{suggestion}'? (y/n): ").strip().lower()
                if typo_choice in ['y', 'yes']:
                    target_name = suggestion
                else:
                    print("Modification cancelled.")
                    continue
            else:
                print(f"No close matches found for '{search_name}'.")
                continue

        print(f"\nModifying product: '{target_name}'")
        print("Enter new values (leave blank to keep current values):")
        
        new_quantity = input("Enter new quantity: ").strip()
        new_selling_price = input("Enter new selling price: ").strip()

        updates = []
        values = []

        if new_quantity:
            updates.append("product_quantity = %s")
            values.append(int(new_quantity))
        if new_selling_price:
            updates.append("selling_price = %s")
            values.append(int(new_selling_price))

        if not updates:
            print("No changes provided.")
            continue

        values.append(target_name)
        update_query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE product_name = %s"

        establish_conn()
        end_connection(update_query, tuple(values))
        print("Product successfully modified!")

    elif choice == '3':
        print("Exiting program. Goodbye!")
        if conn is not None and conn.is_connected():
            conn.close()
        break
    else:
        print("Invalid choice. Please select 1, 2, or 3.")