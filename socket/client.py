#from consoleAP import console
import socket
from getpass import getpass


HOST = input("Enter IP address of server: ")

# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5001        # The port used by the server.
ADDRESS = (HOST, PORT)

class Menu:
    def printMenu():
        print("\nWelcome to Agent Pi Console View!")
        print("1. Login")
        print("2. Exit")

    def selectOptions():
        print("\nPlease select from these Options")
        print("1. Unlock Car")
        print("2. Return Car")
        print("3. Log Out")

class Functions:
    def login(s):
        sent = True
        username = "username:" + input("Please enter username: ")
        s.sendall(username.encode())
        outcome = False

        password = getpass('Password: ')
        passToSend = "password:" + password
        s.sendall(passToSend.encode())

        data = s.recv(4096)
        decodedData = data.decode()

        if not data:
            return

        if decodedData == "Login successful":
            print('\nLogin Successful')
            outcome = True

        else:
            print('\nLogin Failed')
            outcome = False

        return outcome


    def unlockCar(s):
        unlocked = False
        bookingCode = "bookingcode:" + input("Unlock Code: ")
        s.sendall(bookingCode.encode())

        data = s.recv(2048)
        decodedData = data.decode()

        if not data:
            return
    
        if decodedData == "Car Unlocked":
            print('\nCar Unlocked')
    
        elif decodedData == 'Not your booking':
            print('\nError: Not your booking')

        elif decodedData == 'Already Unlocked':
            print('\nError: Car has already been unlocked')

        elif decodedData == 'Car already returned':
            print('\nError: Car has already been returned')

        else:
            print('\nError: Invalid booking code')


    def returnCar(s):
        returned = False
        x = input('Are you sure you want to return the car? (Y/N): ')
        userInput = x.upper()
        msg = "returncar:" + userInput

        if userInput == 'Y' or userInput == 'N':
            s.sendall(msg.encode())
            data = s.recv(2048)
            decodedData = data.decode()

            if not data:
                return
            elif decodedData == 'Car Unlocked':
                print('\nCar Returned')
            elif decodedData == 'Rejected':
                print('\nReturning car cancelled...')
            else:
                print('\nError while returning car')


class Main:
    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(ADDRESS))
            s.connect(ADDRESS)
            print("Connected.")

            isLoggedIn = False
            hasUnlocked = False

            #endless loop for menu until exit 
            while True:
                if not isLoggedIn:
                    Menu.printMenu()
                    response = input("\nResponse: ")
            
                    if response == "1":
                        if Functions.login(s):
                            isLoggedIn = True
                        else:
                            isLoggedIn = False
                    elif response == "2":
                        print("\nShutting down...")
                        break
                    else:
                        print("\nError: Invalid Input")
                else:
                    Menu.selectOptions()
                    response = input("\nResponse: ")

                    if response == "1":
                        if hasUnlocked:
                            print('You have already unlocked a car')
                        else:
                            Functions.unlockCar(s)
                            hasUnlocked = True

                    elif response == "2":
                        if hasUnlocked:
                            Functions.returnCar(s)
                            hasUnlocked = False
                        else:
                            print('\nYou have not unlocked a car to return')

                    elif response == "3":
                        print("\nLogging out...")
                        isLoggedIn = False
                    else:
                        print("\nError: Invalid Input")

            print("Disconnecting from server.")
        print("Done.")


if __name__ == "__main__":
    Main.run()