class Users():
    def __init__(self, id, name, password, balance, is_admin, employed_by):
        self.id = id
        self.name = name
        self.password = password
        self.balance = balance
        self.is_admin = is_admin
        self.employed_by = employed_by
        self.health = 100
        self.energy = 10
        self.luxury = 1



class Companies():
    def __init__(self, name, owner, vault, employees, salary, commodity, production_rate):
        self.name = name 
        self.owner = owner
        self.vault = vault
        self.employees = employees
        self.salary = salary
        self.commodity = commodity
        self.production_rate = production_rate

class Banks():
    def __init__(self, total_reserves, intrest_rate):
        self.total_reserves = total_reserves 
        self.intrest_rate = intrest_rate