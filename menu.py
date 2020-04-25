#from DatabaseUtils import DatabaseUtils
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
            print()
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
        print("{:<15} {}".format("Person ID", "Name"))
        with DatabaseUtils() as db:
            for person in db.getPeople():
                print("{:<15} {}".format(person[0], person[1]))

    def insertPerson(self):
        print("--- Insert Person ---")
        name = input("Enter the person's name: ")
        with DatabaseUtils() as db:
            if(db.insertPerson(name)):
                print("{} inserted successfully.".format(name))
            else:
                print("{} failed to be inserted.".format(name))


if __name__ == "__main__":
    Menu().mainMenu()
