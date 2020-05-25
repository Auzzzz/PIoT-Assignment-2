import unittest
from client import Functions

class PartCTest(unittest.TestCase):
    
    def test_faceRecognitionTimeout(self):
        self.assertEqual(Functions.recogniseFace(), '')
    
if __name__ == '__main__':
    unittest.main()