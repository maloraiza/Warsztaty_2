from mysql.connector import connect

from __initclc__ import password_hash
from __initclc__ import generate_salt


cnx = connect(user="root", password="root123", host="127.0.0.1", database="workshops2")
cursor = cnx.cursor()


class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO Users(username, email, hashed_password) VALUES (%s, %s, %s)"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.lastrowid
            return True

        else:
            sql = """UPDATE User SET username=%s, email=%s, hashed_password=%s, WHERE id=%s"""
            values = (username, email, hashed_password, id)
            cursor.execute(sql, values)
            return True


    @staticmethod
    def load_user_by_id(cursor, id):
        sql = "SELECT id, username, email, hashed_password FROM Users WHERE id={}".format(id)
        result = cursor.execute(sql, (id, ))
        data = cursor.fetchone()
        if data is not None:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT * FROM Users"
        cursor.execute(sql)
        ret = []
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
            return ret

    def delete(self, cursor):
        sql = "DELETE FROM User WHERE id=%s"
        cursor.execute(sql, self.__id)
        self.__id = -1
        return True


user1 = User()
user1.username = "Maggie"
user1.email = "maggie@op.pl"
user1.set_password("kot", "thing")

#user1.save_to_db(cursor)
#user1.load_user_by_id(cursor, 2)
#rint(user1.load_all_users(cursor))
user1.delete(cursor)

print(vars(user1))
cursor.close()
cnx.close()




