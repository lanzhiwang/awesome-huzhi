class Account(object):
    num_accounts = 0

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        Account.num_accounts += 1

    def __del__(self):
        Account.num_accounts -= 1

    def deposit(self, amt):
        self.balance = self.balance + amt

    def withdraw(self, amt):
        self.balance = self.balance - amt

    def inquiry(self):
        return self.balance


a = Account("Guido", 1000.00)  # Account.__init__(a, "Guido", 1000.00)
print("dir(Account):", dir(Account))
print("dir(a):", dir(a))

a.deposit(100.00)  # Account.deposit(a, 100.00)
print(a.inquiry())

name = a.name
deposit = a.deposit
print(name)
print(deposit)

deposit(200.00)
print(a.inquiry())

Account.deposit(a, 300.00)
print(Account.deposit)
print(a.inquiry())

# b = None
# Account.__init__(b, "Bill", 10.00)
# print(b.inquiry())
