from __future__ import print_function
from flask import Flask, Blueprint, request, jsonify, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import sha256_crypt
import os, time, requests, json, random
from datetime import datetime
site = Blueprint("site", __name__)


from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

### User ###
# Client webpage.
@site.route("/")
def index():
    """Main page of website, redirects to login

    :return: login redirection
    """
    return redirect('login')

#Register
@site.route('/register', methods=['GET', 'POST'])
def register():
    """Web page for registering an account

    :return: Returns the template of register.html
    """
    #error message
    msg = ''
    #checking to see if the user has pressed the submit button by looking at POST request
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
    #Capture the form data
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirmPass = request.form['confirmPass']
        email = request.form['email']
        msg = ''
        #validate if password matches with confirmPass
        if password == confirmPass:
            #Add account into the DB
            payload = {"email":email, "name":name, "password":password, "username":username}
            r = requests.post('http://127.0.0.1:5000/api/person/i', json=payload)
            msg = 'Congratz You have been registered......'
        else:
            msg = "Passwords do not match"
    elif request.method == 'POST':
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('register.html', msg=msg)

@site.route('/login', methods=['GET','POST'])
def login():
    """Web page for logging in

    :return: Returns the template of login.html
    """
    msg = ''
    session['loggedin'] = True
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Capture the form data
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            msg = "Username or Password empty"
        else:
            #send user details of
            response = requests.get('http://127.0.0.1:5000/api/token', auth=(username, password))
            print("RESPONCE",response)
            #make response into json format
            data = json.loads(response.text)
            #take token out of json and submit it for access to user info
            token = data['token']
            response = requests.get('http://127.0.0.1:5000/api/login', auth=(token, 'unused'))
            #format the response in json
            data = json.loads(response.text)

            #make a session for user data
            session['loggedin'] = True
            session['userid'] = data['userid']
            session['username'] = data['username']
            session['name'] = data['name']
            session['email'] = data['email']
            session['userrole'] = data['users_roles_roleid']
            #forward the user to home page
            msg = "Successfully logged in redirecting in 3 secounds"
            return redirect('home')
    return render_template('index.html', msg=msg)

@site.route('/home')
def home():
    """Web page for a logged in user

    :return: Returns the template of home.html, or redirects to login if not logged in
    """
    if 'loggedin' in session:
        #When the user is logged in show them this top secret page
        return render_template('home.html', username=session['username'])
    #If not bye bye
    return redirect('login')

# Logout #
@site.route('/logout')
def logout():
    """Method to log out 

    :return: Redirects to login
    """
    #remove all session data to log the user out
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('userrole', None)

    #move to login page
    return redirect('login')

# Profile Page #
@site.route('/profile')
def profile():
    """Web page for the profile of a user

    :return: Returns the template of profile.html, or redirects to login if not logged in
    """
    # check if the user is logged in
    if 'loggedin' in session:
        #Get all car bookings
        userid = session['userid']
        p = {'userid':userid}
        response = requests.post('http://127.0.0.1:5000/api/booking/list', json=p)
        bookings = json.loads(response.text)

        # Show the profile page with account info
        return render_template('profile.html', bookings = bookings)
    # User is not loggedin redirect to login page
    return redirect('login') 


### Car ###
# insert car #
@site.route('/newcar', methods=['GET', 'POST'])
def newcar():
    """Method on site for creating a new car

    :return: Returns template for newcar.html
    """
    #Get car make for list
    response = requests.get('http://127.0.0.1:5000/api/car/make')
    #format the response in json
    carmake = json.loads(response.text)
    
    #Get car type for list
    response = requests.get('http://127.0.0.1:5000/api/car/type')
    #format the response in json
    cartype = json.loads(response.text)
    #error message
    msg = ''
    #checking to see if the user has pressed the submit button by looking at POST request
    if request.method == 'POST' and 'colour' in request.form and 'seats' in request.form and 'location' in request.form and 'cph' in request.form and 'ctype' in request.form and 'cmake' in request.form: #checks post requet for all inputs
        #Capture the form data
        colour = request.form['colour']
        seats = request.form['seats']
        location = request.form['location']
        cph = request.form['cph']
        cmake = request.form['cmake']
        ctype = request.form['ctype']
        #Add account into the DB
        if colour is None or seats is None or location is None or seats is None or cph is None or cmake is None or ctype is None:
            msg = 'Error.... Oh Well'
        else:
            payload = {"colour":colour, "seats":seats, "location":location, "cph":cph, "car_make_makeid":cmake, "car_type_typeid":ctype}
            r = requests.post('http://127.0.0.1:5000/api/car', json=payload)
            msg = 'Congratz You have been registered......'
    elif request.method == 'POST': #if no post request is made
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('newcar.html', carmake=carmake, cartype=cartype, msg=msg)


@site.route('/newbooking', methods=['GET', 'POST'])
def newbooking():
    """Web page for making a booking for a car

    :return: Returns template for newbooking.html
    """
    #get current date for date check
    current = datetime.today().strftime('%Y-%m-%d')
    #error message
    msg = ''
    #check to see if logged in
    if 'loggedin' in session:
        if request.method == 'POST' and 'carid' in request.form and 'date' in request.form:
            carid = request.form['carid']
            bdate = request.form['date']
            #get car bookings
            payload = {'carid':carid}
            response = requests.post('http://127.0.0.1:5000/api/car/checkavailability', json=payload)
            #format the response in json
            cars = json.loads(response.text)
            #get current date for date check
            current = datetime.today().strftime('%Y-%m-%d')
            #get the cars bookings for the day and record time
            for cars in cars:
                if cars["bdate"] == bdate:
                    msg = 'car is booked for that day, please choose another'

        else:
            return redirect('searchcar')
    else:
        return redirect('login') 
    return render_template('newbooking.html', msg=msg, bdate=bdate, carid = carid)

@site.route('/bookingconfirm', methods=['POST', 'GET'])
def bookingConfirm():
    """Confirms booking of a car

    :return: Returns template for newbooking.html
    """
    msg = ''
        #checking to see if the user has pressed the submit button by looking at POST request
    if request.method == 'POST' and 'stime' in request.form and 'etime' in request.form: #Get contents of post data
            userid = session['userid']
            #Capture the form data
            carid = request.form['carid']
            bdate = request.form['bdate']
            stime = request.form['stime']
            etime = request.form['etime']
            bookingstatus = 1
            bookingcode = random.randint(11111, 99999)
            
            #Add account into the DB
            if userid is None or bdate is None or stime is None or etime is None or carid is None:
                msg = 'Error.... Oh Well'
            else:
                
                #Removed google cal API

                #inset into db through api
                payload = {"userid":userid, "bdate":bdate, "stime":stime, "etime":etime, "carid":carid, "bookingstatus":bookingstatus, "bookingcode":bookingcode}
                r = requests.post('http://127.0.0.1:5000/api/car/booking', json=payload)
                msg = 'Congratz Your booing has been registered..... your booking code is:' + str(bookingcode)
            

    elif request.method == 'POST': #if no post request is made
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('newbooking.html', msg=msg, bdate=bdate, carid = carid)

@site.route('/searchcar', methods=['GET', 'POST'])
def searchcar():
    """Web page for searching a car

    :return: Returns template for search.html
    """
    if 'loggedin' in session:
        #Get cars for list
        response = requests.get('http://127.0.0.1:5000/api/car')
        #format the response in json
        cars = json.loads(response.text)
        #error message
        return render_template('search.html', cars=cars)
    else:
        return redirect('login')

@site.route('/bookingcancel', methods = ['GET','POST'])
def bookingcancel():
    """Web page for cancelling a booking

    :return: Returns template for bookingcancel.html
    """
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST':
            bookingid = request.form['bookingid']
            p = {'bookingid':bookingid,'bookingstatus':str(3)}
            response = requests.post('http://127.0.0.1:5000/api/booking/s', json=p)
            if response.ok:
                msg = 'successful'
            else:
                msg = 'errored'


        return render_template('bookingcancel.html', msg = msg)
    else:
        return redirect('login')


### Admin ###
#Show all users to edit
@site.route('/admin/user', methods = ['POST', 'GET'])
def adminUser():
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            #Get all users for the list
            response = requests.get('http://127.0.0.1:5000/api/person')
            #format the response in json
            users = json.loads(response.text)

            #get user role info
            response = requests.get('http://127.0.0.1:5000/api/userroles')
            #format the response in json
            userroles = json.loads(response.text)

            return render_template('admin_users.html', users = users, userroles = userroles)
        else:
            return redirect('/profile')
    else:
        return redirect('login')

#Edit selected user
@site.route('/admin/useredit', methods = ['POST', 'GET', 'PUT'])
def adminUserEdit():
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ''
                #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'userid' in request.form and 'name' in request.form and 'email' in request.form and 'username' in request.form and 'roleid' in request.form: #Get contents of post data
                userid = request.form['userid']
                #Capture the form data
                name = request.form['name']
                email = request.form['email']
                username = request.form['username']
                roleid = request.form['roleid']

                payload = {"name":name, "email":email, "username":username, "roleid":roleid}
                r = requests.put('http://127.0.0.1:5000/api/person/%s' % (userid,) , json=payload)

            return render_template('admin_users.html')
        else:
            return redirect('/profile')
    else:
        return redirect('login')

#Show all users to edit
@site.route('/admin/car', methods = ['POST', 'GET'])
def adminCar():
    msg = ''
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            #Get all users for the list
            response = requests.get('http://127.0.0.1:5000/api/car')
            #format the response in json
            cars = json.loads(response.text)

            #Get car make for list
            response = requests.get('http://127.0.0.1:5000/api/car/make')
            #format the response in json
            carmake = json.loads(response.text)
            
            #Get car type for list
            response = requests.get('http://127.0.0.1:5000/api/car/type')
            #format the response in json
            cartype = json.loads(response.text)

            return render_template('admin_cars.html', cars = cars, carmake = carmake, cartype = cartype, msg = msg)
        else:
            return redirect('/profile')
    else:
        return redirect('login')


#Edit selected car
@site.route('/admin/caredit', methods = ['POST', 'GET', 'PUT'])
def adminCarEdit():
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ''
            #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'carid' in request.form and 'colour' in request.form and 'seats' in request.form and 'location' in request.form and 'cph' in request.form and 'car_make_makeid' in request.form and 'car_type_typeid' in request.form: #Get contents of post data
                carid = request.form['carid']
                #Capture the form data
                colour = request.form['colour']
                seats = request.form['seats']
                location = request.form['location']
                cph = request.form['cph']
                car_make_makeid = request.form['car_make_makeid']
                car_type_typeid = request.form['car_type_typeid']

                payload = {"colour":colour, "seats":seats, "location":location, "cph":cph, "car_make_makeid":car_make_makeid, "car_type_typeid":car_type_typeid}
                r = requests.put('http://127.0.0.1:5000/api/car/%s' % (carid,) , json=payload)
            
            return render_template('admin_cars.html')
        else:
            return redirect('/profile')
    else:
        return redirect('login')


@site.route('/admin/car/issue', methods = ['POST', 'GET', 'PUT'])
def adminCarIssue():
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ''
            #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'carid' in request.form: #Get contents of post data
                carid = request.form['carid']
                #Capture the form data
            else:
                return redirect('/admin/car')

            #Pass through all avaliable maint users
            users_roles_roleid = 4 # usertype for maint workers is 2
            p = {'users_roles_roleid':users_roles_roleid}
            response = requests.post('http://127.0.0.1:5000/api/users', json=p)
            maint = json.loads(response.text)

            return render_template('admin_cars_report.html', carid = carid, maint = maint)
        else:
            return redirect('/profile')
    else:
        return redirect('login')

@site.route('/admin/car/issue/R', methods = ['POST', 'GET'])
def adminCarIssueReport():
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:     
            print("Test1")       
            msg = ''
            #checking to see if the user has pressed the submit button by looking at POST request

            print("Test2")
            carid = request.form['carid']
            report = request.form['report']
            maintid = request.form['maintID']

            p = {'carid':carid,'notes':report, 'assigned_to':maintid}
            response = requests.post('http://127.0.0.1:5000/api/car/issue', json=p)
            print(response)
            if response.ok:
                msg = 'successful'
            else:
                msg = 'errored'
            

            
            return render_template('admin_cars_report.html')
        else:
            return redirect('/profile')
    else:
        return redirect('login')


@site.route('/test', methods = ['POST', 'GET', 'PUT'])
def test():

    
    return render_template('test.html')