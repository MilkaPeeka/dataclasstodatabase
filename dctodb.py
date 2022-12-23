import sqlite3
from dataclasses import fields
import builtins
from typing import Type, Any, List, Dict
import datetime


def _create_connection(db_filename):
    return sqlite3.connect(db_filename)


class dctodb:
    def create_sub_table(self):
            # we will iterate over each item in dcs we have and create a table accordingly, attaching our id
            for dc_in_class in self.dcs_in_class:
                # we will need to create a table to each, with extra column that is the id of self.
                self.dc_in_class_mappings[dc_in_class] = dctodb(dc_in_class, self.db_filename, None, {self.dc.__name__ + "index": int})


    def __init__(self, dc: Type[Any], db_filename: str, dcs_in_class: List[Type[Any]] = None, extra_columns: Dict[str, Any] = None):
        self.dc: Type[Any] = dc
        self.db_filename: str = db_filename
        # self.dc_in_class_mappings = None
        # if dcs_in_class:
        #     self.dc_in_class_mappings = dict()
        #     self.create_sub_table()

        # print(self.dc_in_class_mappings)
        self.create_table()

    def create_table(self):
        command = f"CREATE TABLE IF NOT EXISTS {self.dc.__name__} (id integer PRIMARY KEY AUTOINCREMENT, "

        for field in fields(self.dc):
            if field.name == 'index':
                continue

            match field.type:
                case builtins.int:
                    command += f"{field.name} integer, "

                case builtins.str:
                    command += f"{field.name} text, "

                case builtins.bool:
                    command += f"{field.name} boolean, "

                case builtins.bytes:
                    command += f"{field.name} binary, "

                case datetime.datetime:
                    command += f"{field.name} smalldatetime, "

                case builtins.float:
                    command += f"{field.name} float, "

                case _:
                    # here we will match all classes
                    # if field.type == self.dc_in_class[0]:
                    #     print ('hey my name is kimkwest')
                    # else:
                    raise Exception(f"unsupported data type: {field.type}")

        command = command[:-2]  # removing ', ' from command
        command += ");"  # closing the command
        conn = _create_connection(self.db_filename)
        cur = conn.cursor()
        print(command)
        cur.execute(command)
        conn.close()

    def insert(self, *instances_of_dc):
        var_names = [field.name for field in fields(self.dc) if field.name != 'index']
        command = f"INSERT INTO {self.dc.__name__} ({','.join(var_names)}) VALUES ({'?,' * len(var_names)}"
        command = command[:-1]  # strip ','
        command += ")"

        val_list = [tuple(getattr(instance, var_name) for var_name in var_names) for instance in instances_of_dc]

        conn = _create_connection(self.db_filename)
        cur = conn.cursor()
        cur.executemany(command, val_list)
        conn.commit()
        conn.close()

    def fetch_all(self):
        conn = _create_connection(self.db_filename)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.dc.__name__}")
        rows = cur.fetchall()
        conn.close()

        fetched = []
        # for each row we will iterate over every column and make sure the correct type in inserted

        for row in rows:
            args = []
            
            row = list(row)
            row.append(row.pop(0))  # moving the 'id' side to match the args of dc
            print(row)
            for field, col in zip(fields(self.dc), row):
                if field.type == datetime.datetime:
                    col = col.split('.')[0]
                    col = datetime.datetime.strptime(col, '%Y-%m-%d %H:%M:%S')
                else:
                    col = field.type(col)

                args.append(col)
            
            fetched.append(self.dc(*args))

        return fetched

    def update(self, find_by_field, *instances_of_dc):
        var_names = [field.name for field in fields(self.dc) if field.name != 'index']
        command = f"UPDATE {self.dc.__name__} SET {''.join(f'{name} = ?,' for name in var_names)}"
        command = command[:-1]  # remove ','

        command += f" WHERE {find_by_field} = ?"

        # arg_list contains a tuple of values of all objects data to update COMBINED with the key
        arg_list = []
        for instance in instances_of_dc:
            vals = tuple(getattr(instance, field.name) for field in fields(self.dc))
            find_by = (getattr(instance, find_by_field),)

            arg_list.append(vals + find_by)

        conn = _create_connection(self.db_filename)
        c = conn.cursor()
        c.executemany(command, arg_list)
        conn.commit()
        conn.close()

    def delete(self, *instances_of_dc):
        var_names = [field.name for field in fields(self.dc) if field.name != 'index']
        command = f"DELETE FROM {self.dc.__name__} WHERE {''.join(f'{name} = ? AND ' for name in var_names)}"
        command = command[:-4]  # remove '? AND' from query

        # a list of the tuples containing the value of all objects we want to remove
        val_list = [tuple(getattr(instance, var_name) for var_name in var_names) for instance in instances_of_dc]
        conn = _create_connection(self.db_filename)
        c = conn.cursor()
        c.executemany(command, val_list)
        conn.commit()
        conn.close()
