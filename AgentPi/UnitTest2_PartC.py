import unittest
from client import Functions

class PartCTest(unittest.TestCase):
    
    def test_faceRecognitionTimeout(self):
        """Tests facial recognition timeout when the user fails to provide a valid face in time.
        """
        self.assertEqual(Functions.recogniseFace(), '')
    
if __name__ == '__main__':
    unittest.main()