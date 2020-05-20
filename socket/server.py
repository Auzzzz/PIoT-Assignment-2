import socket
from passlib.hash import sha256_crypt
from _thread import *

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

def usernameAction(username, hashedPass):
    #Dummy return to appease the python gods
    return False

def passwordAction(username, password, hashedPass, s):
    #Dummy return to appease the python gods
    return False

def addClient(conn, addr):
    with conn:
        print("Connected to {}".format(addr))

        sessionUser = ''
        hashedPass = ''

        while True:
            data = conn.recv(2048)
            decodedData = data.decode()
            if(not data):
                break

            instruct, info = decodedData.split(":", 1)

            if instruct == "username":
                sessionUser = info
                print(str(addr) + ' -> Username: ' + sessionUser)
            elif instruct == "password":
                print(str(addr) + ' -> Password: ' + info)
                msg = 'sendback'
                conn.sendall(msg.encode())
        print("Disconnecting from client " + str(addr) + "...")
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind(ADDRESS)
    except socket.error as e:
        print(str(e))
     
    s.listen()

    while True:

        print("Listening on {}...".format(ADDRESS))
        conn, addr = s.accept()
        start_new_thread(addClient, (conn, addr,))
        print('Thread Number:' + str(threadCount))

    print("Closing listening socket...")
print("Done!")
            