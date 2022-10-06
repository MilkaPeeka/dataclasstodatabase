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

    # test_db.insert(test_obj3,test_obj1,test_obj2)

    pr = test_db.fetch_all()
    test_db.delete(test_obj)
