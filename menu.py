from DatabaseUtils import DatabaseUtils
# from W7 Prac
class Menu:
    def main(self):
        with DatabaseUtils() as db:
            db.createPersonTable()
        self.runMenu()

    def mainMenu(self):
        while(True):
            print("==Main Menu==")
            print("1. User Menu")
            print("2. Car Menu")
            print("3. Quit")
            selection = input("Select an option: ")
            print(selection)
            if(selection == "1"):
                self.userMenu()
            elif(selection == "2"):
                self.carMenu()
            elif(selection == "3"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def userMenu(self):
        while(True):
            print("==User Menu==")
            print("1. List People")
            print("2. Insert Person")
            print("3. Main Menu")
            print("3. Quit")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.listPeople()
            elif(selection == "2"):
                self.insertPerson()
            elif(selection == "3"):
                self.mainMenu()
            elif(selection == "4"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def carMenu(self):
        while(True):
            print("==Car Menu==")
            print("1. List Cars")
            print("2. Insert Cars")
            print("3. Main Menu")
            print("4. Quit")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.listPeople()
            elif(selection == "2"):
                self.insertPerson()
            elif(selection == "3"):
                self.mainMenu()
            elif(selection == "4"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def listPeople(self):
        print("--- People ---")
        print("{:<15} {}".format("UserID", "Name"))
        with DatabaseUtils() as db:
            for user in db.getUser():
                print("{:<15} {}".format(user[0], user[1]))

    def insertPerson(self):
        print("--- Insert New User ---")
        fname = input("Enter the users first name: ")
        lname = input("Enter the users last name: ")
        email = input("Enter the users email address")
        password = input ("Enter the users password - NEEDS TO BE HASHED")
        with DatabaseUtils() as db:
            if(db.insertPerson(fname, lname, email, password)):
                print("{} inserted successfully.".format(fname, lname, email, password))
            else:
                print("{} failed to be inserted.".format(fname, lname))


if __name__ == "__main__":
    Menu().mainMenu()
