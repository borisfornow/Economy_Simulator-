import json
import os
import random
import Users, Companies, Banks

# Get the database file path relative to the project root
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.json")
JOB_PROBABILITY = 0.90
COMPANY_COUNT = 3  
CITIZEN_COUNT = 20
STARTING_CAPITAL = 50000

# Global registries for quick in-memory access
user_registry = {}
company_registry = {}
product_registry = {} 

# --- CORE UTILITIES ---

def save_to_disk(data):
    """The single point of entry for writing to the JSON file."""
    try:
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Save error: {e}")

def create_initial_structure():
    """Returns the base dictionary template."""
    return {
        "users": {
            "0": {
                "name": "admin", "password": "password", "balance": 10000000,
                "is_admin": True, "employed_by": None, "health": 100, "energy": 10, "luxury": 5
            }
        },
        "companies": {},
        "products": {},
        "bank": {"total_reserves": 5000000, "interest_rate": 0.05}
    }

# --- CORE DB HELPERS ---

def load_database():
    """Returns the current database contents or creates the default structure."""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return create_initial_structure()


def user_to_dict(user_obj):
    return {
        "name": user_obj.name,
        "password": user_obj.password,
        "balance": user_obj.balance,
        "is_admin": user_obj.is_admin,
        "employed_by": user_obj.employed_by,
        "health": user_obj.health,
        "energy": user_obj.energy,
        "luxury": user_obj.luxury
    }


def company_to_dict(company_obj):
    return vars(company_obj)


def persist_users(data):
    data.setdefault("users", {})
    for uid, user_obj in user_registry.items():
        data["users"][uid] = user_to_dict(user_obj)
    return data


def persist_companies(data):
    data.setdefault("companies", {})
    for cid, comp_obj in company_registry.items():
        data["companies"][cid] = company_to_dict(comp_obj)
    return data


def persist_products(data):
    data.setdefault("products", {})
    data["products"] = dict(product_registry)
    return data


# --- SYNC & UPDATE LOGIC ---

def update_data(target_id, **kwargs):
    """Updates a user in RAM and disk.

    If the user exists in RAM, update the object first. Otherwise create it from JSON data.
    """
    global user_registry
    try:
        data = load_database()
        data.setdefault("users", {})
        data["users"].setdefault(target_id, {})
        data["users"][target_id].update(kwargs)

        if target_id in user_registry:
            user_obj = user_registry[target_id]
            for key, value in kwargs.items():
                if hasattr(user_obj, key):
                    setattr(user_obj, key, value)
        else:
            user_info = data["users"][target_id]
            user_registry[target_id] = Users.User(
                id=target_id,
                name=user_info.get("name", ""),
                password=user_info.get("password", ""),
                balance=user_info.get("balance", 0),
                is_admin=user_info.get("is_admin", False),
                employed_by=user_info.get("employed_by", None),
                health=user_info.get("health"),
                energy=user_info.get("energy"),
                luxury=user_info.get("luxury")
            )

        save_to_disk(persist_users(data))
    except Exception as e:
        print(f"Error updating user {target_id}: {e}")

def update_company_data(company_id, **kwargs):
    """Updates a company in RAM and disk and refreshes the product registry."""
    global company_registry
    try:
        data = load_database()
        data.setdefault("companies", {})
        data["companies"].setdefault(company_id, {})
        data["companies"][company_id].update(kwargs)

        if company_id in company_registry:
            comp_obj = company_registry[company_id]
            for key, value in kwargs.items():
                if hasattr(comp_obj, key):
                    setattr(comp_obj, key, value)
        else:
            comp_info = data["companies"][company_id]
            company_registry[company_id] = Companies.Company(
                name=comp_info.get("name", ""),
                owner=comp_info.get("owner", ""),
                vault=comp_info.get("vault", 0),
                employees=comp_info.get("employees", []),
                salary=comp_info.get("salary", 0),
                commodity=comp_info.get("commodity", ""),
                production_rate=comp_info.get("production_rate", 0)
            )

        sync_product_registry(data)
        save_to_disk(persist_products(persist_companies(data)))
    except Exception as e:
        print(f"Error updating company {company_id}: {e}")


def add_employee_to_company(company_id, user_id):
    """Adds a user to a company's employee list using update_company_data."""
    global company_registry

    if company_id not in company_registry:
        # Load company from JSON if not already in RAM
        data = load_database()
        if company_id not in data.get("companies", {}):
            return
        company_info = data["companies"][company_id]
        company_registry[company_id] = Companies.Company(
            name=company_info.get("name", ""),
            owner=company_info.get("owner", ""),
            vault=company_info.get("vault", 0),
            employees=company_info.get("employees", []),
            salary=company_info.get("salary", 0),
            commodity=company_info.get("commodity", ""),
            production_rate=company_info.get("production_rate", 0)
        )

    company_obj = company_registry[company_id]
    if user_id not in company_obj.employees:
        company_obj.employees.append(user_id)
        update_company_data(company_id, employees=company_obj.employees)


def sync_product_registry(current_data_dict=None):
    """Refreshes product list based on current companies in RAM."""
    global company_registry, product_registry
    product_registry.clear()
    for cid, company in company_registry.items():
        product_registry[company.commodity] = {
            "name": company.commodity.capitalize(),
            "producer": cid,
            "price": 50
        }
    if current_data_dict is not None:
        current_data_dict["products"] = dict(product_registry)

# --- INITIALIZATION ---

def populate_database(data):
    """Initial population for a fresh database."""
    global user_registry, company_registry
    product_list = ["health", "energy", "luxury"]
    
    # Generate Companies
    for i in range(1, COMPANY_COUNT + 1):
        comp_id = f"CO-{i}"
        commodity = random.choice(product_list) if product_list else "general"
        if product_list: product_list.remove(commodity)

        company = Companies.Company(
            name=f"Enterprise_{comp_id}", owner="0", vault=STARTING_CAPITAL,
            employees=[], salary=random.randint(40, 80), 
            commodity=commodity, production_rate=random.randint(1, 5)
        )
        company_registry[comp_id] = company
        data["companies"][comp_id] = vars(company)

    # Generate Citizens
    company_ids = list(data["companies"].keys())
    for i in range(1, CITIZEN_COUNT + 1):
        uid = str(i)
        job = random.choice(company_ids) if random.random() < JOB_PROBABILITY else None
        
        user = Users.User(uid, f"citizen_{uid}", "password", random.randint(50, 100), False, job)
        user_registry[uid] = user
        data["users"][uid] = {
            "name": user.name, "password": user.password, "balance": user.balance,
            "is_admin": user.is_admin, "employed_by": user.employed_by,
            "health": user.health, "energy": user.energy, "luxury": user.luxury
        }
        if job:
            data["companies"][job]["employees"].append(uid)
            company_registry[job].employees.append(uid)
            
    sync_product_registry(data)
    return data

def init_database():
    """Main loader: Connects Disk to RAM."""
    global user_registry, company_registry, product_registry

    if not os.path.exists(DATABASE_FILE):
        data = populate_database(create_initial_structure())
        save_to_disk(data)

    data = load_database()

    for uid, info in data.get("users", {}).items():
        user_registry[uid] = Users.User(
            uid, info["name"], info["password"], info["balance"], info["is_admin"], 
            info["employed_by"], info.get("health"), info.get("energy"), info.get("luxury")
        )

    for cid, info in data.get("companies", {}).items():
        company_registry[cid] = Companies.Company(
            info["name"], info["owner"], info["vault"], info["employees"], 
            info["salary"], info["commodity"], info["production_rate"]
        )

    if data.get("products"):
        product_registry.update(data["products"])
    else:
        sync_product_registry(data)
        save_to_disk(data)

if __name__ == "__main__":
    init_database()