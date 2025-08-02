"""
Database connection and setup utilities
"""

import mysql.connector
from config import DB_CONFIG

def connect_db():
    """Create and return a database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query with optional parameters
    
    Args:
        query (str): SQL query to execute
        params (tuple): Parameters for the query
        fetch_one (bool): Whether to fetch one result
        fetch_all (bool): Whether to fetch all results
        
    Returns:
        Query result or None
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
            
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()