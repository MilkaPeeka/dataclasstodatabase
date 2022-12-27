from dataclasses import dataclass
import datetime
from dctodb import dctodb

@dataclass 
class sub_class:
    date: datetime.datetime
    index: int = 0

    
@dataclass
class mainClass:
    name: str
    age: int
    sub: sub_class

    index: int = 0

mainclass_db = dctodb(mainClass, "Test.db")
mainobj = mainClass("yuvi", 20, sub_class(datetime.datetime.now()))
# mainclass_db.insert_one(mainobj)
res = mainclass_db.fetch_where("id = 3")
# print(mainobj.index)
print(res)