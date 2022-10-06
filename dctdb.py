import sqlite3
from dataclasses import dataclass, fields
import builtins


class dctdb:

    def __init__(self, dc: dataclass, conn):
        self.dc = dc
        self.conn = conn
        self.create_table()

    def create_table(self):
        CREATE_COMMAND = "CREATE TABLE IF NOT EXISTS "

        _create_command = self.dc.__name__ + '(id integer PRIMARY KEY AUTOINCREMENT, '

        for field in fields(self.dc):
            match field.type:
                case builtins.int:
                    _create_command += field.name + " integer, "

                case builtins.str:
                    _create_command += field.name + " text, "

                case builtins.bool:
                    _create_command += field.name + " boolean, "

                case builtins.bytes:
                    _create_command += field.name + " binary, "

                case _:
                    print(field.type)
                    exit(-1)

        _create_command = _create_command[:-2]

        CREATE_COMMAND += _create_command + ");"

        c = self.conn.cursor()
        c.execute(CREATE_COMMAND)
        return True

    def add_to_table(self, instance_of_dc):
        INSERT_COMMAND = "INSERT INTO " + self.dc.__name__ + "("

        _insert_command = ','.join(field.name for field in fields(self.dc))

        INSERT_COMMAND += _insert_command + ") VALUES (" + ("?,"*len(fields(instance_of_dc)))[:-1] + ")"

        c = self.conn.cursor()
        tup = tuple(getattr(instance_of_dc, field.name) for field in fields(instance_of_dc))
        c.execute(INSERT_COMMAND, tup)
        self.conn.commit()
        return True

    def fetch_all_from_table(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM " + self.dc.__name__)

        rows = cur.fetchall()
        toRet = []
        for row in rows:
            args = []
            for item, item_type in zip(row[1:], [field.type for field in fields(self.dc)]):
                args.append(item_type(item))
            toRet.append(self.dc(*args))

        return toRet

    def update(self, instance_of_dc, find_by_field_name):
        UPDATE_COMMAND = "UPDATE " +self.dc.__name__ + " SET "
        _update_command = ''.join(f"{field.name} = ?, " for field in fields(self.dc))[:-2]
        UPDATE_COMMAND += _update_command + f" WHERE {find_by_field_name} = ?"
        c = self.conn.cursor()
        tup = tuple(getattr(instance_of_dc, field.name) for field in fields(instance_of_dc)) + (getattr(instance_of_dc, find_by_field_name),)

        c.execute(UPDATE_COMMAND, tup)
        self.conn.commit()


    def delete(self, instance_of_dc):
        DELETE_COMMAND = "DELETE FROM " +self.dc.__name__ +" WHERE "
        _delete_command = ''.join(f"{field.name} = ? AND " for field in fields(self.dc))[:-5]

        DELETE_COMMAND += _delete_command + ";"
        print(DELETE_COMMAND)

        c = self.conn.cursor()
        tup = tuple(getattr(instance_of_dc, field.name) for field in fields(instance_of_dc))

        c.execute(DELETE_COMMAND, tup)
        self.conn.commit()


@dataclass
class Torrent:
    name: str
    size: str
    seeders: int  # amount of seeders
    leechers: int  # amount of leechers

    download_speed: int  # MAXIMUM download speed in Bytes
    upload_speed: int  # MAXIMUM upload speed in Bytes
    is_start_announced: bool  # if the torrent was already announced.
    announce_url: str  # Where we will announce torrent
    info_hash: bytes  # Data of torrent to announce

    time_to_announce: int  # How much seconds until we will announce the torrent

    client_id: int  # the id of the client. The reason we save the id and not a reference to the object is because it
    # is easier to both save and load, and neither the client or torrent has functions that work on each other

    downloaded: int  # amount of downloaded data
    uploaded: int  # amount of uploaded data

    temp_taken_download: int  # Temp var to hold how much download bandwidth we took from client to the current second
    temp_taken_upload: int  # Temp var to hold how much upload bandwidth we took from client to the current second


@dataclass
class Client:
    rand_id: str  # Random ID constructed from 12 random chars
    client_name: str  # How client will be represented to the user
    user_agent: str  # The user agent that will report to the tracker
    port: int  # The port where we will report data
    upload_limit: int  # Limit in Bytes at how much client can upload
    download_limit: int  # Limit in Bytes at how much client can upload
    available_upload: int  # How much upload bandwidth is available in Bytes
    available_download: int  # How much upload bandwidth is available in Bytes
    peer_id: str  # A peer ID which is originated in the ORIGINAL torrent client. example for one: -AZ3020-


def create_connection(db_file):
    return sqlite3.connect(db_file)

    return conn


if __name__ == '__main__':
    uri = "db.db"
    conn = create_connection(uri)
    test = dctdb(Torrent, conn)
    print(test.fetch_all_from_table())
