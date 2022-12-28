from dataclasses import dataclass, make_dataclass, fields
import datetime
from dctodb import dctodb
from typing import List, Type


def create_class(parent_class_name, item_type: Type):
    cls_name = parent_class_name + item_type.__name__ + "List"
    return make_dataclass(cls_name,
                          [('item_val', item_type), ('index',int,0)])


lis = list[int]

int_lis_dc = create_class("list", int)
print(fields(int_lis_dc(4)))





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