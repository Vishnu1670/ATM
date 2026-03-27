import json
import os

# ATM:

# 1. Account register
# 2. Duplicate account Validation
# 3. Account deposit
# 4. Withdraw
# 5. Balance
# 6. Pin change
# 7. Fund transfer
# 8. Transaction Statement
class ATM:
    def __init__(self):
        # File that store json dats
        self.File = "accounts.json"
        #The place were the data saves
        self.Accounts = {}
        #To check the account is login or not
        self.current_acc = ""
        
        #open the path for the file to get data
        if os.path.exists(self.File):
            try:
                with open(self.File,"r") as f:
                    self.Accounts = json.load(f)
            except json.JSONDecodeError:
                self.Accounts = {}
        else:
            self.Accounts = {}


    #saves the data to the json file
    def save(self):
        with open(self.File,"w") as f:
            json.dump(self.Accounts, f, indent=4)

    #logout from the current Account login
    def logout():
        global current_acc

        option = input("\nAre you sure you want to logout? y/n: ").lower()

        if option == "y":
            current_acc = ""
            print("\nLogout Successfully!..")
        elif option == "n":
            print("\nLogout Cancelled")
        else:
            print("\nInvalid input! Please enter y or n")
        
    #Account register
    def account_reg():
        acc_no = input("Enter the Account Number: ")
        #check the Account name alredy Exist
        if acc_no in Accounts:
            print("\nAccount Alerdy Exist")
            return
        
        name = input("Enter the Name: ")
        #The must be a alphabet
        if not name.isalpha():
            print("\nThe name must be Alphabet")
            return
        
        ph = input("Enter the Phone Number: +91")
        #The ph num must be 10digit and must be an integer
        if len(ph) != 10 or  not ph.isdigit():
            print("\nPlease enter 10 digit number !..")
            return
        
        pin = input("Enter the 4 Digit PIN Number: ")
        #Check the pin
        if len(pin) != 4 or  not pin.isdigit():
            print("\nPlease the Pin must be 4 digit number!..")
            return
        
        balance = input("Enter the Deposit Amount: ")
        #check the balance is number
        if not balance.isdigit() :
            print("\nInvalide Balance Entry !..")
            return
        
        #assing the data
        Account = {}
        Account["name"]= name
        Account["ph"]= int(ph)
        Account["pin"]= int(pin)
        Account["balance"]= float(balance) 
        Account["acc_statement"] = []
        Accounts[acc_no] = Account

        print("Register Succefully")
        #saves to the file
        save()

    #login function
    def login():
        #refer the gobal current account
        global current_acc

        acc_no = input("Enter the Account :")
        #check the account num alredy login
        if acc_no == current_acc:
            print("\nThis Account have alredy login")
            return

        pin = int(input("\nEnter the pin: "))
        #check the account num is not register
        if acc_no not in Accounts:
            print("\nAccount number not Exist, Please Register first")
            return
        
        account = Accounts.get(acc_no)

        og_pin = account.get("pin")
        #check the pin
        if og_pin != pin :
            print("\nInvalid PIN")
            return
        current_acc = acc_no
        print("\nLogin Succefully!..")

    #function for cash deposit
    def deposit():
        #check the account num login 
        if not current_acc :
            print ("\nPlease Login first")
            return
        
        pin = int(input("Enter the pin: "))
        if pin != Accounts[current_acc]["pin"]:
            print("\nEnter the correct PIN")
            return

        amount = input("\nEnter the amount you want to Deposit: ")
        balance = Accounts[current_acc]["balance"]
        add_balance = float(amount) + balance

        if add_balance < balance:
            print("\nCan't give Negative value ")
            return
        
        Accounts[current_acc]["balance"] = add_balance
        Accounts[current_acc]["acc_statement"].append(f"Amount Deposited {amount}., total balance = {add_balance}")
        print (f'\nSuccefully Deposited!.. This is your Current balance {add_balance} ')
        save()

    def withdraw():
        #check the account num login 
        if not current_acc :
            print ("login first")
            return
        
        pin = int(input("Enter the pin: "))
        if pin != Accounts[current_acc]["pin"]:
            print("Enter the correct PIN")
            return
        
        amount = input("Enter the amount you want to withdraw: ")
        balance = Accounts[current_acc]["balance"]

        if amount < balance:
            print("Can't give Negative value ")
            return

        if balance < amount:
            print ("Insufficient balance!..")
            return
        
        withdraw_balance = balance - float(amount)
        Accounts[current_acc]["balance"] = withdraw_balance
        Accounts[current_acc]["acc_statement"].append(f"Amount Withdraw {amount}, total balance = {withdraw_balance}")
        print (f'\nSuccefully Withdraw!.. This is your Current balance {withdraw_balance}')
        save()

    def show_balance():
        #check the account num login 
        if not current_acc:
            print("login first")
            return
        balance = Accounts[current_acc]["balance"]
        print(f"\nYour Balance is RS: {balance}")

    def pin_change():
        #check the account num login 
        if not current_acc:
            print("login first")
            return
        
        old_pin = int(input("Enter your old pin: "))

        og_pin = Accounts[current_acc]["pin"]

        if old_pin != og_pin:
            print("\nEnter the correct pin")
            return
        
        new_pin = int(input("Enter the new Pin: "))
        check_new = int(input("Enter the new Pin again for conformation: "))

        if new_pin == check_new:
            Accounts[current_acc]["pin"] = new_pin
            print("\nNew pin Updated succefully ")
        else:
            print("Please update the new pin correctly in conformation")
        save()

    #Transfer amount to anothe Account
    def fund_transfer():
        #check the account num login 
        if not current_acc:
            print("login first")
            return
        to_acc = input("Enter the reciver account: ")

        #Check the receiver account Exist
        if  to_acc not in Accounts:
            print("\nReciver account not found") 
            return
        #we cannot transfer the amount to the same account
        if to_acc == current_acc:
            print("\nYou cannot transfer to your own account")
            return
        
        transfer_amount = int(input("Enter the Amount: "))
        #check the balance
        if Accounts[current_acc]["balance"] < transfer_amount:
            print(f"\nInsufficient balance!.. your current Balance {Accounts[current_acc]['balance']} ")
            return

        
        Accounts[current_acc]["balance"] -= transfer_amount
        Accounts[to_acc]["balance"] += transfer_amount

        Accounts[current_acc]["acc_statement"].append(f"Amount Transfer too {to_acc}. Transfered Amount = {float(transfer_amount)}. current balance {float(Accounts[current_acc]['balance'])}")
        Accounts[to_acc]["acc_statement"].append(f"Amount Received From {current_acc}. Received Amount = {float(transfer_amount)}. current balance {float(Accounts[to_acc]['balance'])}")
        
        print("Transfered Succefully")
        save()

    def show_transation_statement():
        #check the account num login 
        if not current_acc:
            print("login first")
            return
        
        #print the acc statement
        statement = Accounts[current_acc]["acc_statement"]
        for s in statement:
            print (s)
        print("-------------Done--------------")

while True:
    if not current_acc:
        print("""
        1. Account register
        2. Login
        3. Exit
        """)

        choice = int(input("Enter option: "))

        if choice == 1:
            account_reg()

        elif choice == 2:
            login()

        elif choice == 3:
            break

        else:
            print("Invalid Choice")

    else:
        print(f"\nLogged in as: {Accounts[current_acc]["name"]}")

        print("""
        1. Cash Deposit
        2. Cash Withdraw
        3. Balance Enquiry
        4. Change PIN
        5. Transfer Amount                
        6. Transaction Statement
        7. Logout
        """)

        choice = int(input("Enter option: "))

        if choice == 1:
            deposit()

        elif choice == 2:
            withdraw()

        elif choice == 3:
            show_balance()

        elif choice == 4:
            pin_change()

        elif choice == 5:
            fund_transfer()

        elif choice == 6:
            show_transation_statement()

        elif choice == 7:
            logout()

        else:
            print("Invalid Choice")


    