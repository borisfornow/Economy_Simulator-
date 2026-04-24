import sys
import bcrypt
import random
import init_db
from init_db import user_registry

JOB_PROBABILITY = 0.90

def hash_pw(pw):
    """Hashes a password using bcrypt."""
    pw_bytes = pw.encode('utf-8')
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(pw_bytes, s)
    return h.decode('utf-8')

def load_data():
    """Returns the current database state from init_db."""
    init_db.init_database()
    return init_db.load_database()

def login_auth(data):
    """Handles login and returns the corresponding User object from RAM."""
    login_attempts = 0
    max_attempts = 3
    print("\n*******************")
    print("      LogIn !      ")
    print("*******************")

    while login_attempts < max_attempts:
        username_input = input("Username: ").strip()
        pw_input = input("Password : ").strip()
        
        target_id = None
        user_info = None

        # Search for user in the JSON data by the 'name' field
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
        
        # Verify password (handles bcrypt or plain-text fallback)
        is_valid = False
        try:
            is_valid = bcrypt.checkpw(pw_input.encode('utf-8'), stored_hash.encode('utf-8'))
        except (ValueError, AttributeError):
            is_valid = (pw_input == stored_hash)

        if is_valid:
            print("**************************")
            print(f"Logged in as {username_input} (ID: {target_id})")
            print("**************************")
            
            # Retrieve the object from RAM registry
            return user_registry.get(target_id) 
        else: 
            login_attempts += 1
            remaining = max_attempts - login_attempts
            print(f"Wrong password. {remaining} attempts left.")

    print("Locked out: Too many failed attempts.")
    sys.exit(0)

def signup_auth():
    """Prompts for new user credentials and validates availability."""
    print("\n*******************")
    print("      Sign-up      ")
    print("*******************")

    data = load_data()
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
    """Main entry point for authentication logic. Returns a User Object."""
    # Ensure database is loaded into RAM before we do anything
    init_db.init_database()
    
    while True:
        # Reload fresh data from disk for each loop iteration
        data = load_data()
        
        print("\n--- Economy Simulator ---")
        print("1. Log In")
        print("2. Sign Up")
        print("-------------------------")
        choice = input("# ")

        if choice == "1":
            user_obj = login_auth(data)
            if user_obj:
                return user_obj

        elif choice == "2":
            new_name, new_pw = signup_auth()
            hashed_pw = hash_pw(new_pw)
            
            # Generate new ID
            existing_ids = [int(k) for k in data["users"].keys() if k.isdigit()]
            new_id = str(max(existing_ids) + 1 if existing_ids else 1)

            # Random Job Assignment
            company_ids = list(data.get("companies", {}).keys())
            has_job = random.random() < JOB_PROBABILITY
            assigned_job_id = random.choice(company_ids) if (has_job and company_ids) else None

            # 1. Update JSON and RAM (init_db.update_data must sync user_registry)
            init_db.update_data(
                new_id, 
                name=new_name, 
                password=hashed_pw, 
                balance=100, 
                is_admin=False, 
                employed_by=assigned_job_id,
                health=100,
                energy=10,
                luxury=5
            )

            # 2. Handle company linkage
            if assigned_job_id:
                init_db.add_employee_to_company(assigned_job_id, new_id)

            # 3. Retrieve the newly created object from the registry
            new_user_obj = user_registry.get(new_id)
            
            if new_user_obj:
                print(f"\nAccount created! Welcome, {new_name}.")
                return new_user_obj
            else:
                print("(!) Error: Registry sync failed. Please try logging in.")

        else:
            print("Invalid Input. Please enter 1 or 2.")

if __name__ == "__main__":
    auth_main()