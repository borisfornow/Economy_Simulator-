import sys
from .database import init_db
from .views import sim


def main():
    # 1. Ensure the environment is ready
    init_db.init_database()

    sim.sim()

if __name__ == "__main__":
    main()