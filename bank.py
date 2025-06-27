import json
import os
import re
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
            print(" Insufficient funds")
        else:
            self.balance -= amount
            self.transactions.append({
                'type': 'withdraw',
                'amount': amount,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    def check_balance(self):
        return self.balance

    def getTransactionsHistory(self, n):
        return self.transactions[-n:] if n <= len(self.transactions) else self.transactions

    def toDict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "password": self.password,
            "balance": self.balance,
            "transactions": self.transactions
        }

    @staticmethod
    def from_dict(data):
        return BankAccount(
            account_number=data["account_number"],
            name=data["name"],
            password=data["password"],
            balance=data["balance"],
            transactions=data["transactions"]
        )


class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.next_account_number = 1000
        self.load_all_accounts()

    def load_all_accounts(self):
        account_files = [f for f in os.listdir() if f.startswith("account_") and f.endswith(".json")]
        max_account_num = 999

        for filename in account_files:
            try:
                acc_num = int(re.findall(r"account_(\d+)\.json", filename)[0])
                with open(filename, "r") as f:
                    data = json.load(f)
                    account = BankAccount.from_dict(data)
                    self.accounts[acc_num] = account
                    if acc_num > max_account_num:
                        max_account_num = acc_num
            except Exception as e:
                print(f"Error loading {filename}: {e}")

        self.next_account_number = max_account_num + 1

    def create_account(self, name, password, balance=0.0):
        account = BankAccount(
            account_number=self.next_account_number,
            name=name,
            password=password,
            balance=balance
        )
        self.accounts[self.next_account_number] = account
        self.save_account(account)
        print(f" Account created. Your account number is {account.account_number}")
        self.next_account_number += 1

    def save_account(self, account):
        with open(f"account_{account.account_number}.json", "w") as f:
            json.dump(account.toDict(), f, indent=4)

    def load_account(self, account_number):
        try:
            with open(f"account_{account_number}.json", "r") as f:
                data = json.load(f)
                account = BankAccount.from_dict(data)
                self.accounts[account_number] = account
                return account
        except FileNotFoundError:
            print(" Account not found.")
            return None

    def login(self, account_number, password):
        account = self.load_account(account_number)
        if account and account.password == password:
            print(f" Welcome back, {account.name}!")
            return account
        else:
            print(" Invalid account number or password")
            return None


def main():
    bank = BankSystem()

    while True:
        print("\n Main Menu")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == '1':
         name = input("Enter your name: ")
         password = input("Set a password: ")
         balance = float(input("Enter opening balance: "))
         bank.create_account(name, password, balance)

        elif choice == '2':
            acc_no = int(input("Enter your account number: "))
            pwd = input("Enter password: ")
            user = bank.login(acc_no, pwd)

            if user:
                while True:
                    print("\n Account Menu")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. View Last N Transactions")
                    print("5. Logout")

                    option = input("Choose an option: ")

                    if option == '1':
                        amt = float(input("Amount to deposit: "))
                        user.deposit(amt)
                        bank.save_account(user)

                    elif option == '2':
                        amt = float(input("Amount to withdraw: "))
                        user.withdraw(amt)
                        bank.save_account(user)

                    elif option == '3':
                        print(f" Balance: {user.check_balance()}")

                    elif option == '4':
                        n = int(input("How many recent transactions? "))
                        txns = user.getTransactionsHistory(n)
                        for t in txns:
                            print(t)

                    elif option == '5':
                        print(" Logged out.")
                        break

                    else:
                        print(" Invalid option")

        elif choice == '3':
            print(" Thank you for using the Bank System!")
            break
        else:
            print(" Invalid choice. Try again.")

main()
