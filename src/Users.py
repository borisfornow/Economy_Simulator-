import random

class User:
    def __init__(self, id, name, password, balance, is_admin, employed_by):
        self.id = id
        self.name = name
        self.password = password
        self.balance = balance
        self.is_admin = is_admin
        self.employed_by = employed_by
        
        # Simulation stats
        self.is_alive = True
        self.health = random.randint(60, 100)
        self.energy = random.randint(4, 10)
        self.luxury = random.randint(1, 5)

    def update_balance(self, amount):
        self.balance += amount

    def death_check(self):
        """Checks health and updates status."""
        if self.health <= 0:
            self.is_alive = False
            print(f"💀 {self.name} (ID: {self.id}) has died.")
            return True # Return True so the main loop knows to remove them
        return False