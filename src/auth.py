import sys
import json
import os
import bcrypt
import random
import init_db

DATABASE_FILE = "auth.json"
JOB_PROBABILITY = 0.90  

def hash_pw(pw):
    
    pw_bytes = pw.encode('utf-8')
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(pw_bytes, s)
    return h.decode('utf-8')

def load_data():
    """Reads the database file and returns a dictionary."""
    if not os.path.exists(DATABASE_FILE):
        # Trigger the one-time generation logic from init_db
        init_db.init_database()
            
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error: {DATABASE_FILE} is missing or corrupted.")
        sys.exit(1)

def login_auth(data):
    """Handles login by searching for the username inside the user objects."""
    login_attempts = 0
    max_attempts = 3
    print("\n*******************")
    print("      LogIn !      ")
    print("*******************")

    while login_attempts < max_attempts:
        username_input = input("Username: ").strip()
        pw_input = input("Password : ").strip()
        
        # Since keys are IDs, search for the user by their 'name' attribute
        target_id = None
        user_info = None

        for uid, info in data.get("users", {}).items():
            if info.get("name") == username_input:
                target_id = uid
                user_info = info
                break

        if not user_info:
            print("----------------------------------------")
            print("This User does not exist")
            print("----------------------------------------")
            login_attempts += 1
            continue

        stored_hash = user_info.get("password", "")
        
        # Verify password
        is_valid = False
        try:
            # Check if it's a bcrypt hash
            is_valid = bcrypt.checkpw(pw_input.encode('utf-8'), stored_hash.encode('utf-8'))
        except (ValueError, AttributeError):
            # Fallback for plain-text (useful for the initial 'admin' setup)
            is_valid = (pw_input == stored_hash)

        if is_valid:
            print("**************************")
            print(f"Logged in as {username_input} (ID: {target_id})")
            print("**************************")
            return username_input 
        else: 
            login_attempts += 1
            remaining = max_attempts - login_attempts
            print(f"Wrong password. {remaining} attempts left.")

    print("Locked out: Too many failed attempts.")
    sys.exit(0)

def signup_auth():

    print("\n*******************")
    print("      Sign-up      ")
    print("*******************")

    data = load_data()
    # Extract all existing names to prevent duplicates
    existing_names = [info.get("name") for info in data.get("users", {}).values()]
    
    while True:
        new_name = input("Choose a username: ").strip()
        if new_name in existing_names:
            print("(!) This name is already taken.")
        elif len(new_name) < 5:
            print("(!) Username must be at least 5 characters.")
        else:
            break

    while True:
        new_pw = input("Choose a password: ").strip()
        if len(new_pw) < 5:
            print("(!) Password must be at least 5 characters.")
        else:
            break

    return new_name, new_pw

def auth_main():
    """Main entry point for authentication logic."""
    while True:
        data = load_data()
        
        print("\n--- Economy Simulator ---")
        print("1. Log In")
        print("2. Sign Up")
        print("-------------------------")
        choice = input("# ")

        if choice == "1":
            return login_auth(data)

        elif choice == "2":
            new_name, new_pw = signup_auth()
            hashed_pw = hash_pw(new_pw)
            
            # 1. Generate a new unique ID
            existing_ids = [int(k) for k in data["users"].keys() if k.isdigit()]
            new_id = str(max(existing_ids) + 1 if existing_ids else 1)

            # 2. Random Job Assignment
            company_ids = list(data.get("companies", {}).keys())
            has_job = random.random() < JOB_PROBABILITY
            assigned_job_id = random.choice(company_ids) if (has_job and company_ids) else None

            # 3. Save the new user via init_db
            init_db.update_data(
                new_id, 
                name=new_name, 
                password=hashed_pw, 
                balance=100, 
                is_admin=False, 
                job=assigned_job_id
            )

            # 4. Link the employee to the company if applicable
            if assigned_job_id:
                init_db.add_employee_to_company(assigned_job_id, new_id)

            status = f"employed at {assigned_job_id}" if assigned_job_id else "unemployed"
            print(f"\nAccount created! Welcome, {new_name}. Your ID is {new_id} ({status}).")
            return new_name

        else:
            print("Invalid Input. Please enter 1 or 2.")

if __name__ == "__main__":
    auth_main()