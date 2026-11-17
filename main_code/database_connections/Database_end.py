# Inside Database_end.py (or wherever end_connection is defined)
from main_code.database_connections.database_connect import cursor, conn

def end_connection(query, values):
    cursor.execute(query, values)
    conn.commit()
    
    # Grab the lastrowid before closing the cursor/connection
    last_id = cursor.lastrowid 
    
    # Close your cursor and connection here if your project handles cleanup in this function:
    # cursor.close()
    # conn.close()
    
    return last_id