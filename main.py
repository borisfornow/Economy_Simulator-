import sys
import json
import os

# Use a constant for the filename to avoid typos
DATABASE_FILE = "auth.json"

def load_data():
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: {DATABASE_FILE} is corrupted.")
        sys.exit(1)

def login_auth(data):
    login_attempts = 0
    max_attempts = 3

    while login_attempts < max_attempts:
        username = input("Username: ").strip()
        password = input("Password : ").strip()
        
        user_info = data.get("users", {}).get(username)

        if not user_info:
            print("****************************************")
            print("This User does not exist")
            print("****************************************")
            login_attempts += 1
        elif user_info["password"] == password:
            print("**************************")
            print(f"Logged in to {username}")
            print("**************************")
            return username  # Return the logged-in user for use in main
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

def main():
    data = load_data()

    print("***************************************")
    print("Welcome to the Economy Simulator Program")
    print("***************************************\n")

    # Capture the username so the rest of the program knows who is playing
    current_user = login_auth(data)

    running = True
    while running:
        instruction = input(f"[{current_user}] # ").lower().strip()

        if instruction == "stop" or instruction == "exit":
            running = False
        elif instruction == "help":
            print("Available commands: stop, exit, help")

if __name__ == "__main__":
    main()