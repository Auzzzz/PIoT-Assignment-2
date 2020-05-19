#from consoleAP import console
import socket

HOST = input("Enter IP address of server: ")

# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5000         # The port used by the server.
ADDRESS = (HOST, PORT)

def printMenu():
    print("\nWelcome to Agent Pi Console View!")
    print("1. Login")
    print("2. Exit")

def selectOptions():
    print("\nPlease select from these Options")
    print("1. Unlock Car")
    print("2. Return Car")
    print("3. Log Out")

def login(s):
    sent = True
    username = "username:" + input("Please enter username: ")
    s.sendall(username.encode())

    password = "password:" + input("Please enter password: ")
    s.sendall(password.encode())

    data = s.recv(4096)
    decodedData = data.decode()
    print(decodedData)

    if not data:
        sent = False

    if decodedData == "Login successfull":
        sent = True
    else:
        sent = False

    return sent


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to {}...".format(ADDRESS))
    s.connect(ADDRESS)
    print("Connected.")

    isLoggedIn = False

    #endless loop for menu until exit 
    while True:
        if not isLoggedIn:
            printMenu()
            response = input("\nResponse: ")
            
            if response == "1":
                if login(s):
                    isLoggedIn = True
                else:
                    print("\nLogin failed")
            elif response == "2":
                print("\nShutting down...")
                break
            else:
                print("\nError: Invalid Input")
        else:
            selectOptions()
            response = input("\nResponse: ")

            if response == "1":
                print("\nUnlocking car...")
            elif response == "2":
                print("\nReturning car...")
            elif response == "3":
                print("\nLogging out...")
                isLoggedIn = False
            else:
                print("\nError: Invalid Input")

    
    print("Disconnecting from server.")
print("Done.")


 