from dataclasses import dataclass
import datetime
from dctodb import dctodb
from typing import List

@dataclass
class BankPair:
    name: str
    value: int
    index: int = 0
@dataclass
class backAccounts:
    owner: str
    accounts: List[BankPair]
    index: int = 0

back_accounts_db = dctodb(backAccounts, "Test.db")

bank_account = backAccounts("Yuval", [BankPair("mainBank", 1243333), BankPair("secondAccount", 9938234), BankPair("secretBank", -9999)])
bank_account2 = backAccounts("Eyal", [BankPair("IDFBank", 8873453492), BankPair("MainBank", 93453859), BankPair("FraudBank", -9999)])

# back_accounts_db.insert_one(bank_account2)

print(back_accounts_db.fetch_where('id == 2'))


# @dataclass 
# class sub_class:
#     date: datetime.datetime
#     index: int = 0

    
# @dataclass
# class mainClass:
#     name: str
#     age: int
#     sub: sub_class

#     index: int = 0

# mainclass_db = dctodb(mainClass, "Test.db")
# mainobj = mainClass("yuvi", 20, sub_class(datetime.datetime.now()))
# # mainclass_db.insert_one(mainobj)
# res = mainclass_db.fetch_where("id = 3")
# # print(mainobj.index)
# print(res)