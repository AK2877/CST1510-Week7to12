"""
From week 7 - Polished 
"""

import bcrypt
from app.data.users import get_user_by_username, insert_user

def hash_password(password):

    """Hash a password using bcrypt for secure storage"""
    
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # Convert back to string for storage
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):

    """Verify if a password matches the stored hash"""
    
    try:
        # Convert both to bytes for comparison
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Use bcrypt to check if password matches hash
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except:
        # If anything goes wrong return False
        return False

def register_user(username, password, role='user'):

    """Register a new user to the system"""
    
    # Check if user already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return False, "Username already exists"
    
    # Hash the password
    password_hash = hash_password(password)
    
    # Insert user into database
    try:
        insert_user(username, password_hash, role)
        return True, "User registered successfully"
    except Exception as e:
        return False, f"Error registering user: {str(e)}"

def authenticate_user(username, password):

    """Authenticate a user by checking username and password"""
    
    # Get user from database
    user = get_user_by_username(username)
    
    # Check if user exists
    if not user:
        return False, None
    
    # Creating a user tuple with format: (id, username, password_hash, role)
    user_id, db_username, stored_hash, user_role = user
    
    # Verify the password
    if verify_password(password, stored_hash):
        # Return user information if authentication successful
        user_info = {
            'id': user_id,
            'username': db_username,
            'role': user_role
        }
        return True, user_info
    
    # Return False if password doesn't match
    return False, None

def validate_username(username):

    """Check if a username is valid"""
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 20:
        return False, "Username cannot exceed 20 characters"
    
    if not username.isalnum():
        return False, "Username may only contain letters and numbers"
    
    return True, ""

def validate_password(password):

    """Check if a password is secure"""
    
    if len(password) < 5:
        return False, "Password must be at least 5 characters"
    
    if len(password) > 50:
        return False, "Password cannot exceed 50 characters"
    
    has_number = any(char.isdigit() for char in password)
    if not has_number:
        return False, "Password must contain at least one number"
    
    has_upper = any(char.isupper() for char in password)
    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    
    has_lower = any(char.islower() for char in password)
    if not has_lower:
        return False, "Password must contain at least one lowercase letter"
    
    return True, ""