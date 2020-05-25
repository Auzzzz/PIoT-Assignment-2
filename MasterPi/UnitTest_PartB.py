import unittest
from server import Functions
import socket

HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5001        # The port used by the server.
ADDRESS = (HOST, PORT)

class PartBTest(unittest.TestCase):
    def test_successfulLogin(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertEqual(Functions.login("1234","1234",s), "35")


    def test_unlockCarWithInvalidCode(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertEqual(Functions.unlockCar(s, '12787', '35'), '')


    #loginWithFace function passes a userID since it has already confirmed the face
    def test_loginWithFaceSuccess(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertEqual(Functions.loginWithFace('35', s), '35')


    def test_loginWithFaceFailure(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertEqual(Functions.loginWithFace('100', s), '')


    #need to make a valid booking for this test to work
    def test_unlockCarSuccessfully(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertEqual(Functions.unlockCar(s, '59300', '35'), '38')

if __name__ == '__main__':
    unittest.main()