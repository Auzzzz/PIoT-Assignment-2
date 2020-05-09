from DatabaseUtils import DatabaseUtils

# from W7 Prac
class Menu:
    def main(self):
        self.mainMenu()

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
#test
            if(selection == "1"):
                self.listPeople()
            elif(selection == "2"):
                self.insertUser()
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
                self.listCar()
            elif(selection == "2"):
                self.insertCar()
            elif(selection == "3"):
                self.mainMenu()
            elif(selection == "4"):
                self.listCarMake()
                #print("Goodbye!")
                #break
            else:
                print("Invalid input - please try again.")
#####User#####
    def listPeople(self):
        print("--- People ---")
        print("{:<15} {}".format("UserID", "Name", "Email"))
        with DatabaseUtils() as db:
            for user in db.getUser():
                print("{:<15} {}".format(user[0], user[1]))

    def insertUser(self):
        print("--- Insert New User ---")
        name = input("Enter the users name: ")
        email = input("Enter the users email address: ")
        pass_to_hash = input ("Enter the users password - NEEDS TO BE HASHED: ")
        
        with DatabaseUtils() as db:
            if(db.insertUser(name, email, pass_to_hash)):
                print("{} inserted successfully.".format(name, email, pass_to_hash))
            else:
                print("{} failed to be inserted.".format(name))

#####Car#####
    def listCarMake(self):
        print("--- Car Makes ---")
        print("{:<15} {}".format("MakeID", "Make"))
        with DatabaseUtils() as db:
            for make in db.getCarMake():
                print("{:<15} {}".format(make[0], make[1]))
    
    def listCarType(self):
        print("--- Car Makes ---")
        print("{:<15} {}".format("TypeID", "Type"))
        with DatabaseUtils() as db:
            for typec in db.getCarType():
                print("{:<15} {}".format(typec[0], typec[1]))

    def listCar(self):
        print("--- All Cars ---")
        print("{:<15} {}".format("CarID", "Colour", "Make", "Type", "Seats", "Location", "Cost Per Hour"))
        with DatabaseUtils() as db:
            for car in db.getCar():
                 print("{:<15} {}".format(car[0], car[1], car[3], car[4], car[5], car[6]))

    def insertCar(self):
        print("--- Insert New Car ---")
        print("Available Makes: ", self.listCarMake())
        makeid = input("Choose the Makeid of the car ")
        print("Available Types: ", self.listCarType())
        typeid = input("Choose the Typeid of the car")
        colour = input("Colour of the car")
        seats = input("How many seats are in the car")
        location = input("Current location")
        cph = input("What is the cost to hire car eg. 7.5")
        
        with DatabaseUtils() as db:
            if(db.insertUser(colour, makeid, typeid, seats, location, cph)):
                print("{} inserted successfully.")
            else:
                print("{} failed to be inserted.")



if __name__ == "__main__":
    Menu().main()
