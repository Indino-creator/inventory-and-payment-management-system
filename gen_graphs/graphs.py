# Graph generator for inventory stock levels (Pure procedural, saves to graphs folder)

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add the root project directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main_code.database_connections.database_connect import establish_conn, conn

# Establish the database connection
establish_conn()

try:
    # Query inventory data from all category tables with category labels
    q_groceries = "SELECT product_name, product_quantity, 'Groceries' AS category FROM groceries"
    q_dairy = "SELECT product_name, product_quantity, 'Dairy' AS category FROM dairy_products"
    q_household = "SELECT product_name, product_quantity, 'Household' AS category FROM household_products"
    
    # Read data into pandas DataFrames
    df_groceries = pd.read_sql(q_groceries, conn)
    df_dairy = pd.read_sql(q_dairy, conn)
    df_household = pd.read_sql(q_household, conn)
    
    # Combine all tables into a single DataFrame
    df = pd.concat([df_groceries, df_dairy, df_household], ignore_index=True)
    
    if df.empty:
        print("\nNo inventory data available to graph.")
    else:
        # Set Seaborn styling theme
        sns.set_theme(style="whitegrid")
        
        # Create the plot window
        plt.figure(figsize=(12, 6))
        
        # Draw a bar plot showing product quantities grouped by category
        sns.barplot(
            data=df, 
            x='product_name', 
            y='product_quantity', 
            hue='category', 
            palette='Set2',
            dodge=False
        )
        
        # Formatting chart labels and layout
        plt.title('Inventory Stock Levels by Product', fontsize=16, fontweight='bold', pad=15)
        plt.xlabel('Product Name', fontsize=12, fontweight='bold')
        plt.ylabel('Stock Quantity', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Category')
        plt.tight_layout()
        
        # Ensure the target 'graphs' directory exists in the root project folder
        graphs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../graphs"))
        os.makedirs(graphs_dir, exist_ok=True)
        
        # Define file path and save the figure
        save_path = os.path.join(graphs_dir, "inventory_stock_levels.png")
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nGraph successfully saved to: {save_path}")
        
        # Display the plot window
        plt.show()
        
except Exception as e:
    print(f"Error generating or saving graph: {e}")