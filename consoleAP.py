from lib.db_connection import DB
from passlib.hash import sha256_crypt

class ConsoleAP:

    #constructor (idk what to put in here just yet)
    def __init__(self):
        self.username = NULL
        self.loggedIn = False

    #method to log in
    def login(self, username, password):
        hashedPass = ''

        while DB() as db:
            passFromDB = db.getPasswordWithUser(username)

            if passFromDB:
                if sha256_crypt.verify(password, passFromDB[0]):
                    hashedPass = passFromDB[0]

                    account = db.loginUser(username, hashedPass)

                    if account:
                        self.username = username
                        self.loggedIn = True
                        return True
                else:
                    print("Incorrect password")
                    return False
            else:
                print("Error: Not a registered username")
                return False

    #method to log out
    def logout(self):
        self.username = NULL
        self.loggedIn = False


    #method to unlock car
    def unlockCar(self):
        print("To be implemented")


    #method to return car
    def returnCar(self):
        print("To be implemented")


    def printMenu(self):
        if self.loggedIn == False
            print("Welcome to Agent Pi Console View!")
            print("1. Login")
            print("2. Exit")
        else:
            print("Currently logged in as " + self.username)
            print("1. Unlock Car")
            print("2. Return Car")
            print("3. Logout")
