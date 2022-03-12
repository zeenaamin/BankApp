class Account:

    def __init__(self, user_id, acc_num, acc_type, balance):
        self.user_id = user_id
        self.acc_num = acc_num
        self.acc_type = acc_type
        self.balance = balance

    def __str__(self):
        return "\nCustomer: " + str(self.user_id) + "\nAccount number: " + str(self.acc_num) + "\nAccount type: " + self.acc_type + "\nBalance: " + str(self.balance)
