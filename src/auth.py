import sys
import json
import os
import bcrypt
import init_db

DATABASE_FILE = "auth.json"

def hash_pw(pw):
    """Converts a plain-text password into a secure, salted hash."""
    pw_bytes = pw.encode('utf-8')
    # gensalt() handles the complexity of making the hash unique
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(pw_bytes, s)
    return h.decode('utf-8')

def load_data():
    """Reads the database file and returns a dictionary."""
    try:
        if not os.path.exists(DATABASE_FILE):
            # If the file is missing, trigger the initializer
            init_db.init_database()
            
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error: {DATABASE_FILE} is missing or corrupted.")
        sys.exit(1)

def login_auth(data):
    """Handles the login process with a maximum of 3 attempts."""
    login_attempts = 0
    max_attempts = 3
    print("\n*******************")
    print("      LogIn !      ")
    print("*******************")

    while login_attempts < max_attempts:
        username = input("Username: ").strip()
        pw = input("Password : ").strip()
        
        user_info = data.get("users", {}).get(username)

        if not user_info:
            print("----------------------------------------")
            print("This User does not exist")
            print("----------------------------------------")
            login_attempts += 1
            continue

        # Verify the provided password against the stored hash
        # 
        stored_hash = user_info.get("password", "")
        if bcrypt.checkpw(pw.encode('utf-8'), stored_hash.encode('utf-8')):
            print("**************************")
            print(f"Logged in to {username}")
            print("**************************")
            return username 
        else: 
            login_attempts += 1
            remaining = max_attempts - login_attempts
            print("----------------------------------------")
            print("Wrong password.")
            if remaining > 0:
                print(f"You have {remaining} attempts left")
            print("----------------------------------------")

    print("************************************************")
    print("Locked out: Too many failed attempts.")
    print("************************************************")
    sys.exit(0)

def signup_auth():
    """Handles user registration and returns the validated credentials."""
    print("\n*******************")
    print("      Sign-up      ")
    print("*******************")

    data = load_data()
    user_info = data.get("users", {})
    
    final_username = ""
    final_pw = ""

    # Username Validation Loop
    while True:
        temp_username = input("Choose a username: ").strip()
        if temp_username in user_info:
            print("(!) This user is already taken.")
        elif len(temp_username) < 5:
            print("(!) Username must be at least 5 characters.")
        else:
            final_username = temp_username
            break

    # Password Validation Loop
    while True:
        temp_pw = input("Choose a password: ").strip()
        if len(temp_pw) < 5:
            print("(!) Password must be at least 5 characters.")
        else:
            final_pw = temp_pw
            break

    return final_username, final_pw

def auth_main():
    """Main entry point for authentication logic."""
    while True:
        # Always reload data to ensure we have the latest users
        data = load_data()
        
        print("\n--- Economy Simulator ---")
        print("1. Log In")
        print("2. Sign Up")
        print("-------------------------")
        result = input("# ")

        if result == "1":
            return login_auth(data)

        elif result == "2":
            # 1. Get validated inputs
            new_user, new_pw = signup_auth()
            
            # 2. Secure the password before it touches the database
            # 
            hashed_pw = hash_pw(new_pw)
            
            # 3. Save to database using the standard 'password' key
            init_db.update_data(new_user, password=hashed_pw)

            print(f"***************************************")
            print(f"\nAccount created! Welcome, {new_user}.")
            print(f"***************************************")
            return new_user

        else:
            print("Invalid Input. Please enter 1 or 2.")

if __name__ == "__main__":
    auth_main()