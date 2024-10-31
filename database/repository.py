import sqlite3

from database import DB_NAME


class Repository:
    def __init__(self, database):
        if database is None:
            database = DB_NAME
        self.database = database
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
