import sys
import json
import os
import bcrypt
import auth



def main():

    print("***************************************")
    print("Welcome to the Economy Simulator Program")
    print("***************************************\n")

    # Capture the username so the rest of the program knows who is playing
    current_user = auth.auth_main()

    running = True
    while running:
        instruction = input(f"[{current_user}] $ ").lower().strip()

        if instruction == "stop" or instruction == "exit":
            running = False
        elif instruction == "help":
            print("Available commands: stop, exit, help")

if __name__ == "__main__":
    main()