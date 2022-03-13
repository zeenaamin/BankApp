from datasource import Datasource
from customer import Customer
from account import Account

class Bank:

    ds = Datasource()
    customers = []
    accounts = []

    def _load(self):
        self.customer = self.ds.get_all_customers()
        self._load_customers()
        self._load_accounts()

    #Load all customers
    def _load_customers(self):
        for x in self.customer:
            try:
                customer = Customer(int(x[0]), x[1].split()[0], x[1].split()[1], int(x[2]))
                self.customers.append(customer)
            except:
                print("Error while loading{}.".format(x))

    # Load all accounts
    def _load_accounts(self):
        account_details = {}

        for x in self.customer:
            account_details[x[0]] = x[3:]

        for x, y in account_details.items():
            if len(y) > 3:
                first_account = Account(int(x), int(y[0]), y[1], float(y[2].split("#")[0]))
                second_account = Account(int(x), int(y[2].split("#")[1]), y[3], float(y[4]))
                self.accounts.append(first_account)
                self.accounts.append(second_account)
            elif len(y) == 3:
                first_account = Account(int(x), int(y[0]), y[1], float(y[2]))
                self.accounts.append(first_account)

            else:
                pass

    #Add new customer
    def add_customer(self,first_name,last_name,ssn):

        for customer in self.customer:
            if str(ssn) in customer:
                return False

        customer_id = int(self.ds.get_last_id())+1
        name = first_name + " " + last_name
        self.customer.append([customer_id, name, ssn])
        self.customers.append(Customer(customer_id,first_name, last_name, ssn))
        self.ds.add_row_customers(customer_id, name, ssn)
        return True

    #Add account for a specific customer
    def add_account(self, ssn):
        account_temp = []
        acc_num = self.get_new_acc_num()
        acc_type = "debit account"
        acc_balance = 0.0

        for x in self.customers:
            if ssn == x.ssn:
                for y in self.accounts:
                    if x.id == y.user_id:
                        account_temp.append(y)

                if len(account_temp) == 2:
                    return -1

                elif len(account_temp) == 1:
                    acc_row = "#" + str(acc_num) + ":" + acc_type + ":" + str(acc_balance) + "\n"
                    new_acc = Account(x.id, acc_num, acc_type, acc_balance)
                    self.accounts.append(new_acc)
                    self.ds.update_row_acc(acc_row,ssn)
                    return acc_num
                else:
                    acc_row = ":" + str(acc_num) + ":" + acc_type + ":" + str(acc_balance) + "\n"
                    new_acc = Account(x.id, acc_num, acc_type, acc_balance)
                    self.accounts.append(new_acc)
                    self.ds.update_row_acc(acc_row, ssn)
                    return acc_num
        return -1

    #Uppdate customer's name
    def change_customer_name(self, name, ssn):
        for x in self.customers:
            if ssn == x.ssn:
                x.first_name = name.split()[0]
                x.last_name = name.split()[1]
                self.ds.update_row_name(name, ssn)
                self.customer = self.ds.get_all_customers()
                return True
        return False

    #Delete customer
    def remove_customer(self, ssn):
        returned_balance = 0.0
        to_remove = []
        to_return = []

        for x in self.customer:
            if ssn == x.ssn:
                index = self.customers.index(x)
                self.customers.pop(index)

                for y in self.accounts:
                    if x.id == y.user_id:
                        to_return.append(y)
                        to_remove.append(self.accounts.index(y))
                        returned_balance += y.balance

                for r in reversed(to_remove):
                    self.accounts.pop(r)

                self.ds.remove_row(ssn)
                self.customer = self.ds.get_all_customers()

                to_return.append(returned_balance)
        return to_return

    #Return cusyomer
    def get_customer(self, ssn):
        returned_list = []

        for x in self.customers:
            if ssn == x.ssn:
                returned_list.append(x.first_name + " " + x.last_name)
                returned_list.append(x.ssn)

                for y in self.accounts:
                    if x.id == y.user_id:
                        account = "Account number: " + str(y.acc_num) + ", Balance: " + str(y.balance)
                        returned_list.append(account)

                return returned_list

        return "\nNo customer with SSN{} was found.".format(ssn)

    #Return account
    def get_account(self, ssn, acc_num):
        for x in self.customers:
            if ssn == x.ssn:
                for y in self.accounts:
                    if acc_num == y.acc_num and x.id == y.user_id:
                        return "\nAccount number: {}\nAccount type: {}\nBalance: {}".format(acc_num, y.acc_type, y.balance )
                return "\nAccount number {} was not found.".format(acc_num)
        return "\nNo customer found with SSN {}".format(ssn)

    #Delete account
    def close_account(self, ssn, acc_num):
        to_remove = []
        returned_balance = 0.0

        for x in self.customers:
            if ssn == x.ssn:
                for y in self.accounts:
                    if acc_num == y.acc_num and x.id == y.user_id:
                        returned_balance = y.balance
                        to_remove.append(self.accounts.index(y))
                if not to_remove:
                    return "\nNo account found with account number {}.".format(acc_num)
                else:
                    for r in to_remove:
                        if self.ds.remove_row_acc(acc_num):
                            self.accounts.pop(r)
                            return "\nAccount closed. ${} refunded.".format(returned_balance)
                        else:
                            return "\nAccount could not be removed. Please contact customer service for further assistance."
        return "\nNo customer found with SSN {}".format(ssn)


    # Deposit to chosen account
    def deposit(self, ssn, acc_num, amount):
        for x in self.customers:
            if ssn == x.ssn:
                for y in self.accounts:
                    if acc_num == y.acc_num and x.id == y.user_id:
                        y.balance += amount
                        self.ds.update_row_balance(acc_num, amount)
                        return True
        return False

    # Withdraw from chosen account
    def withdraw(self, ssn, acc_num, amount):
        for x in self.customers:
            if ssn == x.ssn:
                for y in self.accounts:
                    if acc_num == y.acc_num and x.id == y.user_id:
                        if y.balance >= amount:
                            y.balance -= amount
                            self.ds.update_row_balance(acc_num, amount * -1)

                            return True
        return False

    # Generate new account number
    def get_new_acc_num(self):
        acc_numbers = []
        max_num = 0

        for x in self.accounts:
            acc_numbers.append(x.acc_num)

        for i in acc_numbers:
            if int(i) > max_num:
                max_num = int(i)

        return max_num + 1

    # Return all accounts from specific customer
    def get_all_acc(self, ssn):
        returned_acc_info = []

        for x in self.customers:
            if ssn == x.ssn:
                for y in self.accounts:
                    if x.id == y.user_id:
                        acc_info = "Account number: " + str(y.acc_num) + ", Balance: " + str(y.balance)
                        returned_acc_info.append(acc_info)
        return returned_acc_info
























