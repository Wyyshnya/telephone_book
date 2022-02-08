import mariadb


class DataBase:
    def __init__(self):
        try:
            self.conn = mariadb.connect(user="root", password="1337", host="127.0.0.1", port=3306, database="test_ex")
            self.cursor = self.conn.cursor()
            self.conn.autocommit = True
        except mariadb.Error as e:
            print(f"Error connecting: {e}")

    def __exit__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Соединение с Mariadb закрыто")

    def create_users(self):
        self.cursor.execute("Create Table users (id int Primary Key AUTO_INCREMENT, username varchar(255) Not Null, "
                            "password varchar(255) Not NULL,"
                            "data_birth varchar(255));")
        self.conn.commit()

    def create_book(self):
        self.cursor.execute("Create Table book (id_user int references users(id), "
                            "fio varchar(255) NOT NULL, telephone varchar(255) NOT NULL,"
                            "data_birth varchar(255), id_char int, primary key(id_user, fio, telephone, data_birth));")
        self.conn.commit()

    def drop(self):
        self.cursor.execute("DROP table if exists book;")
        self.cursor.execute("DROP table if exists users;")


# a = DataBase()
# a.drop()
# a.create_users()
# a.create_book()
