"""Handle all JSON file I/O and object serialization."""

import json
import os

# Get the database file path relative to the project root
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.json")


def save_to_disk(data):
    """The single point of entry for writing to the JSON file."""
    try:
        with open(DATABASE_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Save error: {e}")


def load_database():
    """Returns the current database contents or creates the default structure."""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return create_initial_structure()


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


def user_to_dict(user_obj):
    """Serialize a User object to a dictionary."""
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
    """Serialize a Company object to a dictionary."""
    return vars(company_obj)


def persist_users(user_registry, data):
    """Sync all users from RAM to JSON structure."""
    data.setdefault("users", {})
    for uid, user_obj in user_registry.items():
        data["users"][uid] = user_to_dict(user_obj)
    return data


def persist_companies(company_registry, data):
    """Sync all companies from RAM to JSON structure."""
    data.setdefault("companies", {})
    for cid, comp_obj in company_registry.items():
        data["companies"][cid] = company_to_dict(comp_obj)
    return data


def persist_products(product_registry, data):
    """Sync all products from RAM to JSON structure."""
    data.setdefault("products", {})
    data["products"] = dict(product_registry)
    return data


def sync_registry_to_json(user_registry, company_registry):
    """Sync user and company registries to JSON."""
    data = load_database()
    data = persist_users(user_registry, data)
    data = persist_companies(company_registry, data)
    save_to_disk(data)


def save_product_registry(product_registry):
    """Sync product registry to JSON."""
    data = load_database()
    data = persist_products(product_registry, data)
    save_to_disk(data)


def remove_user_from_data(user_id):
    """Remove a user from the JSON data."""
    data = load_database()
    if "users" in data and user_id in data["users"]:
        del data["users"][user_id]
        save_to_disk(data)
