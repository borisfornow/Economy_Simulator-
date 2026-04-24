"""Handle registry synchronization between RAM and disk."""

from ..models import Users, Companies
from ..database.persistence import load_database, save_to_disk, persist_users, persist_companies, persist_products


def update_data(user_registry, target_id, **kwargs):
    """Updates a user in RAM and disk.
    
    If the user exists in RAM, update the object first. Otherwise create it from JSON data.
    """
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

        save_to_disk(persist_users(user_registry, data))
    except Exception as e:
        print(f"Error updating user {target_id}: {e}")


def update_company_data(company_registry, product_registry, target_company_id, **kwargs):
    """Updates a company in RAM and disk and refreshes the product registry."""
    try:
        data = load_database()
        data.setdefault("companies", {})
        data["companies"].setdefault(target_company_id, {})
        data["companies"][target_company_id].update(kwargs)

        if target_company_id in company_registry:
            comp_obj = company_registry[target_company_id]
            for key, value in kwargs.items():
                if hasattr(comp_obj, key):
                    setattr(comp_obj, key, value)
        else:
            comp_info = data["companies"][target_company_id]
            company_registry[target_company_id] = Companies.Company(
                name=comp_info.get("name", ""),
                owner=comp_info.get("owner", ""),
                vault=comp_info.get("vault", 0),
                employees=comp_info.get("employees", []),
                salary=comp_info.get("salary", 0),
                commodity=comp_info.get("commodity", ""),
                production_rate=comp_info.get("production_rate", 0)
            )

        sync_product_registry(company_registry, product_registry, data)
        save_to_disk(persist_products(product_registry, persist_companies(company_registry, data)))
    except Exception as e:
        print(f"Error updating company {target_company_id}: {e}")


def add_employee_to_company(company_registry, user_id, target_company_id):
    """Adds a user to a company's employee list using update_company_data."""
    if target_company_id not in company_registry:
        # Load company from JSON if not already in RAM
        data = load_database()
        if target_company_id not in data.get("companies", {}):
            return
        company_info = data["companies"][target_company_id]
        company_registry[target_company_id] = Companies.Company(
            name=company_info.get("name", ""),
            owner=company_info.get("owner", ""),
            vault=company_info.get("vault", 0),
            employees=company_info.get("employees", []),
            salary=company_info.get("salary", 0),
            commodity=company_info.get("commodity", ""),
            production_rate=company_info.get("production_rate", 0)
        )

    company_obj = company_registry[target_company_id]
    if user_id not in company_obj.employees:
        company_obj.employees.append(user_id)


def sync_product_registry(company_registry, product_registry, current_data_dict=None):
    """Refreshes product list based on current companies in RAM."""
    product_registry.clear()
    for cid, company in company_registry.items():
        product_registry[company.commodity] = {
            "name": company.commodity.capitalize(),
            "producer": cid,
            "price": 50
        }
    if current_data_dict is not None:
        current_data_dict["products"] = dict(product_registry)
