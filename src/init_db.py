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

def init_database():
    create_data()

if __name__ == "__main__":
    init_database()