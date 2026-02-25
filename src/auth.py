import sys
import json
import os
import bcrypt

DATABASE_FILE = "src/auth.json"

def hash_password(pw):
    pw_bytes = pw.encode('utf-8')
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(pw_bytes, s)
    return h.decode('utf-8')

def load_data():
    if not os.path.exists(DATABASE_FILE):
        # Create a default structure if file is missing
        return {"users": {}}
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: {DATABASE_FILE} is corrupted.")
        sys.exit(1)

def login_auth(data):
    login_attempts = 0
    max_attempts = 3
    print("*******\nLogIn !\n*******")

    while login_attempts < max_attempts:
        username = input("Username: ").strip()
        password = input("Password : ").strip()
        
        user_info = data.get("users", {}).get(username)

        if not user_info:
            print("****************************************")
            print("This User does not exist")
            print("****************************************")
            login_attempts += 1
        # Corrected bcrypt verification logic
        # bcrypt.checkpw(password.encode('utf-8'), user_info["password"].encode('utf-8'))
        
        elif user_info["password"] == password:
            print("**************************")
            print(f"Logged in to {username}")
            print("**************************")
            return username 
        else: 
            login_attempts += 1
            remaining = max_attempts - login_attempts
            print("****************************************")
            print("Either wrong username or wrong password")
            if remaining > 0:
                print(f"You have {remaining} attempts left")
            print("****************************************")

    print("************************************************")
    print("You've been locked out (over 3 attempted logins)")
    print("************************************************")
    sys.exit(0)

def signup_auth():
    print("*******\nSign-up\n*******")

    data = load_data()
    # Safety: Default to empty dict if "users" doesn't exist
    user_info = data.get("users", {})
    
    final_username = ""
    final_password = ""

    # Username Loop
    usr_running = True
    while usr_running:
        print("***********************************")
        temp_username = input("Enter the username you would like: ").strip()
        print("***********************************")
        if temp_username in user_info:
            print("This user is already taken")
        elif len(temp_username) < 5:
            print("Username must be at least 5 chr")
        else:
            print("Your username is set")
            final_username = temp_username
            usr_running = False

    # Password Loop
    pass_running = True
    while pass_running:
        print("***********************************")
        temp_password = input("Enter the password you would like: ").strip()
        print("***********************************")
        if len(temp_password) < 5:
            print("Password must be at least 5 chr")
        else:
            print("Your password is set")
            final_password = temp_password
            pass_running = False

    # Return the values so auth_main can use them
    return final_username, final_password

def auth_main():
    while True:
        data = load_data()
        print("*******************")
        print("To LogIn enter     :1")
        print("To Sign Up enter   :2")
        print("*******************")
        result = input("# ")

        if result == "1":
            current_user = login_auth(data)
            return current_user # Pass the logged in user back to the caller

        elif result == "2":
            # Capture the returned values from signup
            new_user, new_pass = signup_auth()
            
            # NOTE: Still need a function here to hash new_pass 
            # and save it to the JSON before calling login_auth.
            
            # Refresh data after signup and log in
            data = load_data()
            current_user = login_auth(data)
            return current_user

        else:
            print("Invalid Input, choose between option 1 or 2")

if __name__ == "__main__":
    auth_main()