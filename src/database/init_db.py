"""Main database initialization module. Loads registries from disk."""

import Users
import Companies
import Banks
from persistence import load_database, save_to_disk
from db_population import populate_database
from sync import sync_product_registry, update_data as _update_data, update_company_data as _update_company_data, add_employee_to_company as _add_employee_to_company

# Global registries for quick in-memory access
user_registry = {}
company_registry = {}
product_registry = {}


# --- COMPATIBILITY WRAPPERS ---

def update_data(target_id, **kwargs):
    """Wrapper for sync.update_data with global registries."""
    _update_data(user_registry, target_id, **kwargs)


def update_company_data(company_id, **kwargs):
    """Wrapper for sync.update_company_data with global registries."""
    _update_company_data(company_registry, product_registry, company_id, **kwargs)


def add_employee_to_company(company_id, user_id):
    """Wrapper for sync.add_employee_to_company with global registries."""
    _add_employee_to_company(company_registry, user_id, company_id)


# --- INITIALIZATION ---

def init_database():
    """Main loader: Connects Disk to RAM."""
    global user_registry, company_registry, product_registry

    # Ensure database file exists
    try:
        data = load_database()
    except Exception as e:
        print(f"Error loading database: {e}")
        return

    if not data.get("users") or (len(data.get("users", {})) == 1 and "0" in data["users"]):
        # Database is empty (only admin exists), populate it
        data = populate_database(user_registry, company_registry, product_registry, data)
        save_to_disk(data)
    else:
        # Load existing data into registries
        for uid, info in data.get("users", {}).items():
            user_registry[uid] = Users.User(
                uid,
                info["name"],
                info["password"],
                info["balance"],
                info["is_admin"],
                info["employed_by"],
                info.get("health"),
                info.get("energy"),
                info.get("luxury")
            )

        for cid, info in data.get("companies", {}).items():
            company_registry[cid] = Companies.Company(
                info["name"],
                info["owner"],
                info["vault"],
                info["employees"],
                info["salary"],
                info["commodity"],
                info["production_rate"]
            )

        if data.get("products"):
            product_registry.update(data["products"])
        else:
            sync_product_registry(company_registry, product_registry, data)
            save_to_disk(data)

if __name__ == "__main__":
    init_database()