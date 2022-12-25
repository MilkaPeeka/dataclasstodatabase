from dataclasses import dataclass
from dctodb import dctodb

@dataclass
class Client:
    name: str
    index: int = 0

@dataclass
class Test:
    name: str
    age: int
    is_adult: bool
    client: Client
    index: int = 0



if __name__ == "__main__":
    # client_db = dctodb(Client, "client.db", None, {"nameindex": str})
    test_db = dctodb(Test, "test_db.db")
    print(test_db.fetch_all())

    # client = Client("Another Client Lol")
    # test2 = Test("Another test Test", 20, False, client)

    # test_db.insert(test2)
    # test_db = dctodb(Test, [("age", 69)], uri)
    # test_obj3 = Test("Daniel", 19, True)
    #
    # test_db.insert(test_obj3)
    #
    # # now db contains all three objects
    # pr = test_db.fetch_all()
    # print(pr)
    # will contain a list of objects
    #
    # test_db.delete(test_obj)
    # # now db contains all objects except of first one
    #
    # test_obj2.age = 14
    # test_obj2.is_adult = True
    # test_db.update("name", test_obj2)
    # # now test_obj2 is updated to new values
