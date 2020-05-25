import unittest
from client import Functions

class PartCTest(unittest.TestCase):
    
    def test_faceRecognitionSuccess(self):
        self.assertEqual(Functions.recogniseFace(), '35')
    
if __name__ == '__main__':
    unittest.main()