# Net profit calculator with basic statistics using pandas and numpy

import os
import sys
import pandas as pd
import numpy as np

# Add the root project directory ('just a cs project') to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main_code.database_connections.database_connect import establish_conn, conn

# Establish the database connection
establish_conn()

def calculate_net_profit():
    try:
        # Load the payments table into a pandas DataFrame
        query = "SELECT * FROM payments"
        df = pd.read_sql(query, conn)
        
        # Check if the DataFrame is empty or missing the AMOUNT column
        if df.empty or 'AMOUNT' not in df.columns:
            print("\nNo payment data available to analyze.")
            return
            
        # Convert the AMOUNT column into a NumPy array for fast stats calculation
        amounts = df['AMOUNT'].to_numpy(dtype=float)
        
        # Financial metrics
        total_revenue = np.sum(amounts)
        total_transactions = len(amounts)
        estimated_expenses = 0.0  # Adjust this if you track expenses in a table
        net_profit = total_revenue - estimated_expenses
        
        # Basic statistical metrics using NumPy
        mean_payment = np.mean(amounts)
        median_payment = np.median(amounts)
        min_payment = np.min(amounts)
        max_payment = np.max(amounts)
        std_deviation = np.std(amounts)
        
        # Display the results neatly in the terminal
        print("\n" + "=" * 50)
        print(f"{'FINANCIAL SUMMARY & NET PROFIT':^50}")
        print("=" * 50)
        print(f"Total Transactions Recorded: {total_transactions}")
        print(f"Total Revenue Collected:     ${total_revenue:,.2f}")
        print(f"Total Estimated Expenses:    ${estimated_expenses:,.2f}")
        print("-" * 50)
        print(f"Net Profit:                  ${net_profit:,.2f}")
        print("=" * 50)
        
        print(f"{'BASIC PAYMENT STATISTICS':^50}")
        print("-" * 50)
        print(f"Average (Mean) Payment:      ${mean_payment:,.2f}")
        print(f"Median Payment:              ${median_payment:,.2f}")
        print(f"Lowest Payment:              ${min_payment:,.2f}")
        print(f"Highest Payment:             ${max_payment:,.2f}")
        print(f"Standard Deviation:          ${std_deviation:,.2f}")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error calculating financial stats: {e}")

# Run the function directly
calculate_net_profit()