import MySQLdb 
import hashlib
import os
## Modified from W7 Prac
class DatabaseUtils:
    HOST = "34.87.245.145"
    USER = "root"
    PASSWORD = "banana192"
    DATABASE = "carshare"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def insertUser(self, hashpass ,name, email, pass_to_hash):
        salt = os.urandom(32)
        password = hashlib.pbkdf2_hmac('sha256', pass_to_hash.encode('utf-8'), salt, 100000)

        with self.connection.cursor() as cursor:
            insert = [name, email, password, salt]
            cursor.execute("insert into users (Name, Email, Password, Salt) values (%s,%s,%s,%s)", insert)
        self.connection.commit()

        return cursor.rowcount == 1

    def getUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select UserID, Name from users")
            return cursor.fetchall()

    def deletePerson(self, userid):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from users where UserID != %s", (userid,))
        self.connection.commit()