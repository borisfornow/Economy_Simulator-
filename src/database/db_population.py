"""Handle initial database population and data generation."""

import random
from ..models import Users, Companies
from .persistence import create_initial_structure
from ..controllers.sync import sync_product_registry

# Configuration constants
JOB_PROBABILITY = 0.90
COMPANY_COUNT = 3
CITIZEN_COUNT = 5
COMPANY_STARTING_CAPITAL = 50000


def populate_database(user_registry, company_registry, product_registry, data=None):
    """Initial population for a fresh database."""
    if data is None:
        data = create_initial_structure()

    product_list = ["health", "energy", "luxury"]

    # Generate Companies
    for i in range(1, COMPANY_COUNT + 1):
        comp_id = f"CO-{i}"
        commodity = random.choice(product_list) if product_list else "general"
        if product_list:
            product_list.remove(commodity)

        company = Companies.Company(
            name=f"Enterprise_{comp_id}",
            owner="0",
            vault=COMPANY_STARTING_CAPITAL,
            employees=[],
            salary=random.randint(40, 80),
            commodity=commodity,
            production_rate=random.randint(1, 5)
        )
        company_registry[comp_id] = company
        data["companies"][comp_id] = vars(company)

    # Generate Citizens
    company_ids = list(data["companies"].keys())
    for i in range(1, CITIZEN_COUNT + 1):
        uid = str(i)
        job = random.choice(company_ids) if random.random() < JOB_PROBABILITY else None

        user = Users.User(
            uid,
            f"citizen_{uid}",
            "password",
            random.randint(50, 100),
            False,
            job
        )
        user_registry[uid] = user
        data["users"][uid] = {
            "name": user.name,
            "password": user.password,
            "balance": user.balance,
            "is_admin": user.is_admin,
            "employed_by": user.employed_by,
            "health": user.health,
            "energy": user.energy,
            "luxury": user.luxury
        }
        if job:
            data["companies"][job]["employees"].append(uid)
            company_registry[job].employees.append(uid)

    sync_product_registry(company_registry, product_registry, data)
    return data
