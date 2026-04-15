import json
import os
import random
import Users, Companies, Banks

DATABASE_FILE = "auth.json"
JOB_PROBABILITY = 0.90
COMPANY_COUNT = 3  
CITIZEN_COUNT = 20
STARTING_CAPITAL = 50000

# Global registries for quick in-memory access
user_registry = {}
company_registry = {}

def create_initial_structure():
    """Returns the base dictionary with the admin user."""
    return {
        "users": {
            "0": {
                "name": "admin",
                "password": "password",
                "balance": 10000000, # Keep as int for math
                "is_admin": True,
                "employed_by": None,
                "health": 100,
                "energy": 10,
                "luxury": 5
            }
        },
        "companies": {},
        "bank": {
            "total_reserves": 5000000,
            "interest_rate": 0.05
        }
    }

def populate_database(data):
    """Generates companies and citizens into the provided dictionary and memory."""
    global user_registry, company_registry
    
    product_list = ["health", "energy", "luxury"]
    user_ids = list(data["users"].keys()) 

    # 1. Generate Companies
    for i in range(1, COMPANY_COUNT + 1):
        comp_id = f"CO-{i}"
        commodity = random.choice(product_list) if product_list else "general"
        if product_list: product_list.remove(commodity)

        company = Companies.Company(
            name=f"Enterprise_{comp_id}",
            owner=random.choice(user_ids),
            vault=STARTING_CAPITAL,
            employees=[],
            salary=random.randint(40, 80),
            commodity=commodity,
            production_rate=random.randint(1, 5)
        )
        
        company_registry[comp_id] = company
        data["companies"][comp_id] = vars(company) # vars() converts object to dict

    # 2. Generate Citizens
    company_ids = list(data["companies"].keys())
    for i in range(1, CITIZEN_COUNT + 1):
        target_id = str(i)
        has_job = random.random() < JOB_PROBABILITY
        assigned_job_id = random.choice(company_ids) if (has_job and company_ids) else None
        
        user = Users.User(
            id=target_id, 
            name=f"citizen_{target_id}", 
            password="password", 
            balance=random.randint(50, 100), 
            is_admin=False, 
            employed_by=assigned_job_id
        )
        
        user_registry[target_id] = user
        data["users"][target_id] = {
            "name": user.name,
            "password": user.password,
            "balance": user.balance, # Stored as int
            "is_admin": user.is_admin,
            "employed_by": user.employed_by,
            "health": user.health,
            "energy": user.energy,
            "luxury": user.luxury
        }

        if user.employed_by:
            company_data = data["companies"][user.employed_by]
            # Check JSON structure
            if user.id not in company_data["employees"]:
                company_data["employees"].append(user.id)
            
            # Check in-memory object
            if user.id not in company_registry[user.employed_by].employees:
                company_registry[user.employed_by].employees.append(user.id)
            
    return data

def save_to_disk(data):
    """Helper to write the current data state to JSON."""
    try:
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Save error: {e}")

def update_data(target_id, **kwargs):
    """Updates a user's data in JSON and syncs the in-memory object."""
    global user_registry
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
            
        if target_id in data["users"]:
            for key, value in kwargs.items():
                data["users"][target_id][key] = value
            
            save_to_disk(data)
            
            # Re-sync object
            u = data["users"][target_id]
            user_registry[target_id] = Entities.Users(
                target_id, u['name'], u['password'], u['balance'], 
                u['is_admin'], u['employed_by']
            )
    except Exception as e:
        print(f"Update error: {e}")

def remove_user_from_data(user_id):
    """Removes a user from memory and disk."""
    global user_registry
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
        
        if user_id in data["users"]:
            # Remove from company list first
            emp_by = data["users"][user_id].get("employed_by")
            if emp_by and emp_by in data["companies"]:
                data["companies"][emp_by]["employees"].remove(user_id)
            
            del data["users"][user_id]
            if user_id in user_registry: del user_registry[user_id]
            
            save_to_disk(data)
    except Exception as e:
        print(f"Removal error: {e}")

def init_database():
    """Initializes or loads the database."""
    global user_registry, company_registry

    if not os.path.exists(DATABASE_FILE):
        data = populate_database(create_initial_structure())
        save_to_disk(data)
    else:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
            for uid, info in data["users"].items():
                user_registry[uid] = Users.User(
                    uid, info["name"], info["password"], 
                    info["balance"], info["is_admin"], info["employed_by"]
                )
            for cid, info in data["companies"].items():
                company_registry[cid] = Companies.Company(
                    info["name"], info["owner"], info["vault"], 
                    info["employees"], info["salary"], info["commodity"], 
                    info["production_rate"]
                )

if __name__ == "__main__":
    init_database()