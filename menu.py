from bank import Bank

bank = Bank()
bank._load()


def menu():
    execute = True
    while(execute):
        print("""\nChoose an option:
         1. Print all customers.
         2. Print specific customer.
         3. Add new customer.
         4. Change customer info.
         5. Delete customer.
         6. Add an account to existing customer.
         7. Close account.
         8. Withdraw/Deposit from/to account.
         9. Exit.
         """)
        try:
            choice = int(input("Choose One Of The Alternatives: "))
            if len(str(choice)) != 1:
                print("Please choose an option between 1 and 9 ")
        except ValueError:
            print("Invalid choice, please try again")


        #Print all existing customers
        if choice == 1:
            print("\nName and SSN")
            for x in bank.customers:
                print(x)



        #Print specific customer
        if choice == 2:
            ssn = ssn_input()
            if ssn != 0:
                print(bank.get_customer(ssn))

        #Creat new customer
        elif choice == 3:
            ssn = ssn_input()
            if ssn != 0:
                first_name = str(input("\nEnter First Name: "))
                last_name = str(input("\nEnter Last Name: "))
                if bank.add_customer(first_name, last_name, ssn):
                    print("\nCustomer With Social Security Number {} Added.".format(ssn))
                else:
                    print("\nThis Social Security Number Already Exists.".format(ssn))


        #Change customer info
        elif choice == 4:
            ssn = ssn_input()
            if ssn != 0:
                first_name = str(input("Enter first name: "))
                last_name = str(input("Enter last name: "))
                if bank.change_customer_name(first_name + " " + last_name, ssn):
                    print("Customer with SSN {} has been updated.".format(ssn))
                else:
                    print("No customer found with SSN {}.".format(ssn))


        #Delete customer
        elif choice == 5:
            ssn = ssn_input()
            if ssn != 0:
                returned_list = bank.remove_customer(ssn)
                if returned_list:
                    print("\nCustomer with SSN {} has been deleted.".format(ssn))
                    if len(returned_list) == 3:
                        print("\nDeleted accounts:")
                        print(returned_list[0])
                        print(returned_list[1])
                    elif len(returned_list) == 2:
                        print("\nDeleted accounts:")
                        print(returned_list[0])
                    print("\n${} has been refunded.".format(returned_list[-1]))
                else:
                    print("No customer found with SSN {}.".format(ssn))


        #Add account to existing customer
        if choice == 6:
            ssn = ssn_input()
            if ssn != 0:
                acc_num = bank.add_account(ssn)
                if acc_num != -1:
                    print("Account created with account number {}.".format(acc_num))
                else:
                    print("This customer has two accounts".format(ssn))


        #Close account
        elif choice == 7:
            ssn = ssn_input()
            if ssn != 0:
                if display_customer_accounts(ssn):
                    acc_num = acc_num_input()
                    if acc_num != 0:
                        print(bank.close_account(ssn, acc_num))


        #Withdraw/Deposit
        if choice == 8:
            print("""
                        1. Withdraw from chosen account.
                        2. Deposit to chosen account.
                        3. Main menu.
                        """)
            try:
                w_d_choice = int(input("Choose One Of The Options: "))
                if len(str(w_d_choice)) != 1:
                    print("Please choose between 1 and 3")
            except ValueError:
                print("Invalid choice")

            #Withdraw/Deposit
            if w_d_choice == 3:
                return menu()
            elif w_d_choice == 1 or 2:
                ssn = ssn_input()
                if ssn != 0:
                    if display_customer_accounts(ssn):
                        acc_num = acc_num_input()
                        if acc_num != 0:
                            try:
                                amount = float(input("Enter amount: "))
                                if amount > 0:
                                    if w_d_choice == 1:
                                        if bank.withdraw(ssn, acc_num, amount):
                                            print("\n${} withdrawn from account {}.".format(amount, acc_num))
                                        else:
                                            print("\nWithdrawal declined.")
                                    else:
                                        if bank.deposit(ssn, acc_num, amount):
                                            print("\n${} deposited to account {}.".format(amount, acc_num))
                                        else:
                                            print("\nDeposit declined.")
                                else:
                                    print("You can only withdraw/deposit a positive amount.")

                            except ValueError:
                                print("Enter numbers only.")
        #Exit
        elif choice == 9:
            print("\nPress 'Enter' To Exit ...")
            exit()

#Display customer accounts
def display_customer_accounts(ssn):
    returned_acc_info = bank.get_all_acc(ssn)
    if returned_acc_info:
        print("Available accounts:")
        for x in returned_acc_info:
            print(x)
    else:
        print("No available accounts for customer with SSN {}.".format(ssn))
        return False
    return True

#input ssn
def ssn_input():
    try:
        ssn = int(input("\nEnter SSN (8 digits): "))
        if len(str(ssn)) != 8:
            print("You need to enter SSN with 8 digits (you entered {}).".format(len(str(ssn))))
            return 0
        return ssn
    except ValueError:
        print("SSN can only contain numbers.")
    return 0

#Get account number input from user
def acc_num_input():
    try:
        acc_num = int(input("Enter account number (4 digits): "))
        if len(str(acc_num)) != 4:
            print("You need to enter account number with 4 digits (you entered {}).".format(len(str(acc_num))))
            return 0
        return acc_num
    except ValueError:
        print("Account number can only contain numbers.")
    return 0

if __name__ == "__main__":
    menu()


























