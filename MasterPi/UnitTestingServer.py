import socket

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5001 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

class Main:
    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(ADDRESS)
                print('Server Running...')
                print("\n( -- Press CTRL+C to Quit -- )\n")
            except socket.error as e:
                print(str(e))
     
            s.listen()

            while True:
                try:
                    print("Listening on {}...".format(ADDRESS))
                    conn, addr = s.accept()
                except KeyboardInterrupt:
                    break

            s.shutdown(socket.SHUT_RDWR)
            s.close()
            print("\nClosing listening socket...")
        print("Done!")

if __name__ == '__main__':
    Main.run()