"""
From Week 8 - Polished
"""

# Import the database connection function
from app.data.db import connect_database

def get_user_by_username(username):
    """
    Get a user from the database by their username.
    
    Args:
        username (str): The username to search for
    
    Returns:
        tuple: User data as a tuple (id, username, password_hash, role)
        None: If user not found
    """
    
    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)  # comma makes it a tuple
    )
    
    user = cursor.fetchone()
    
    # Close the database connection
    conn.close()
    
    return user

def insert_user(username, password_hash, role='user'):
    """
    Insert a new user into the database.
    
    Args:
        username (str): The username
        password_hash (str): The hashed password
        role (str): User role, defaults to 'user'
    
    Returns:
        int: The ID of the newly inserted user
    """
    
    conn = connect_database()
    cursor = conn.cursor()
    
    # Insert the new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    
    # Get the ID of the newly inserted user
    new_user_id = cursor.lastrowid
    
    # Save changes to database
    conn.commit()
    
    conn.close()
    
    return new_user_id

def get_all_users():
    """
    Get all users from the database.
    
    Returns:
        list: List of all users as tuples
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    conn.close()
    return users