import os
import subprocess

# Completely flat procedural CLI menu (No classes, no functions)
while True:
    print("\n" + "=" * 45)
    print(f"{'CS PROJECT - MAIN CONTROL PANEL':^45}")
    print("=" * 45)
    print("1. Generate & Print Payment Bill / PDF")
    print("2. Insert New Payment Record")
    print("3. Insert/Manage Inventory Product")
    print("4. Calculate Net Profit")
    print("5. Generate Graphs")
    print("6. Exit")
    print("=" * 45)
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == '1':
        print("\n--- Running Bill & PDF Generator ---")
        script_path = os.path.join("Payment_modules", "pdf_generator.py")
        if os.path.exists(script_path):
            subprocess.run(["python", script_path])
        elif os.path.exists("pdf_generator.py"):
            subprocess.run(["python", "pdf_generator.py"])
        else:
            print("Error: Bill generation script not found.")
            
    elif choice == '2':
        print("\n--- Running Payment Insertion ---")
        script_path = os.path.join("Payment_module", "payments_insertion.py")
        if os.path.exists(script_path):
            subprocess.run(["python", script_path])
        else:
            print("Error: payments_insertion.py not found.")
            
    elif choice == '3':
        print("\n--- Running Inventory Management ---")
        script_path = os.path.join("main code", "Inventory_module", "insert_product.py")
        if os.path.exists(script_path):
            subprocess.run(["python", script_path])
        elif os.path.exists("insert_product.py"):
            subprocess.run(["python", "insert_product.py"])
        else:
            print("Error: Inventory script path not found.")
            
    elif choice == '4':
        print("\n--- Calculating Net Profit ---")
        script_path = os.path.join("data_extraction", "net_profit.py")
        if os.path.exists(script_path):
            subprocess.run(["python", script_path])
        else:
            print("Error: data_extraction/net_profit.py not found.")
            
    elif choice == '5':
        print("\n--- Generating Graphs ---")
        script_path = os.path.join("gen_graphs", "graphs.py")
        if os.path.exists(script_path):
            subprocess.run(["python", script_path])
        else:
            print("Error: gen_graphs/graphs.py not found.")
            
    elif choice == '6':
        print("\nExiting program. Goodbye!")
        break
    else:
        print("\nInvalid choice! Please enter a number between 1 and 6.")