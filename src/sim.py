import sys
import auth
import init_db
import Users, Companies, Banks
from init_db import user_registry, company_registry, bank_registry

def sim():
    print("*****************************************")
    print("Welcome to the Economy Simulator Program")
    print("*****************************************\n")

    # 2. Force a valid login before entering the game loop
    current_user = None
    while not current_user:
        current_user = auth.auth_main()
        if not current_user:
            print("Login failed or cancelled. Please try again.")

    # 3. Game Loop
    running = True
    print(f"\nWelcome back, {current_user}. Type 'help' for commands.\n")
    
    while running:

        for user_id in list(user_registry.keys()): 
            user = user_registry[user_id]
    
            # Run the check
            if user.death_check():
                # 1. Remove from the in-memory registry
                del user_registry[user_id]
        
                # 2. Remove from the JSON data store
                init_db.remove_user_from_data(user_id)

                # 3. Remove from their company's employee list
                if user.employed_by:
                    company_registry[user.employed_by].employees.remove(user_id)

        # Using a distinct prompt style
        cmd = input(f"[{current_user.upper()}] $ ").lower().strip()

        if cmd in ["stop", "exit", "quit"]:
            print("Saving data and exiting...")
            running = False
        elif cmd == "help":
            print("\n--- Available Commands ---")
            print("status : Check your current user status and stats")
            print("help   : Show this menu")
            print("exit   : Close the program\n")
        elif cmd == "status":
            init_db.get_data_dict(current_user)
        else:
            print(f"Unknown command: '{cmd}'")