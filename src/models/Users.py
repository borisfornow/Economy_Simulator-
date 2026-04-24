import random

class User:
    def __init__(self, id, name, password, balance, is_admin, employed_by, health=None, energy=None, luxury=None):
        self.id = id
        self.name = name
        self.password = password
        self.balance = balance
        self.is_admin = is_admin
        self.employed_by = employed_by
        
        # Simulation stats
        self.is_alive = True
        
        # If stats are provided (from JSON), use them. Otherwise, generate random starts.
        self.health = health if health is not None else random.randint(60, 100)
        self.energy = energy if energy is not None else random.randint(4, 10)
        self.luxury = luxury if luxury is not None else random.randint(1, 5)

    def update_balance(self, amount):
        """Standard method for simple balance adjustments."""
        self.balance += amount

    def death_check(self):
        """Checks health and updates status."""
        if self.health <= 0:
            self.is_alive = False
            print(f"💀 {self.name} (ID: {self.id}) has died.")
            return True 
        return False

    def __repr__(self):
        """Helpful for debugging in the console."""
        return f"<User {self.name} | Balance: {self.balance} | HP: {self.health}>"