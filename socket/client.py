#from consoleAP import console
import socket
from getpass import getpass


HOST = input("Enter IP address of server: ")

# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5004        # The port used by the server.
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

        password = getpass('Password: ')
        passToSend = "password:" + password
        s.sendall(passToSend.encode())

        data = s.recv(4096)
        decodedData = data.decode()

        if not data:
            sent = False

        if decodedData == "Login successful":
            sent = True
        else:
            sent = False

        return sent


    def unlockCar(s):
        unlocked = False
        carID = "carid:" + input("Car ID: ")
        s.sendall(carID.encode())
        unlockCode = "unlockcode:" + input("Unlock Code: ")
        s.sendall(unlockCode.encode())

        data = s.recv(4096)
        decodedData = data.decode()

        if not data:
            unlocked = False
    
        if decodedData == "Car Unlocked":
            unlocked = True
        else:
            unlocked = False

        return unlocked


class Main:
    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(ADDRESS))
            s.connect(ADDRESS)
            print("Connected.")

            isLoggedIn = False

            #endless loop for menu until exit 
            while True:
                if not isLoggedIn:
                    Menu.printMenu()
                    response = input("\nResponse: ")
            
                    if response == "1":
                        if Functions.login(s):
                            isLoggedIn = True
                            print("\nLogin successful!")
                        else:
                            print("\nLogin failed")
                    elif response == "2":
                        print("\nShutting down...")
                        break
                    else:
                        print("\nError: Invalid Input")
                else:
                    Menu.selectOptions()
                    response = input("\nResponse: ")

                    if response == "1":
                        if Functions.unlockCar(s):
                            print("\nCar Unlocked")
                        else:
                            print("\nInvalid credentials or car already unlocked by user...")
                    elif response == "2":
                        print("\nReturning car...")
                    elif response == "3":
                        print("\nLogging out...")
                        isLoggedIn = False
                    else:
                        print("\nError: Invalid Input")

            print("Disconnecting from server.")
        print("Done.")


if __name__ == "__main__":
    Main.run()

