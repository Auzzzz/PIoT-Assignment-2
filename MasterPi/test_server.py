import socket
import unittest
from getpass import getpass
from server import Functions

class TestServer(unittest.TestCase):
    def setUp(self):
        HOST = input("Enter IP address of server: ")

        # HOST = "127.0.0.1" # The server's hostname or IP address.
        PORT = 5002        # The port used by the server.
        ADDRESS = (HOST, PORT)

    def successfulLogin(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.assertEqual(login("1234","1234",s), "35" )