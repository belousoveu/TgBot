from database.repository import Repository


class ProductRepository(Repository):
    def __init__(self, database=None, table_name='products'):
        super().__init__(database)
        self.table_name = table_name
        super().create_table(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    description TEXT,
                                    picture BLOB,
                                    price INTEGER NOT NULL
                                )'''
                             )

    def get_all(self):
        return self.cursor.execute(f'SELECT * FROM {self.table_name}').fetchall()
