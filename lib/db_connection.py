import MySQLdb 

class DB:
    ### Database Conn ###
    HOST = "34.87.245.145"
    USER = "root"
    PASSWORD = "banana192"
    DATABASE = "carshare"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DB.HOST, DB.USER,
                DB.PASSWORD, DB.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
    
### User DB Qureys ###

    def insertUser(self, name, username, email, password):
        with self.connection.cursor() as cursor:
            cursor.execute('insert into users values (NULL, %s, %s, %s, %s, NULL, NULL)', (name, username, email, password,)) ##TODO: add password hashing
        self.connection.commit()

    def checkUser(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from users where username = %s', (username,))
        self.cursor.fetchone()  
    
    def loginUser(self, user, password):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from users where name = %s and password = %s", (user, password))
            return cursor.fetchone() 

    def accountUser(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from users where id = %s', (id,))
            return cursor.fetchone()


### Car DB Qureys ####
# get avaliable car makes #
    def getCarMake(self):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from car_make')
            return cursor.fetchall()

    def getCarType(self):
        with self.connection.cursor() as cursor:
            cursor.execute('select * from car_type')
            return cursor.fetchall()
    
    def insertNewCar(self, colour, seats, location, cph, cmake, ctype):
        with self.connection.cursor() as cursor:
            cursor.execute('insert into cars values (NULL, %s, %s, %s, %s, %s, %s)', (colour, seats, location, cph, cmake, ctype,))
        self.connection.commit()