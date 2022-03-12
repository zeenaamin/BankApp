class DataSource:

    file_customers = "customer.txt"
#Method to ensure that the connection is established to the datasource
    def datasource_conn(self):
        try:
            f = open(self.file_customers)
            ds = (True, "Connection successful", self.file_customers)

        except:
            ds = (False, "Connection faild", self.file_customers)
        finally:
            f.close(self.file_customers)

        return ds

    #Get all rows from the customer file and returns the list with saparated values
    def get_all_customers(self):
        data = []

        try:
            f = open(self.file_customers, "r")
            for x in f:
                row = x.strip().split(":")
                data.append(row)
        finally:
            f.close()

        return data

    #Get the highest id from the customer file
    def get_last_id(self):
        id = []

        try:
            f = open(self.file_customers, "r")
            for x in f:
                row = x.strip().split(":")
                id.append(row[0])
            last_id = id[-1]
        finally:
            f.close()

        return last_id

    #Adding new row to the customers file
    def add_row_customers(self, id, name, ssn):
        new_row = str(id) + ":" + name + ":" + str(ssn)

        try:
            f = open(self.file_customers, "a")
            f.write("\n" + new_row)
        finally:
            f.close()

    #Updating customer name
    def update_row_name(self, name, ssn):
        f = open(self.file_customers, "r")
        rows = f.readlines()
        f.close()

        for row in rows:
            if str(ssn) in row:
                index = rows.index(row)
                full_name = row.split(":")[1]
                new_row = row.replace(full_name, name)
                rows[index] = new_row

        f = open(self.file_customers, "w")
        f.writelines(rows)
        f.close()

    #Add account in customers file
    def update_row_acc(self, account, ssn):
        f = open(self.file_customers, "r")
        rows = f.readlines()
        f.close()

        for row in rows:
            if str(ssn) in row:
                index = rows.index(row)
                rows[index] = row.rstrip("\n")
                rows[index] = rows[index] + account

        f = open(self.file_customers, "w")
        f.writelines(rows)
        f.close()

    #Remove row form the customer file
    def remove_row(self, ssn):
        f = open(self.file_customers, "r")
        rows = f.readlines()
        f.close()

        for row in rows:
            if str(ssn) in row:
                index = rows.index(row)
                del rows[index]

        rows[len(rows) - 1] = rows[len(rows) - 1].rstrip("\n")

        f = open(self.file_customers, "w")
        f.writelines(rows)
        f.close()

    #Remove account from the customer file
    def remove_row_acc(self, acc_num):
        f = open(self.file_customers, "r")
        rows = f.readlines()
        f.close()

        for row in rows:
            if str(acc_num) in row:
                index = rows.index(row)
                if "#" in row:
                    customer_info = row.strip().split("#")[0].split(":")[:3]
                    first_acc = row.strip().split("#")[0].split(":")[3:]
                    second_acc = row.strip().split("#")[1].split(":")

                    new_row_customer = customer_info[0] + ":" + customer_info[1] + ":" + customer_info[2]

                    if str(acc_num) not in first_acc:
                        new_row_acc = ":" + first_acc[0] + ":" + first_acc[1] + ":" + first_acc[2]
                    else:
                        new_row_acc = ":" + second_acc[0] + ":" + second_acc[1] + ":" + second_acc[2]
                    new_row = new_row_customer + new_row_acc

                else:
                    customer_info = row.strip().split(":")[:3]
                    new_row = customer_info[0] + ":" + customer_info[1] + ":" + customer_info[2]

                if row != rows[-1]:
                    new_row += "\n"

                rows[index] = new_row
                f = open(self.file_customers, "w")
                f.writelines(rows)
                f.close()
                return True
        return False




