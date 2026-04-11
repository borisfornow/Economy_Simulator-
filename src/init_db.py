import json
import os
import random
import Entities
from Entities import Users, Companies, Banks

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
                "balance": 10000000,
                "is_admin": True,
                "employed_by": None
            }
        },
        "companies": {},
        "bank": {
            "total_reserves": 5000000,
            "interest_rate": 0.05
        }
    }

def populate_database(data):
    """Generates companies and citizens into the provided data dictionary and memory."""
    global user_registry, company_registry
    
    product_list = ["health", "energy", "luxury"]
    user_ids = list(data["users"].keys()) 

    # 1. Generate Companies
    for i in range(1, COMPANY_COUNT + 1):
        comp_id = f"CO-{i}"
        
        # Ensure we don't crash if product_list is empty
        company_commodity = random.choice(product_list) if product_list else "general"
        if product_list: product_list.remove(company_commodity)

        company = Entities.Companies(
            name=f"Enterprise_{comp_id}",
            owner=random.choice(user_ids),
            vault=STARTING_CAPITAL,
            employees=[],
            salary=random.randint(40, 80),
            commodity=company_commodity,
            production_rate=random.randint(1, 5)
        )
        
        company_registry[comp_id] = company
        data["companies"][comp_id] = {
            "name": company.name,
            "owner": company.owner,
            "vault": company.vault,
            "employees": company.employees,
            "salary": company.salary,
            "commodity": company.commodity,
            "production_rate": company.production_rate
        }

    # 2. Generate Citizens
    company_ids = list(data["companies"].keys())
    for i in range(1, CITIZEN_COUNT + 1):
        target_id = str(i)
        has_job = random.random() < JOB_PROBABILITY
        assigned_job_id = random.choice(company_ids) if (has_job and company_ids) else None
        
        user = Entities.Users(
            id=target_id, 
            name=f"citizen_{target_id}", 
            password="password", 
            balance=100, 
            is_admin=False, 
            employed_by=assigned_job_id
        )
        
        user_registry[target_id] = user
        data["users"][target_id] = {
            "name": user.name,
            "password": user.password,
            "balance": user.balance,
            "is_admin": user.is_admin,
            "employed_by": user.employed_by
        }

        # Link employee to company in the JSON structure
        if user.employed_by:
            data["companies"][user.employed_by]["employees"].append(user.id)
            # Also update the in-memory company object
            company_registry[user.employed_by].employees.append(user.id)
    
    return data

def update_data(target_id, **kwargs):
    """Updates a user's data in JSON and syncs the in-memory object."""
    global user_registry
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
            
        if target_id not in data["users"]:
            data["users"][target_id] = {}

        for key, value in kwargs.items():
            data["users"][target_id][key] = value
            
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
        
        # Update/Create the in-memory object
        u = data["users"][target_id]
        user_registry[target_id] = Users(
            id=target_id,
            name=u.get("name", ""),
            password=u.get("password", ""),
            balance=u.get("balance", 0),
            is_admin=u.get("is_admin", False),
            employed_by=u.get("employed_by", None)
        )
        
            
    except Exception as e:
        print(f"Error updating database: {e}")

def add_employee_to_company(company_id, user_id):
    """Links an employee to a company in the database."""
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
        
        if company_id in data["companies"]:
            if user_id not in data["companies"][company_id]["employees"]:
                data["companies"][company_id]["employees"].append(user_id)
                
                # If using in-memory registry, sync it here too
                if company_id in company_registry:
                    company_registry[company_id].employees.append(user_id)
        
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error linking employee: {e}")

def init_database():
    """Initializes database file and populates global registries."""
    global user_registry, company_registry

    if not os.path.exists(DATABASE_FILE):
        print("No database found. Initializing...")
        data = create_initial_structure()
        data = populate_database(data)
        
        try:
            with open(DATABASE_FILE, 'w') as file:
                json.dump(data, file, indent=4)
                print(f"Database created: {CITIZEN_COUNT} citizens, {COMPANY_COUNT} companies.")
        except Exception as e:
            print(f"File creation error: {e}")
    else:
        print("Loading existing data into memory...")
        try:
            with open(DATABASE_FILE, "r") as file:
                data = json.load(file)
                
            # Populate user_registry from file
            for uid, info in data["users"].items():
                user_registry[uid] = Users(
                    id=uid, name=info["name"], password=info["password"],
                    balance=info["balance"], is_admin=info["is_admin"],
                    employed_by=info["employed_by"]
                )
            
            # Populate company_registry from file
            for cid, info in data["companies"].items():
                company_registry[cid] = Companies(
                    name=info["name"], owner=info["owner"], vault=info["vault"],
                    employees=info["employees"], salary=info["salary"],
                    commodity=info["commodity"], production_rate=info["production_rate"]
                )
        except Exception as e:
            print(f"Error loading database: {e}")

if __name__ == "__main__":
    init_database()