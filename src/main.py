import sys
import auth
import init_db
import sim

def main():
    # 1. Ensure the environment is ready
    init_db.init_database()

    sim.sim()

if __name__ == "__main__":
    main()