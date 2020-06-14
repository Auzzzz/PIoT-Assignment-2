import unittest
from client import Functions
import socket

HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5001        # The port used by the server.
ADDRESS = (HOST, PORT)

class PartCTest(unittest.TestCase):
    
    def test_QRCodeSuccess(self):
        """Tests successful with qr code scanning, means a qr code is detected.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertTrue(Functions.detectQR(s))
    
if __name__ == '__main__':
    unittest.main()