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
        print("Thank you for using our appliacation")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

def end_connect(conn_obj, cursor_obj, query, values):
    try:
        cursor_obj.execute(query, values)
        conn_obj.commit()
        print("Query executed successfully!")
    except Exception as e:
        conn_obj.rollback()
        print(f"Error: {e}")
    # Note: Be careful closing the connection here if you plan to run 
    # more database queries later in the same script session, 
    # as it will shut down the connection permanently.