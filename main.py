import sys
import json

running = True

with open("auth.json", "r") as file:
    data = json.load(file)


def login_auth():
    logged_in = False
    login_attempts = 0

    while not logged_in:
        
        username = input("Username: ")
        password = input("Password : ")

        if login_attempts >= 2:
            print("************************************************")
            print("You've been locked out (over 3 attempted logins)")
            print("************************************************")
            sys.exit(0)
        
        elif password != "password":
            print("****************************************")
            print("Either wrong useranme or wrong password")
            print("You have", {2-login_attempts},"attempts left")
            print("****************************************")
            login_attempts += 1
            continue

        elif username == "admin" and password == "password":
            print("**************************")
            print("Logged in to " , {username})
            print("**************************")
            logged_in = True
            break




def main():

    print("***************************************")
    print("Wecome to the Econmony Simultor Program")
    print("***************************************\n")

    login_auth()


    while running:
            
        instruction = input("# ")

        if instruction == "stop":
            break
        else:
            continue



if __name__ == "__main__":
    main()