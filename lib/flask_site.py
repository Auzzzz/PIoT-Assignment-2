from flask import Flask, Blueprint, request, jsonify, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import sha256_crypt
import os, time, requests, json, random
from datetime import datetime
from lib.cal.cal import get_calendar_service
site = Blueprint("site", __name__)

### User ###
# Client webpage.
@site.route("/")
def index():
    return redirect('login')

#Register
@site.route('/register', methods=['GET', 'POST'])
def register():
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
            r = requests.post('http://127.0.0.1:5000/api/person', json=payload)
            msg = 'Congratz You have been registered......'
        else:
            msg = "Passwords do not match"
    elif request.method == 'POST':
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('register.html', msg=msg)

@site.route('/login', methods=['GET','POST'])
def login():
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
            #forward the user to home page
            msg = "Successfully logged in redirecting in 3 secounds"
            time.sleep(3)
            return redirect('home')
    return render_template('index.html', msg=msg)

@site.route('/home')
def home():
    if 'loggedin' in session:
        #When the user is logged in show them this top secret page
        return render_template('home.html', username=session['username'])
    #If not bye bye
    return redirect('login')

# Logout #
@site.route('/logout')
def logout():
    #remove all session data to log the user out
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    session.pop('name', None)
    session.pop('email', None)
    #move to login page
    return redirect('login')

# Profile Page #
@site.route('/profile')
def profile():
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
@site.route('/bookingconfirm', methods=['POST'])
def bookingConfirm():
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
            payload = {"userid":userid, "bdate":bdate, "stime":stime, "etime":etime, "carid":carid, "bookingstatus":bookingstatus, "bookingcode":bookingcode}
            r = requests.post('http://127.0.0.1:5000/api/car/booking', json=payload)
            msg = 'Congratz Your booing has been registered..... your booking code is:' + str(bookingcode)

        
        # creates one hour event tomorrow 10 AM IST
        service = get_calendar_service()
        event_result = service.events().insert(calendarId='primary',
            body={ 
                "summary": 'Your Car App', 
                "description": {'Calander Event for the booking you have made for car: ':carid},
                "start": {"dateTime": stime, "timeZone": 'Australia/Melbourne'}, 
                "end": {"dateTime": etime, "timeZone": 'Australia/Melbourne'},
            }
        ).execute()

        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    elif request.method == 'POST': #if no post request is made
        #error message
        msg = 'Fill the form out you ido*'
    return render_template('newbooking.html', msg=msg, bdate=bdate, carid = carid)

@site.route('/searchcar', methods=['GET', 'POST'])
def searchcar():
    if 'loggedin' in session:
        #Get cars for list
        response = requests.get('http://127.0.0.1:5000/api/car')
        #format the response in json
        cars = json.loads(response.text)
        #error message
  
        return render_template('search.html', cars=cars)
    else:
        return redirect('login')
        
@site.route('/test', methods=['GET', 'POST'])
def test():
    
    service = get_calendar_service()
    event_result = service.events().insert(calendarId='primary',
            body={ 
                "summary": 'Your Car App', 
                "description": {'Calander Event for the booking you have made for car: ':carid},
                "start": {"dateTime": stime, "timeZone": 'Australia/Melbourne'}, 
                "end": {"dateTime": etime, "timeZone": 'Australia/Melbourne'},
            }
        ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])
        
    return render_template('test.html')
