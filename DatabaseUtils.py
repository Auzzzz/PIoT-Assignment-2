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

#####User DB SQL#####

#Insert a user into the DB, pulled from menu.py
    def insertUser(self, hashpass ,name, email, pass_to_hash):
        salt = os.urandom(32)
        password = hashlib.pbkdf2_hmac('sha256', pass_to_hash.encode('utf-8'), salt, 100000)

        with self.connection.cursor() as cursor:
            insert = [name, email, password, salt]
            cursor.execute("insert into users (Name, Email, Password, Salt) values (%s,%s,%s,%s)", insert)
        self.connection.commit()

        return cursor.rowcount == 1
#serch a user from the DB, pulled from menu.py
    def getUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select UserID, Name, Email from users")
            return cursor.fetchall()
#remove a user from the DB, pulled from menu.py
    def deletePerson(self, userid):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from users where UserID != %s", (userid,))
        self.connection.commit()

#####Car DB SQL#####

#Insert a car into the DB, pulled from menu.py
    def insertCar(self, colour , makeid , typeid , seats, location, cph):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into cars (colur, seats, location, cph, makeid, typeid) values (%s,%s,%s,%s,%s,%s)")
        self.connection.commit()

        #INSERT INTO `cars` (`carid`, `colour`, `seats`, `location`, `cph`, `car_make_makeid`, `car_type_typeid`) VALUES ('1', 'Black', '4', 'Melbourne', '7.5', '5', '3');

        return cursor.rowcount == 1
#serch a car from the DB, pulled from menu.py
    def getCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT carid, colour, car_make_makeid, car_type_typeid, seats, location, cph FROM cars")
            return cursor.fetchall()
#remove a car from the DB, pulled from menu.py
    def deleteCar(self, userid):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from users where UserID != %s", (userid,))
        self.connection.commit()

#show make options
    def getCarMake(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select makeid, make from car_make")
            return cursor.fetchall()

#show type options
    def getCarType(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select typeid, type from car_type")
            return cursor.fetchall()

