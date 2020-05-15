import socket
from lib.db_connection import DB
from passlib.hash import sha256_crypt

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

def usernameAction(username, hashedPass):
    with DB() as db:
        passFromDB = db.getPasswordWithUser(sessionUser)

        if passFromDB:
            hashedPass = passFromDB[0]
    
    return hashedPass

def passwordAction(username, password, hashedPass, s):
    if hashedPass != '':
        if sha256_crypt.verify(password, hashedPass):
            with DB() as db:
                account = db.loginUser(username, hashedPass)

                if account:
                    data = "Login successfull"

                else:
                    data = "Login failed"

        else:
            data = "Login failed"
            
    else:
        data = "Login failed"


    conn.sendall(data.encode())        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))

        sessionUser = ''
        hashedPass = ''

        while True:
            data = conn.recv(4096)
            decodedData = data.decode()
            if(not data):
                break

            instruct, info = decodedData.split(":", 1)

            if instruct == "username":
                sessionUser = info
                hashedPass = usernameAction(sessionUser, hashedPass)
            elif instruct == "password":
                passwordAction(sessionUser, info, hashedPass, conn)

        #    print("Received {} bytes of data decoded to: '{}'".format(
        #        len(data), data.decode()))
        #    print("Sending data back.")
        #    conn.sendall(data)
        
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")
            