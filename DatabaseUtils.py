#import MySQLdb 
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

    #add in password not null when hashing added
    def createUserTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists User (
                    UserID int not null auto_increment,
                    Name VARCHAR(100) not null,
                    Email VARCHAR(320) not null,
                    Password CHAR(40), 
                    Salt CHAR(32),
                    constraint PK_User primary key (UserID)
                )""")
        self.connection.commit()

    def insertUser(self, hashpass ,name, email, pass_to_hash):
        salt = os.urandom(32)
        password = hashlib.pbkdf2_hmac('sha256', pass_to_hash.encode('utf-8'), salt, 100000)

        with self.connection.cursor() as cursor:
            insert = [name, email, password, salt]
            cursor.execute("insert into User (Name, Email, Password, Salt) values (%s,%s,%s,%s)", insert)
        self.connection.commit()

        return cursor.rowcount == 1

    def getUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select UserID, Name from User")
            return cursor.fetchall()

    def deletePerson(self, userid):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from User where UserID != %s", (userid,))
        self.connection.commit()