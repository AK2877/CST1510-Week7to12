# Step 3:
import bcrypt
import os

# Step 6:
USER_DATA_FILE = "users.txt"
with open(USER_DATA_FILE, "w") as file:
    pass


# Step 4:
def hash_password(plain_text_password):
    # Hashes a password using bcrypt with automatic salt generation

    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    encode_pass = plain_text_password.encode("utf-8")

    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()

    # TODO: Hash the password using bcrypt.hashpw()
    hashed = bcrypt.hashpw(encode_pass, salt)

    # TODO: Decode the hash back to a string to store in a text file
    decode_pass = hashed.decode("utf-8")
    
    return decode_pass


# Step 5:
def verify_password(plain_text_password, hashed_password):
    # Verifies a plaintext password against a stored bcrypt hash
    
    # TODO: Encode both the plaintext password and the stored hash to bytes
    password_bytes = plain_text_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# Step 7:
def register_user(username, password):
    # Registers a new user by hashing the password and storing credentials
    
    # TODO: Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
        
    # TODO: Hash the password
    hashed = hash_password(password)

    # TODO: Append the new user to the file
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed}\n")  # Format: username,hashed_password

    print(f"Success: User '{username}' registered successfully!")
    return True


# Step 8:
def user_exists(username):
    # Checks if a username already exists in users database

    # TODO: Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False

    # TODO: Read the file and check each line for the username
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")
            if stored_username == username:
                return True

    return False


# Step 9:
def login_user(username, password):
    # Authenticates a user by verifying username and password

    # TODO: Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    # TODO: Search for the username in the file
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")

            if stored_username == username:
                
                # TODO: If username matches, verify the password
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    # TODO: If we reach here, the username was not found
    print("Error: Username not found.")
    return False


# Step 10:
def validate_username(username):
    # Validates username format

    if len(username) < 3:
        return (False, "Username must be at least 3 characters.")

    if len(username) > 20:
        return (False, "Username cannot exceed 20 characters.")

    # alphanumeric check without regex
    for char in username:
        if not (char.isalpha() or char.isdigit()):
            return (False, "Username may only contain letters and numbers.")

    return (True, "")


def validate_password(password):
    # Validates password strength

    if len(password) < 5:
        return (False, "Password must be at least 5 characters.")

    if len(password) > 20:
        return (False, "Password cannot exceed 20 characters.")

    # require at least 1 digit
    if not any(i.isdigit() for i in password):
        return (False, "Password must contain at least one number.")

    # require uppercase
    if not any(i.isupper() for i in password):
        return (False, "Password must contain at least one uppercase letter.")

    # require lowercase
    if not any(i.islower() for i in password):
        return (False, "Password must contain at least one lowercase letter.")

    return (True, "")


# Step 11:
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
                
            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
                
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
                
            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the data)")
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...") 
                    
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
                    
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")        


if __name__ == "__main__":
    main()
