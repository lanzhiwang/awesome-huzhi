import random


class Account(object):
    num_accounts = 0

    def __init__(self, name, balance):
        print("Account, __init__")
        self.name = name
        self.balance = balance
        Account.num_accounts += 1

    def __del__(self):
        print("Account __del__")
        Account.num_accounts -= 1

    def deposit(self, amt):
        print("Account deposit")
        self.balance = self.balance + amt

    def withdraw(self, amt):
        print("Account withdraw")
        self.balance = self.balance - amt

    def inquiry(self):
        print("Account inquiry")
        return self.balance


class EvilAccount(Account):
    def __init__(self, name, balance, evilfactor):
        print("EvilAccount __init__")
        Account.__init__(self, name, balance)
        self.evilfactor = evilfactor

    def inquiry(self):
        print("EvilAccount inquiry")
        if random.randint(0, 4) == 1:
            return self.balance * self.evilfactor
        else:
            return self.balance


class DepositCharge(object):
    fee = 5.00

    def deposit_fee(self):
        print("DepositCharge deposit_fee")
        print("DepositCharge fee:", self.fee)
        self.withdraw(self.fee)


class WithdrawCharge(object):
    fee = 2.50

    def withdraw_fee(self):
        print("WithdrawCharge withdraw_fee")
        print("WithdrawCharge fee:", self.fee)
        self.withdraw(self.fee)


class MostEvilAccount(EvilAccount, DepositCharge, WithdrawCharge):
    def deposit(self, amt):
        print("MostEvilAccount deposit")
        self.deposit_fee()
        super(MostEvilAccount, self).deposit(amt)

    def withdraw(self, amt):
        print("MostEvilAccount withdraw")
        self.withdraw_fee()
        super(MostEvilAccount, self).withdraw(amt)


print(MostEvilAccount.__mro__)
"""
(
    <class '__main__.MostEvilAccount'>,
    <class '__main__.EvilAccount'>,
    <class '__main__.Account'>,
    <class '__main__.DepositCharge'>,
    <class '__main__.WithdrawCharge'>,
    <class 'object'>
)
"""
d = MostEvilAccount("Dave", 500.00, 1.00)

print("MostEvilAccount.__dict__:", MostEvilAccount.__dict__)
print("d.__dict__:", d.__dict__)
# MostEvilAccount.__dict__: {
#     '__module__': '__main__',
#     '__firstlineno__': 62,
#     'deposit': <function MostEvilAccount.deposit at 0x7f8c1af9a700>,
#     'withdraw': <function MostEvilAccount.withdraw at 0x7f8c1af9a7a0>,
#     '__static_attributes__': (),
#     '__doc__': None
# }
# d.__dict__: {
#     'name': 'Dave',
#     'balance': 500.0,
#     'evilfactor': 1.0
# }
