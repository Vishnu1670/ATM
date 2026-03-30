import json
import os
import smtplib  
from email.mime.text import MIMEText


class EmailService:
    def __init__(self):
        self.sender_email = "vishnuvardhan1691@gmail.com"
        self.sender_password = "buyn zbxi vpnw uvpl"  # Gmail App Password

    def send_email(self, receiver_email, subject, message):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = receiver_email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print("Email failed:", e)

# ATM:

# 1. Account register
# 2. Duplicate account Validation
# 3. Account deposit
# 4. Withdraw
# 5. Balance
# 6. Pin change
# 7. Fund transfer
# 8. Transaction Statement
class ATM(EmailService):
    def __init__(self):
        super().__init__() 
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
    def logout(self):
        option = input("\nAre you sure you want to logout? y/n: ").lower()

        if option == "y":
            self.current_acc = ""
            print("\nLogout Successfully!..")
        elif option == "n":
            print("\nNot Logout")
        else:
            print("\nInvalid input! Please enter y or n")
        
    #Account register
    def account_reg(self):
            acc_no = input("\nEnter the Account Number: ")
            if acc_no == "":
                print("Account number cannot be empty")
                return
            #check the Account name alredy Exist
            if acc_no in self.Accounts:
                print("\nAccount Number Alerdy Exist!..Try Something New. ")
                return
            
            name = input("\nEnter the Name: ")
            #The must be a alphabet
            if not name.isalpha():
                print("\nThe name must be in Alphabet")
                return

            ph = input("\nEnter the Phone Number: +91 ")
            #The ph num must be 10digit and must be an integer
            if len(ph) != 10 or  not ph.isdigit():
                print("\nPlease enter 10 digit Phone number !..")
                return
            
            pin = input("\nEnter a 4 Digit PIN Number: ")
            #Check the pin
            if len(pin) != 4 or  not pin.isdigit():
                print("\nThe Pin must be 4 digit number!..")
                return
            
            try:
                balance = float(input("\nEnter the Deposit Amount: "))

                if balance <= 0:
                    print("\nAmount must be greater than 0!..")
            except ValueError:
                print("\nPlease enter a valid number!..")
        
            #assing the data
            self.Accounts[acc_no] = {
                "name": name,
                "ph": int(ph),
                "pin": int(pin),
                "balance": float(balance),
                "acc_statement": []
            }

            print("Register Succefully")
            #saves to the file
            self.save()

    #login function
    def login(self):
        acc_no = input("Enter the Account :")

        #check the account num alredy login
        if acc_no == self.current_acc:
            print("\nThis Account have alredy login")
            return
        #check the account num is not register
        if acc_no not in self.Accounts:
            print("\nAccount number not Exist, Please Register first")
            return
        #checking the pin for 3 times
        for i in range(3):
            pin = int(input("Enter PIN: "))
            if self.Accounts[acc_no]["pin"] == pin:
                self.current_acc = acc_no
                print("\nLogin Successful")
                break
            else:
                #less the count every time the pin invalid
                count = 2 - i
                print(f"Invalid PIN. You have {count} attempt left")
        else:
            print("\nThree failed attempts. Try again later.")

    #function for cash deposit:
    def deposit(self):        
        pin = int(input("Enter the pin: "))
        if pin != self.Accounts[self.current_acc]["pin"]:
            print("\nEnter the correct PIN")
            return

        amount = float(input("\nEnter the amount you want to Deposit: "))
        balance = self.Accounts[self.current_acc]["balance"]
        add_balance = amount + balance

        if amount <= 0:
            print("\nCan't give Negative value or Zero ")
            return
        
        self.Accounts[self.current_acc]["balance"] = add_balance
        self.Accounts[self.current_acc]["acc_statement"].append(f"Amount Deposited {amount}., total balance = {add_balance}")
        print (f'\nSuccefully Deposited!.. This is your Current balance {add_balance} ')
        self.save()

    def withdraw(self):        
        pin = int(input("Enter the pin: "))
        if pin != self.Accounts[self.current_acc]["pin"]:
            print("Enter the correct PIN")
            return
        
        amount = float(input("Enter the amount you want to withdraw: "))
        balance = self.Accounts[self.current_acc]["balance"]

        if amount <= 0:
            print("Invalid amount")
            return

        if balance < amount:
            print ("Insufficient balance!..")
            return
        
        withdraw_balance = balance - amount
        self.Accounts[self.current_acc]["balance"] = withdraw_balance
        self.Accounts[self.current_acc]["acc_statement"].append(f"Amount Withdraw {amount}, total balance = {withdraw_balance}")
        print (f'\nSuccefully Withdraw!.. This is your Current balance {withdraw_balance}')
        self.save()

    #Balance check
    def show_balance(self):
        #check with the pin 
        pin = int(input("Enter your PIN Number: "))
        if pin != self.Accounts[self.current_acc]["pin"]:
            print("Enter the Correct PIN!..")
            return
        balance = self.Accounts[self.current_acc]["balance"]
        print(f"\nYour Balance is RS: {balance}")

    #change Account pin
    def pin_change(self):  
        #get old to check the user
        old_pin = int(input("Enter your old pin: "))
        #getting the new pin
        og_pin = self.Accounts[self.current_acc]["pin"]
        #checking the correct pin
        while True:
            if old_pin != og_pin:
                print("\nEnter the correct pin")
            else:
                break
        
        new_pin = int(input("Enter the new Pin: "))
        #check the old and new pin are same
        while True:
            if new_pin == old_pin:
                print("\nOld PIN Can not be your New PIN")
            else:
                break
        
        check_new = int(input("Enter the new Pin again for conformation: "))
        #getting the two step conformation 
        if new_pin == check_new:
            self.Accounts[self.current_acc]["pin"] = new_pin
            print("\nNew pin Updated succefully ")
        else:
            print("Please update the new pin correctly in conformation")
        self.save()


    #Transfer amount to anothe Account
    def fund_transfer(self):
        to_acc = input("Enter the reciver account: ")
        #Check the receiver account Exist
        while True:
            if  to_acc not in self.Accounts:
                print("\nReciver account not found") 
            else:
                break
        #we cannot transfer the amount to the same account
        while True:
            if to_acc == self.current_acc:
                print("\nYou cannot transfer to your own account")
            else:
                break
        
        transfer_amount = int(input("Enter the Amount: "))
        #check the balance
        if self.Accounts[self.current_acc]["balance"] < transfer_amount:
            print(f"\nInsufficient balance!.. your current Balance {self.Accounts[self.current_acc]['balance']} ")
            return

        #calculation for debit and credit the account balance
        self.Accounts[self.current_acc]["balance"] -= transfer_amount
        self.Accounts[to_acc]["balance"] += transfer_amount

        #sendind the message to the transation statement
        self.Accounts[self.current_acc]["acc_statement"].append(f"Amount Transfer too {to_acc}. Transfered Amount = {float(transfer_amount)}. current balance {float(self.Accounts[self.current_acc]['balance'])}")
        self.Accounts[to_acc]["acc_statement"].append(f"Amount Received From {self.current_acc}. Received Amount = {float(transfer_amount)}. current balance {float(self.Accounts[to_acc]['balance'])}")
        
        print("Transfered Succefully")
        self.save()

    def show_transation_statement(self):
        #print the acc statement
        statement = self.Accounts[self.current_acc]["acc_statement"]
        for s in statement:
            print (s)
        print("-------------Done--------------")

    def del_account(self):
        #getting conformation to delete the account
        confirm = input("Are you sure you want to delete this account? y/n: ").lower()
        if confirm == "y":
            #using del keyword to delete the account data
            del self.Accounts[self.current_acc]
            #auto logout 
            self.current_acc = ""
            self.save()
            print("Account deleted successfully")
        else:
            print("Cancelled")

#Assiging  the object for the class 
atm = ATM()
while True:
    #check is it in the current account
    if not atm.current_acc:
        print("""
        1. Account register
        2. Login
        3. Exit
        """)

        choice = int(input("Enter option: "))

        if choice == 1:
            atm.account_reg()
        elif choice == 2:
            atm.login()
        elif choice ==3:
            break
        else:
            print("Invalid Choice")
    #if login this print statement shows
    else:
        print(f"\nLogged in as: {atm.Accounts[atm.current_acc]['name']}")

        print("""
        1. Cash Deposit
        2. Cash Withdraw
        3. Balance Enquiry
        4. Change PIN
        5. Amount Transfer                
        6. Transaction Statement
        7. Delete Account
        8. Logout
        """)

        choice = int(input("Enter option: "))

        if choice == 1:
            atm.deposit()
        elif choice == 2:
            atm.withdraw()
        elif choice == 3:
            atm.show_balance()
        elif choice == 4:
            atm.pin_change()
        elif choice == 5:
            atm.fund_transfer()
        elif choice == 6:
            atm.show_transation_statement()
        elif choice == 7:
            atm.del_account()
        elif choice == 8:
            atm.logout()
        else:
            print("Invalid Choice")


    