import os
import re
import json
from datetime import datetime   

class BankAccount:
    def __init__(self, account_number, name, password, balance=0.0, transactions=None):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.transactions = transactions if transactions else []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        else:
            self.balance -= amount
            self.transactions.append({
                'type': 'withdraw',
                'amount': amount,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return True

    def check_balance(self):
        return self.balance

    def getTransactionsHistory(self, n):
        return self.transactions[-n:] if n <= len(self.transactions) else self.transactions

    @staticmethod
    def from_dict(data):
        return BankAccount(
            data["account_number"],
            data["name"],
            data["password"],
            data["balance"],
            data["transactions"]
        )

    def toDict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "password": self.password,
            "balance": self.balance,
            "transactions": self.transactions
        }

class Bank_DB:
    def __init__(self):
        self.next_acc_no = 1000
        self.loadFile()

    def loadFile(self):
        files = os.listdir()
        self.next_account_number = self.next_acc_no
        for file in files:
            if re.match(r"accounts_\d+\.json", file):
                acc_no = int(re.search(r"accounts_(\d+)\.json", file).group(1))
                if acc_no >= self.next_account_number:
                    self.next_account_number = acc_no + 1

    def add_account(self, account):
        fileName = f"accounts_{account.account_number}.json"
        with open(fileName, 'w') as f:
            json.dump(account.toDict(), f, indent=4)
        self.next_account_number += 1

    def get_account(self, account_number):
        fileName = f"accounts_{account_number}.json"
        if os.path.exists(fileName):
            with open(fileName, 'r') as f:
                data = json.load(f)
                return BankAccount.from_dict(data)
        else:
            print("Account not found")
            return None

    def save_account(self, account):
        fileName = f"accounts_{account.account_number}.json"
        with open(fileName, 'w') as f:
            json.dump(account.toDict(), f, indent=4)

class Bank:
    def __init__(self):
        self.db = Bank_DB()

    def create_account(self):
        name = input("Name: ")
        pwd = input("Password: ")
        balance = float(input("Initial Deposit: "))
        acc_no = self.db.next_account_number
        acc = BankAccount(acc_no, name, pwd, balance)
        self.db.add_account(acc)
        print("Account created with number:", acc_no)  

    def login(self):
        acc_no = int(input("Account No: "))
        pwd = input("Password: ")
        acc = self.db.get_account(acc_no)
        if acc and acc.password == pwd:
            print("Welcome,", acc.name)
            self.account_menu(acc)
        else:
            print("Login failed.")     

    def account_menu(self, acc):
        while True:
            print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Last N Transactions\n5. Change Passowrd\n6. Logout")
            ch = input("Choose: ")
            if ch == '1':
                amt = float(input("Amount: "))
                acc.deposit(amt)
                self.db.save_account(acc)
            elif ch == '2':
                amt = float(input("Amount: "))
                if acc.withdraw(amt):
                    self.db.save_account(acc)
            elif ch == '3':
                print("Your Balance is:", acc.check_balance())
            elif ch == '4':
                n = int(input("How many numbers of history do you want? "))
                for t in acc.getTransactionsHistory(n):
                    print(t)
            elif ch=='6':
                new_pwd = input("Enter New Password: ")
                acc.password = new_pwd
                self.db.save_account(acc)
                print("Password changed successfully.")        
            elif ch == '5':
                break

    def run(self):
        while True:
            print("\n1. Create Account\n2. Login\n3. Exit")
            ch = input("Choose: ")
            if ch == '1':
                self.create_account()
            elif ch == '2':
                self.login()
            elif ch == '3':
                break

def main():
    b = Bank()
    b.run()

main()
