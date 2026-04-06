import json
import os
import random

DATABASE_FILE = "auth.json"
JOB_PROBABILITY = 0.90
COMPANY_COUNT = 3  
CITIZEN_COUNT = 20
STARTING_VAULT = 5000

def create_initial_structure():
    """Returns the base dictionary with the admin user."""
    return {
        "users": {
            "0": {
                "name": "admin",
                "password": "password",
                "balance": 1000000,
                "is_admin": True,
                "job": None
            }
        },
        "companies": {},
        "bank": {
            "total_reserves": 500000,
            "interest_rate": 0.05
        }
    }

def populate_database(data):
    """Generates companies and citizens into the provided data dictionary."""
    
    # 1. Generate Companies
    user_ids = list(data["users"].keys()) # Initially ['0']
    for i in range(1, COMPANY_COUNT + 1):
        comp_id = f"CO-{i}"
        data["companies"][comp_id] = {
            "name": f"Enterprise_{comp_id}",
            "owner": random.choice(user_ids),
            "vault": STARTING_VAULT,
            "employees": [],
            "salary": random.randint(40, 80)
        }

    # 2. Generate Citizens
    company_ids = list(data["companies"].keys())
    for i in range(1, CITIZEN_COUNT + 1):
        user_id = str(i) # IDs 1, 2, 3...
        has_job = random.random() < JOB_PROBABILITY
        assigned_job_id = random.choice(company_ids) if (has_job and company_ids) else None

        data["users"][user_id] = {
            "name": f"citizen_{user_id}",
            "password": "password",
            "balance": 100,
            "is_admin": False,
            "job": assigned_job_id
        }

        if assigned_job_id:
            data["companies"][assigned_job_id]["employees"].append(user_id)
    
    return data

def update_data(target_id, **kwargs):
    """Updates a specific user's data or creates a new entry if the ID doesn't exist."""
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
            
        # If the user (ID) doesn't exist, initialize their dictionary
        if target_id not in data["users"]:
            data["users"][target_id] = {}

        # Update the fields provided in kwargs (name, password, balance, etc.)
        for key, value in kwargs.items():
            data["users"][target_id][key] = value
            
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
            
    except Exception as e:
        print(f"Error updating database: {e}")

def add_employee_to_company(company_id, user_id):
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
        
        if company_id in data["companies"]:
            if user_id not in data["companies"][company_id]["employees"]:
                data["companies"][company_id]["employees"].append(user_id)
        
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error linking employee: {e}")

def init_database():
    """Only creates and populates the database if the file does not exist."""
    if not os.path.exists(DATABASE_FILE):
        print("No database found. Initializing and generating population...")
        
        # Start with the base structure
        data = create_initial_structure()
        
        # Fill it with the requested number of citizens and companies
        data = populate_database(data)
        
        try:
            with open(DATABASE_FILE, 'w') as file:
                json.dump(data, file, indent=4)
                print(f"Database created with {CITIZEN_COUNT} citizens and {COMPANY_COUNT} companies.")
        except Exception as e:
            print(f"An error occurred during file creation: {e}")
    else:
        
        print("Database already exists. Loading existing data...")

if __name__ == "__main__":
    init_database()