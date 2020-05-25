import unittest
from client import Functions

class PartCTest(unittest.TestCase):
    
    def test_faceRecognitionSuccess(self):
        """Tests successful facial recognition.
        """
        self.assertEqual(Functions.recogniseFace(), '35')
    
if __name__ == '__main__':
    unittest.main()