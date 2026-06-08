def add(num1: int, num2: int):
    return num1 + num2

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1