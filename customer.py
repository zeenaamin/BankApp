class Customer:

    def __init__(self, id, first_name, last_name, ssn):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn

    def __str__(self):
        return self.first_name + " " + self.last_name + " - " + str(self.ssn)