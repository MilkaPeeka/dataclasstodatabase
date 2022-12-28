import sqlite3
from dataclasses import fields, is_dataclass, make_dataclass
import builtins
from typing import Type, Any, Dict, Tuple, Union, List
import datetime


def _create_connection(db_filename) -> sqlite3.Connection:
    return sqlite3.connect(db_filename)


def _split_fields(dc) -> Tuple[List[Any]]:
    basic_fields = []
    dc_fields = []
    list_fields = []
    for field in fields(dc):
        if is_dataclass(field.type):
            dc_fields.append(field)

        elif isinstance(field.type, list):
            list_fields.append(field)

        else:
            basic_fields.append(field)

    return basic_fields, dc_fields, list_fields


def _sql_represent(name, type) -> str:
    match type:
        case builtins.int:
            return f"{name} integer"

        case builtins.str:
            return f"{name} text"

        case builtins.bool:
            return f"{name} boolean"

        case builtins.bytes:
            return f"{name} binary"

        case datetime.datetime:
            return f"{name} smalldatetime"

        case builtins.float:
            return f"{name} float"

        case _:
            raise Exception(f"Unrecognized type: {type}")


"""
helper class to store lists
"""


def create_class(parent_class_name, item_type: Type):
    cls_name = parent_class_name + item_type.__name__ + "List"
    return make_dataclass(cls_name,
                          [('item_val', item_type), ('index',int,0)])

class dctodb:
    def __init__(self, dc: Type[Any], db_filename: str, extra_columns: Dict[str, Any] = dict()):
        self.dc: Type[Any] = dc
        self.db_filename: str = db_filename
        self.extra_columns = extra_columns  # won't be returned inside an object but in a dict next to the object
        self.basic_fields, self.dcs_fields, self.list_fields = _split_fields(
            self.dc)  # only fields that are not dcs or lists
        self.dc_in_class_mappings = dict()
        self.lists_in_class_mappings = dict()
        self._create_sub_conn()

        self.create_table()

    @property
    def table_name(self) -> str:
        return self.dc.__name__

    # a way for our childs to recognize us
    @property
    def identifier(self) -> str:
        return self.dc.__name__ + "index"

    def _execute(self, command, args=None):
        conn = _create_connection(self.db_filename)
        cur = conn.cursor()
        if args:
            res = cur.execute(command, args)
        else:
            res = cur.execute(command)

        return res, conn

    def create_table(self):
        command = "CREATE TABLE IF NOT EXISTS {} (id integer PRIMARY KEY AUTOINCREMENT, {});"
        # might remove index from basic_fields but unsure
        args = [_sql_represent(field.name, field.type) for field in self.basic_fields if field.name != 'index'] + [
            _sql_represent(col_name, col_type) for col_name, col_type in self.extra_columns.items()]
        args = ', '.join(args)
        command = command.format(self.table_name, args)
        _, conn = self._execute(command)
        conn.close()

    def _get_count(self) -> int:
        res, conn = self._execute(f"SELECT COUNT(*) FROM {self.dc.__name__}")
        res = res.fetchone()[0]
        conn.close()
        return res

    def _create_sub_conn(self):
        """
        Essentially, Before we insert self, we need to create sub-connections to every complicated object we need to store, like sub-dataclasses and lists.
        That connection is creating connection to our sub-dataclasses, however we create extra columns that are not part of the object but rather an identifier to their parent class

        NEED TO ADD SUPPORT FOR: LIST

        """
        for list_in_class in self.list_fields:
            self.lists_in_class_mappings[list_in_class] = dctodb()
        for dc_in_class in dcs_or_classes_in_class:
            self.dc_in_class_mappings[dc_in_class] = dctodb(dc_in_class.type, self.db_filename, {self.identifier: int})

    def _insert_list(self):
        pass

    def _insert_dcs(self, instance):
        sub_dcs = filter(lambda x: is_dataclass(x.type), self.possible_dcs_or_lists)
        for field in sub_dcs:
            instance_dc_value = getattr(instance, field.name)
            self.dc_in_class_mappings[field].insert_one(instance_dc_value, {self.identifier: instance.index})

    def insert_many(self, *instances):
        """
        Mega function that consists of multiple child functions.
        1. We will insert our dataclasses and lists
        2. We will insert ourselves, MEANWHILE updating our indexes as fitted in the db itself.
        
        """

    def insert_one(self, instance, extra_columns: Dict[str, Any] = dict()):
        """
        A potentially mega function, we want that function to insert one item (and update its value). if it has extra columns, obviously we need to insert them as well.
        Extra columns is a dict: {col_name: col_value}
        After we updated our own index, we can proceed to enter fields like dcs and lists
        """

        command = "INSERT INTO {} ({}) VALUES ({});"
        # Remember, we will need to handle dataclasses and lists seperatley so we exclude them from now
        variable_names = [field.name for field in self.basic_fields if field.name != "index"]
        variable_values = [getattr(instance, field_name) for field_name in variable_names]
        for col_name, col_value in extra_columns.items():
            variable_names.append(col_name)
            variable_values.append(col_value)

        command = command.format(self.table_name, ', '.join(variable_names), ','.join(['?'] * len(variable_names)))
        _, conn = self._execute(command, variable_values)
        res = conn.commit()
        instance.index = self._get_count()

        conn.close()

        if self.dc_in_class_mappings:
            self._insert_dcs(instance)

    def _fetch_lists_from_subtable(self):
        return dict()

    def fetch_where(self, condition) -> List[Tuple[Any, Union[Dict, None]]]:
        """
        A cute function that returns a list where condition is met.
        condition looks like that:
        FIELD_NAME OPERATOR VALUE

        We will have to make sure that we also fetch sub-classes \ lists if there are any
        
        Each row will be dismantled into columns and we will put the columns as needed in args and then return
        If there are extra_columns, than we return it in a seperate dict
        """
        fetched = []

        command = "SELECT * FROM {} WHERE {};"
        command = command.format(self.table_name, condition)
        res, conn = self._execute(command)
        rows = res.fetchall()
        conn.close()

        for row in rows:
            index = row[0]
            basic_args = row[1:]
            child_dc_values = self._fetch_dcs_from_sub_table(index)
            list_values = self._fetch_lists_from_subtable()

            item = self._build_item_from_values(index, basic_args, child_dc_values, list_values)
            fetched.append(item)

        return fetched

    def _build_item_from_values(self, index, basic_args, child_dc_values: Dict = dict(),
                                child_lists_values: Dict = dict()):
        """
        We'll iterate over each value and append it into an args and then create an object through it
        """

        basic_args = list(basic_args)
        args = []
        for field in fields(self.dc):
            if field in child_dc_values:
                args.append(child_dc_values[field])
                continue

            if field in child_lists_values:
                args.append(child_dc_values[field])
                continue

            if field.name == "index":
                args.append(int(index))
                continue

            if field.type == datetime.datetime:
                date = basic_args.pop(0)
                date = date.split(".")[0]
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                args.append(date)
                continue

            args.append(field.type(basic_args.pop(0)))

        return self.dc(*args)

    def _fetch_dcs_from_sub_table(self, self_index) -> Dict:
        """
        We will fetch every sub-item using our self.index.
        Each field in our subclass is just one item, so it will always return only one item (one to one relationship)
        """
        dc_childs = dict()

        for dc_field, connector in self.dc_in_class_mappings.items():
            command = f'{self.identifier} == {self_index}'
            dc_childs[dc_field] = connector.fetch_where(command)[0]

        return dc_childs

    # def update(self, find_by_field, *instances_of_dc):
    #     var_names = [field.name for field in fields(self.dc) if field.name != "index"]
    #     command = f"UPDATE {self.dc.__name__} SET {''.join(f'{name} = ?,' for name in var_names)}"
    #     command = command[:-1]  # remove ','

    #     command += f" WHERE {find_by_field} = ?"

    #     # arg_list contains a tuple of values of all objects data to update COMBINED with the key
    #     arg_list = []
    #     for instance in instances_of_dc:
    #         vals = tuple(getattr(instance, field.name) for field in fields(self.dc))
    #         find_by = (getattr(instance, find_by_field),)

    #         arg_list.append(vals + find_by)

    #     conn = _create_connection(self.db_filename)
    #     c = conn.cursor()
    #     c.executemany(command, arg_list)
    #     conn.commit()
    #     conn.close()

    # def delete(self, *instances_of_dc):
    #     var_names = [field.name for field in fields(self.dc) if field.name != "index"]
    #     command = f"DELETE FROM {self.dc.__name__} WHERE {''.join(f'{name} = ? AND ' for name in var_names)}"
    #     command = command[:-4]  # remove '? AND' from query

    #     # a list of the tuples containing the value of all objects we want to remove
    #     val_list = [
    #         tuple(getattr(instance, var_name) for var_name in var_names)
    #         for instance in instances_of_dc
    #     ]
    #     conn = _create_connection(self.db_filename)
    #     c = conn.cursor()
    #     c.executemany(command, val_list)
    #     conn.commit()
    #     conn.close()
