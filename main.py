from dataclasses import dataclass
from dctodb import dctodb

@dataclass
class Client:
    name: str
    index: int = 0

@dataclass
class Test:
    index: int
    name: str
    age: int
    is_adult: bool
    client: Client



if __name__ == "__main__":
    client_db = dctodb(Client, "client.db")
    client = Client("torrentdbclient", 1)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)
    client_db.insert(client)

    print(client_db.fetch_all())
    #test_db = dctodb(Test, "test_db.db", [Client])

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
