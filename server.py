import socket

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))

        while True:
            data = conn.recv(4096)
            if(not data):
                break
            print("Received {} bytes of data decoded to: '{}'".format(
                len(data), data.decode()))
            print("Sending data back.")
            conn.sendall(data)
        
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")
