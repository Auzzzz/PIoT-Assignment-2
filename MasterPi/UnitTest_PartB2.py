import unittest
from server import Functions
import socket

HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5001        # The port used by the server.
ADDRESS = (HOST, PORT)

class PartBTest(unittest.TestCase):
    def test_returnCar(self):
        """ Function to test validation that return car method is working as expected
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertTrue(Functions.returnCar(s, '38'))

if __name__ == '__main__':
    unittest.main()