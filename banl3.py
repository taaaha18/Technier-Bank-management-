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
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions

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
        if n <= len(self.transactions):
            return self.transactions[-n:]
        else:
            return self.transactions

    @staticmethod
    def from_dict(data):
        return BankAccount(
            data["account_number"],
            data["name"],
            data["password"],
            data["balance"],
            data["transactions"],
        )

    def toDict(self):
      return{
          "account_number":self.account_number,
           "name":self.name,
           "password":self.password ,
           "balance":self.balance,
            "transactions":self.transactions}
    
class BankSystem:
        def __init__(self):
            self.accounts = {}
            self.load_accounts()   

        def load_accounts(self ):
            files=os.listdir()
            max_number=999
            for filename in files:
                if filename.startswith("account_") and filename.endswith(".json"):
                    try:
                        match=re.findall("account_(\\d+)\\.json", filename)
                        if match:
                            acc_num=int(match[0])
                            files=(open(filename, "r"))
                            data = json.load(files)
                            files.close()
                            account= BankAccount.from_dict(data)
                            self.accounts[acc_num] = account
                            if acc_num > max_number:
                              max_number = acc_num
                    except Exception as e:
                        print("Error loading account from" + filename +str(e))

        def save_account(self, account):
            filename="account_" + str(account).account_number + ".json"
            f=open(filename,"w")
            json.dump(account.toDict(),f,indent=4)
            f.close()

        def load_account(self, account_number):
           filename="account_" +str(account_number) + ".json"
           try:
               f=open(filename,"r")
               data=json.load()
               f.close()
               account=BankAccount.from_dict(data)
               self.accounts[account_number]=account
               return account
           except Exception as e:
                print("Error loading account:", str(e))
                return None
               
               
                

        def login(self, account_number, password):
          if account_number in self.accounts:
            account = self.accounts[account_number]
          else:
            account = self.load_account(account_number)

          if account is not None and account.password == password:
           print("Welcome back,", account.name)
           return account
          else:
           print("Invalid account number or password")
           return None
                  

        
        def create_account(self, name, password, balance):
           account = BankAccount(self.next_account_number, name, password, balance)
           self.accounts[self.next_account_number] = account
           self.save_account(account)
           print("Account created. Your account number is", account.account_number)
           self.next_account_number = self.next_account_number + 1
      


def main():
    bank = BankSystem()

    while True:
        print("\nMain Menu")
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

            if user is not None:
                while True:
                    print("\nAccount Menu")
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
                        print("Balance:", user.check_balance())

                    elif option == '4':
                        n = int(input("How many recent transactions? "))
                        txns = user.getTransactionsHistory(n)
                        for t in txns:
                            print(t)

                    elif option == '5':
                        print("Logged out.")
                        break

                    else:
                        print("Invalid option")

        elif choice == '3':
            print("Thank you for using the Bank System!")
            break
        else:
            print("Invalid choice. Try again.")

main()
