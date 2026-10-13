import os
import sys

# Ensure the root directory is in Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Use absolute import from the root project folder
from database_connections.database_connect import cursor, conn

def end_connection(query, values):
    try:
        cursor.execute(query, values)
        conn.commit()
        print("Payment inserted successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")