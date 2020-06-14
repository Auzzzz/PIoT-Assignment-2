import unittest
from client import Functions
import socket

HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5001        # The port used by the server.
ADDRESS = (HOST, PORT)

class A3PartBTest(unittest.TestCase):

    def test_bluetoothDetected(self):
        """Tests successful bluetooth detection.
        """
        found_devices = []
        found_devices_success = ['D0:7F:A0:98:1C:DE']
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            self.assertEqual(Functions.searchBluetooth(s, found_devices, True), found_devices_success)

if __name__ == '__main__':
    unittest.main()