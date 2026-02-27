class Users():
    def __init__(self, name, password, balance, is_admin, job):
        self.name = name 
        self.password = password
        self.balance = balance
        self.is_admin = is_admin
        self.job = job


class Companies():
    def __init__(self, name, owner, vault, employees, salary):
        self.name = name 
        self.owner = owner
        self.vault = vault
        self.employees = employees
        self.salary = salary

class Banks():
    def __init__(self, total_reserves, intrest_rate):
        self.total_reserves = total_reserves 
        self.intrest_rate = intrest_rate