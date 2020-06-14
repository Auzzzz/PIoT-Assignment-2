from lib.flask_api import api, db
import os, requests, json
import unittest

class PartATests(unittest.TestCase):
    def test_engineerMACaddress(self):
        """Tests to see if route to validate mac address works
        """
        response = requests.get('http://127.0.0.1:5000/api/users/engineer/check/D0:7F:A0:98:1C:DE')
        self.assertEqual(response.status_code, 200)

    def test_checkIssueIsValid(self):
        """Tests to see if route to get issue with car id works
        """
        response = requests.get('http://127.0.0.1:5000/api/car/issue/car/list/109')
        self.assertEqual(response.status_code, 200)

    def test_setIssueStatus(self):
        """Tests to see if route to set issue status works
        """
        p = {'issue_status':2}
        response = requests.post('http://127.0.0.1:5000/api/car/issue/web/status/43', json=p)
        
        self.assertEqual(response.status_code, 200)
    


if __name__ == '__main__':
    unittest.main()