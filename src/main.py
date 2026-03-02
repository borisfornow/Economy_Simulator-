import sys
import auth
import init_db

def main():
    # 1. Ensure the environment is ready
    init_db.init_database()

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
        # Using a distinct prompt style
        cmd = input(f"[{current_user.upper()}] $ ").lower().strip()

        if cmd in ["stop", "exit", "quit"]:
            print("Saving data and exiting...")
            running = False
        elif cmd == "help":
            print("\n--- Available Commands ---")
            print("status : Check your current balance and job")
            print("help   : Show this menu")
            print("exit   : Close the program\n")
        elif cmd == "status":
            init_db.get_data_dict(current_user)
        else:
            print(f"Unknown command: '{cmd}'")

if __name__ == "__main__":
    main()