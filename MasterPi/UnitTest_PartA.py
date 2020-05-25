from lib.flask_api import api, db
import os, requests, json
import unittest

class PartATests(unittest.TestCase):
    def test_loginSuccess(self):
        response = requests.get('http://127.0.0.1:5000/api/token', auth=('1234','1234'))
        self.assertEqual(response.status_code, 200)
    
    def test_loginFailure(self):
        response = requests.get('http://127.0.0.1:5000/api/token', auth=('random','user'))
        self.assertEqual(response.status_code, 401)

    

if __name__ == '__main__':
    unittest.main()


