import json 
import os

DATABASE_FILE = "auth.json"



def create_data():

    # 1. Define the dictionary inside the function
    data_dict = {
        "users": {
        "admin": {
            "password": "password",
            "balance": 1000000,
            "is_admin": True,
            "job": None
        },
        "citizen_one": {
            "password": "password",
            "balance": 100,
            "is_admin": False,
            "job": "TechCorp"
        }
        },
        "companies": {
        "TechCorp": {
            "owner": "admin",
            "vault": 5000,
            "employees": ["citizen_one"],
            "salary": 50
        }
        },
        "bank": {
        "total_reserves": 500000,
        "interest_rate": 0.05
        }
}

    # 2. Check if the file exists
    if not os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'w') as file:
                # 3. Convert to string and write inside the same block
                json.dump(data_dict, file, indent=4)
                print(f"File '{DATABASE_FILE}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Database populated already.")

def update_data(target_user, **kwargs):
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 1. If user doesn't exist, create a blank template for them FIRST
    if target_user not in data["users"]:
        print(f"Creating new profile for {target_user}...")
        data["users"][target_user] = {
            "password": "default_password", 
            "balance": 100,
            "is_admin": False,
            "job": None
        }

    # 2. Now that the user definitely exists, update their fields
    for key, value in kwargs.items():
        if key in data["users"][target_user]:
            data["users"][target_user][key] = value
            print(f"Updated {key} for {target_user}")
        else:
            print(f"Warning: {key} is not a valid field for {target_user}")

    # 3. Save to file
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)
    
def get_data_dict(current_user):
    
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"*************************************************")
    print(f"User: {current_user} | Status: Online")
    print(f"Balance: {data["users"][current_user]["balance"]}")
    print(f"Job: {data["users"][current_user]["job"]}")
    print(f"*************************************************")

def init_database():
    create_data()

if __name__ == "__main__":
    init_database()