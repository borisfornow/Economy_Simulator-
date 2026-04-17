import json
import os
import random
import Users, Companies, Banks

DATABASE_FILE = "database.json"
JOB_PROBABILITY = 0.90
COMPANY_COUNT = 3  
CITIZEN_COUNT = 20
STARTING_CAPITAL = 50000

# Global registries for quick in-memory access
user_registry = {}
company_registry = {}
product_registry = {} 

def create_initial_structure():
    """Returns the base dictionary with the admin user."""
    return {
        "users": {
            "0": {
                "name": "admin",
                "password": "password",
                "balance": 10000000,
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
        data["companies"][comp_id] = vars(company)

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
            "balance": user.balance,
            "is_admin": user.is_admin,
            "employed_by": user.employed_by,
            "health": user.health,
            "energy": user.energy,
            "luxury": user.luxury
        }

        if user.employed_by:
            company_data = data["companies"][user.employed_by]
            if user.id not in company_data["employees"]:
                company_data["employees"].append(user.id)
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
    """Updates JSON and ensures the in-memory registry is synced."""
    global user_registry
    try:
        data = {}
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "r") as file:
                data = json.load(file)
        
        if "users" not in data: data["users"] = {}
        if target_id not in data["users"]: data["users"][target_id] = {}

        for key, value in kwargs.items():
            data["users"][target_id][key] = value
            
        save_to_disk(data)
        
        # Syncing RAM
        u = data["users"][target_id]
        user_registry[target_id] = Users.User(
            id=target_id,
            name=u.get("name"),
            password=u.get("password"),
            balance=u.get("balance"),
            is_admin=u.get("is_admin", False),
            employed_by=u.get("employed_by")
        )
    except Exception as e:
        print(f"Error updating database: {e}")

def remove_user_from_data(user_id):
    """Removes a user from memory and disk."""
    global user_registry
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
        
        if user_id in data["users"]:
            emp_by = data["users"][user_id].get("employed_by")
            if emp_by and emp_by in data["companies"]:
                data["companies"][emp_by]["employees"].remove(user_id)
            
            del data["users"][user_id]
            if user_id in user_registry: del user_registry[user_id]
            save_to_disk(data)
    except Exception as e:
        print(f"Removal error: {e}")

def add_employee_to_company(company_id, user_id):
    """Adds an employee to a company in both RAM and JSON."""
    global company_registry
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
        
        if company_id in data["companies"] and user_id in data["users"]:
            if user_id not in data["companies"][company_id]["employees"]:
                data["companies"][company_id]["employees"].append(user_id)
            if user_id not in company_registry[company_id].employees:
                company_registry[company_id].employees.append(user_id)
            save_to_disk(data)
    except Exception as e:
        print(f"Error adding employee: {e}")

def init_database():
    """Initializes and loads the database registries."""
    global user_registry, company_registry, product_registry

    if not os.path.exists(DATABASE_FILE):
        print("Initializing database...")
        data = populate_database(create_initial_structure())
        save_to_disk(data)

    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
            
            # 1. Populate Users
            for uid, info in data.get("users", {}).items():
                user_registry[uid] = Users.User(
                    uid, info["name"], info["password"], 
                    info["balance"], info["is_admin"], info["employed_by"]
                )
            
            # 2. Populate Companies
            for cid, info in data.get("companies", {}).items():
                company_registry[cid] = Companies.Company(
                    info["name"], info["owner"], info["vault"], 
                    info["employees"], info["salary"], info["commodity"], 
                    info["production_rate"]
                )

            # 3. Populate Products based on Company Commodities
            # We clear it first to avoid duplicates on refresh
            product_registry.clear()
            for cid, company in company_registry.items():
                # We use the commodity name as the key
                
                product_registry[company.commodity] = {
                    "name": company.commodity.capitalize(),
                    "producer": company.name,
                    "price": 50  # Default price for now 
                }

        print("✔ Registries synced with Company commodities.")

    except Exception as e:
        print(f"Registry load error: {e}")

if __name__ == "__main__":
    init_database()