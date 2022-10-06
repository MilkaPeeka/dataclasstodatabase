from dataclasses import dataclass
from dctodb import dctodb


@dataclass
class Test:
    name: str
    age: int
    is_adult: bool


if __name__ == "__main__":
    uri = "test.db"
    test_db = dctodb(Test, uri)
    test_obj = Test("Nicki", 29, True)
    test_obj2 = Test("Roei", 1, False)
    test_obj3 = Test("Daniel", 19, True)

    test_db.insert(test_obj3, test_obj, test_obj2)
    # now db contains all three objects
    pr = test_db.fetch_all()
    # will contain a list of objects

    test_db.delete(test_obj)
    # now db contains all objects except of first one

    test_obj2.age = 14
    test_obj2.is_adult = True
    test_db.update("name", test_obj2)
    # now test_obj2 is updated to new values
