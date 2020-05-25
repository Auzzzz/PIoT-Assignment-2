from lib.flask_api import api, db
import os, requests, json
import unittest

class PartATests(unittest.TestCase):
    def test_loginSuccess(self):
        """Tests login for a valid user
        """
        response = requests.get('http://127.0.0.1:5000/api/token', auth=('1234','1234'))
        self.assertEqual(response.status_code, 200)
    
    def test_loginFailure(self):
        """Tests login for an invalid user
        """
        response = requests.get('http://127.0.0.1:5000/api/token', auth=('random','user'))
        self.assertEqual(response.status_code, 401)

    def test_insertPerson(self):
        """Tests the creation of an account
        """
        json = {'name':'Winston Lie','username':'unit_test','email':'email@email.com','password':'password1234'}
        response = requests.post('http://127.0.0.1:5000/api/person/i', json=json)
        self.assertEqual(response.status_code, 200)

    def test_getAllCars(self):
        """Tests the get all cars method in the API
        """
        response = requests.get('http://127.0.0.1:5000/api/car')  
        self.assertEqual(response.status_code, 200) 

    def test_getAllMake(self):
        """Tests the get all car makes method in the API
        """
        response = requests.get('http://127.0.0.1:5000/api/car/make') 
        self.assertEqual(response.status_code, 200)

    def test_getAllType(self):
        """Tests the get all car types method in the API
        """
        response = requests.get('http://127.0.0.1:5000/api/car/make') 
        self.assertEqual(response.status_code, 200)

    def test_createCar(self):
        """Tests the creation of a car 
        """
        json = {'seats':'5','colour':'black','cph':'50','location':'Melbourne','car_make_makeid':'3','car_type_typeid':'3'}
        response = requests.post('http://127.0.0.1:5000/api/car', json=json)
        self.assertEqual(response.status_code, 200)

    def test_createBooking(self):
        """Tests the creation of a booking
        """
        json = {'userid':'61','bdate':'2020-05-25','stime':'18:00:00','etime':'23:59:00','carid':'110','bookingstatus':'1','bookingcode':'12345'}
        response = requests.post('http://127.0.0.1:5000/api/car/booking', json=json)
        self.assertEqual(response.status_code, 200)

    def test_verifyBookingCode(self):
        """Verifies booking code by checking if it is related to a booking
        """
        json = {'bookingcode':'78705'}
        response = requests.post('http://127.0.0.1:5000/api/booking/code', json=json)
        self.assertEqual(response.status_code, 200)

    def test_updateBookingStatus(self):
        """Tests changing the booking status of a booking
        """
        json = {'bookingid':'37','bookingstatus':'3'}
        response = requests.post('http://127.0.0.1:5000/api/booking/s', json=json)
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()


