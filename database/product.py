from database.repository import Repository


class ProductRepository(Repository):
    def __init__(self, database=None, table_name='products'):
        super().__init__(database)
        self.table_name = table_name
        self.create_table()

    def create_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                picture BLOB,
                price INTEGER NOT NULL
            )'''
        self.cursor.execute(sql)
        self.connection.commit()

    def get_all(self):
        return self.cursor.execute(f'SELECT * FROM {self.table_name}').fetchall()
