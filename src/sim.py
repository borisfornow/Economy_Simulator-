import auth
import init_db
import Users, Companies, Banks
from init_db import user_registry, company_registry

def sim():
    # 1. Initialize data structures
    init_db.init_database()

    print("*****************************************")
    print("Welcome to the Economy Simulator Program")
    print("*****************************************\n")

    # 2. Force a valid login
    current_user = None
    while not current_user:
        current_user = auth.auth_main()
        if not current_user:
            print("Login failed or cancelled. Please try again.")

    # 3. Game Loop
    running = True
    print(f"\nWelcome back, {current_user.name}. Type 'help' for commands.\n")
    
    while running:
        # World Tick: Death and Cleanup
        for user_id in list(user_registry.keys()): 
            user = user_registry[user_id]
    
            if user.death_check():
                # Remove from in-memory registry
                del user_registry[user_id]
        
                # Remove from JSON data store
                init_db.remove_user_from_data(user_id)

                # Remove from company's employee list if applicable
                if user.employed_by and user.employed_by in company_registry:
                    company_registry[user.employed_by].employees.remove(user_id)
                
                # Exit if the active player dies
                if user_id == current_user.id:
                    print("Game Over: Your character has died.")
                    return

        # User Input
        cmd = input(f"[{current_user.name.upper()}] $ ").lower().strip()

        if cmd in ["stop", "exit", "quit"]:
            print("Saving data and exiting...")
            running = False
        elif cmd == "help":
            print("\n--- Available Commands ---")
            print("status : Check your current user status and stats")
            print("help   : Show this menu")
            print("exit   : Close the program\n")
        elif cmd == "status":
            # Accessing stats directly from the object
            print(f"\n--- {current_user.name}'s Stats ---")
            print(f"Balance: {current_user.balance}")
            print(f"Health:  {current_user.health}")
            print(f"Energy:  {current_user.energy}")
            print(f"Luxury:  {current_user.luxury}")
            print(f"Job:     {current_user.employed_by}\n")
        else:
            print(f"Unknown command: '{cmd}'")

if __name__ == "__main__":
    sim()