import 
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
    def createPersonTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists User (
                    UserID int not null auto_increment,
                    First_Name VARCHAR(50) not null,
                    Last_Name, VARCHAR(50) not null,
                    Email, VARCHAR(320) not null
                    Password CHAR(40), 
                    constraint PK_User primary key (UserID)
                )""")
        self.connection.commit()

    def insertUser(self, fname, lname, email, password):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into User (First_Name, Last_Name, Email, Password) values (%s)", (fname, lname, email, password))
        self.connection.commit()

        return cursor.rowcount == 1

    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select UserID, Name from User")
            return cursor.fetchall()

    def deletePerson(self, userid):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from User where UserID != %s", (userid,))
        self.connection.commit()
