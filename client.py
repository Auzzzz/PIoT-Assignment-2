#from consoleAP import console
import socket
from passlib.hash import sha256_crypt

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

def checkSelectOption(option):
    if option == "1":
        data = "Implement unlock car method"
    elif option == "2":
        data = "Implement return car method"
    elif option == "3":
        data ="Exiting right now!"
    
    return data

def login(s):
    sent = True
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    
    hashedPassword = sha256_crypt.hash(password)

    s.sendall(username.encode())
    s.sendall(hashedPassword.encode())

    data = s.recv(4096)

    if not data:
        sent = False

    return sent


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to {}...".format(ADDRESS))
    s.connect(ADDRESS)
    print("Connected.")

    while True:
        printMenu()
        message = input("Enter your choice: ")
        if message == "1":
            if login(s):
                loggedIn = True
            else:
                print("Login failed")
        elif message == "2":
            print("Exiting now!")
            break
        else:
            print("Invalid Input")
        
        if loggedIn:
            while True:
                selectOptions()
                option = input("Enter Option: ")
                data = checkSelectOption(option)
                if data == "Exiting right now!":
                    break
                else:
                    print(data)

        else:
            print("Log In failed!")

    
    print("Disconnecting from server.")
print("Done.")


 