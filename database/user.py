from database.repository import Repository


class UserRepository(Repository):
    def __init__(self, database=None, table_name='users'):
        super().__init__(database)
        self.table_name = table_name
        super().create_table(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    age INTEGER NOT NULL,
                                    balance INTEGER NOT NULL
                                    )'''
                             )

    def add_user(self, user_id, username, email, age, balance=1000):
        self.cursor.execute(
            f"INSERT INTO {self.table_name} (id, username, email, age, balance) "
            f"VALUES ('{user_id}', '{username}', '{email}', '{age}', '{balance}')")
        self.connection.commit()

    def user_exists(self, user_id, username) -> bool:
        if user_id is not None:
            return bool(self.get_by_id(user_id))
        elif username is not None:
            return bool(self.get_by_username(username))
        return False

    def get_by_username(self, username):
        return self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE username = "{username}"').fetchone()

    def get_by_id(self, user_id):
        return self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = "{user_id}"').fetchone()
