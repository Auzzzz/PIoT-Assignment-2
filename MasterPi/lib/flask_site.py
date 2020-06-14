from __future__ import print_function
from flask import Flask, Blueprint, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import sha256_crypt
import os, time, requests, json, random
from datetime import datetime
import speech_recognition as sr
site = Blueprint("site", __name__)

#pushbullet
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


import googlemaps
import speech_recognition as sr
import subprocess

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
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
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
            if request.method == 'POST' and 'colour' in request.form and 'seats' in request.form and 'location' in request.form and 'cph' in request.form and 'ctype' in request.form and 'cmake' in request.form and 'car_status' in request.form: #checks post for all inputs
                #Capture the form data
                colour = request.form['colour']
                seats = request.form['seats']
                location = request.form['location']
                cph = request.form['cph']
                cmake = request.form['cmake']
                ctype = request.form['ctype']
                car_status = request.form['car_status']

                #Add account into the DB
                if colour is None or seats is None or location is None or seats is None or cph is None or cmake is None or ctype is None:
                    msg = 'Error.... Oh Well'
                else:
                    payload = {"colour":colour, "seats":seats, "location":location, "cph":cph, "car_make_makeid":cmake, "car_type_typeid":ctype, "car_status":car_status}
                    r = requests.post('http://127.0.0.1:5000/api/car', json=payload)
                    msg = 'Congratz You have been registered......'
            elif request.method == 'POST': #if no post request is made
                    #error message
                    msg = 'Fill the form out you ido*'
            return render_template('newcar.html', carmake=carmake, cartype=cartype, msg=msg)
        else:
            return redirect('profile')
    else:
        return redirect('login')

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
    """Web page for admin account

    :return: Returns template for admin_users.html or redirects if wrong
    """
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

            #Get all engineers to check if engineer was an engineer before
            response = requests.get('http://127.0.0.1:5000/api/users/engineer')
            #format the response in json
            engineer = json.loads(response.text)

            return render_template('admin_users.html', users = users, userroles = userroles, engineer = engineer )
        else:
            return redirect('/profile')
    else:
        return redirect('login')

#Edit selected user
@site.route('/admin/useredit', methods = ['POST', 'GET', 'PUT'])
def adminUserEdit():
    """Website route for editing user details

    :return: Redirects to admin/user, or profile, or login
    """
    #Get all engineers to check if engineer was an engineer before
    response = requests.get('http://127.0.0.1:5000/api/users/engineer')
    #format the response in json
    engineers = json.loads(response.text)
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            
                #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'userid' in request.form and 'name' in request.form and 'email' in request.form and 'username' in request.form and 'roleid' in request.form: #Get contents of post data
                userid = request.form['userid']
                #Capture the form data
                name = request.form['name']
                email = request.form['email']
                username = request.form['username']
                roleid = request.form['roleid']
                if roleid == '2':
                    for each in engineers:
                        if each["userid"] == userid:
                            msg = ''
                        else:
                            #create them in the engineer table
                            print("make")
                            mac_address = "Null"
                            pushbullet_api = "Null"
                            payload = {"userid":userid, "mac_address":mac_address, "pushbullet_api":pushbullet_api}
                            r = requests.post('http://127.0.0.1:5000/api/users/engineer', json=payload)

                payload = {"name":name, "email":email, "username":username, "roleid":roleid}
                r = requests.put('http://127.0.0.1:5000/api/person/%s' % (userid,) , json=payload)

            return redirect('/admin/user')
        else:
            return redirect('/profile')
    else:
        return redirect('login')

#delete selected user
@site.route('/admin/user/delete', methods = ['POST', 'GET', 'DELETE'])
def adminUserDelete():
    """Website route for deleting users

    :return: Redirects to site.adminUser
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ""
            if request.method == 'POST' and 'userid' in request.form:
                userid = request.form['userid']

                response = requests.delete('http://127.0.0.1:5000/api/person/%s' % (userid,))
                if response.ok:
                    msg = 'successful'
                else:
                    msg = 'errored'
            return redirect(url_for('site.adminUser'))

@site.route('/admin/user/engineer', methods = ['POST', 'GET'])
def adminUserEngineer():
    """Website route for inputting engineer data

    :return: Returns redirection to site.adminUser
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ""
            if request.method == 'POST' and 'mac' in request.form and 'push' in request.form:
                #update engineers
                userid = request.form['userid']
                mac_address = request.form['mac']
                pushbullet_api = request.form['push']
                
                payload = {"mac_address":mac_address, "pushbullet_api":pushbullet_api}
                r = requests.put('http://127.0.0.1:5000/api/users/engineer/%s' % (userid), json=payload)

            return redirect(url_for('site.adminUser'))

#Show all users to edit
@site.route('/admin/car', methods = ['POST', 'GET'])
def adminCar():
    """Website route for getting all car information

    :return: Returns template for admin_cars.html, or redirects if wrong
    """
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

#delete selected car
@site.route('/admin/car/delete', methods = ['POST', 'DELETE'])
def adminCarDelete():
    """Website route for deleting cars

    :return: Returns redirection to site.adminCar
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ""
            if request.method == 'POST' and 'carid' in request.form:
                carid = request.form['carid']

                response = requests.delete('http://127.0.0.1:5000/api/car/del/%s' % (carid,))
                if response.ok:
                    msg = 'successful'
                else:
                    msg = 'errored'
            return redirect(url_for('site.adminCar'))

#Edit selected car
@site.route('/admin/caredit', methods = ['POST', 'GET', 'PUT'])
def adminCarEdit():
    """Website route for editing car details

    :return: Returns template for admin_cars.txt or redirects if wrong
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 4:
            msg = ''

            #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'carid' in request.form and 'colour' in request.form and 'seats' in request.form and 'location' in request.form and 'cph' in request.form and 'car_make_makeid' in request.form and 'car_type_typeid' in request.form and 'car_status' in request.form: #Get contents of post data
                carid = request.form['carid']
                #Capture the form data
                colour = request.form['colour']
                seats = request.form['seats']
                location = request.form['location']
                cph = request.form['cph']
                car_make_makeid = request.form['car_make_makeid']
                car_type_typeid = request.form['car_type_typeid']
                car_status = request.form['car_status']

                payload = {"colour":colour, "seats":seats, "location":location, "cph":cph, "car_make_makeid":car_make_makeid, "car_type_typeid":car_type_typeid, "car_status":car_status}
                r = requests.put('http://127.0.0.1:5000/api/car/%s' % (carid,) , json=payload)
            
            return render_template('admin_cars.html')
        else:
            return redirect('/profile')
    else:
        return redirect('login')


def getCarIDToSearch():
    """Gets carID for searching using the voice recognition

    :return: Returns found CarID (whatever was said to the microphone)
    :rtype: String
    """
    
    if request.method == 'POST':
    
        # To test searching without the microphone uncomment this line of code
        # return input("Enter the first name to search for: ")
        MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"

        # Set the device ID of the mic that we specifically want to use to avoid ambiguity
        for i, microphone_name in enumerate(sr.Microphone()):
            if(microphone_name == MIC_NAME):
                device_id = i
                break

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)

            print("Car ID Expected")
            try:
                audio = r.listen(source, timeout = 1.5)
            except sr.WaitTimeoutError:
                return None

        # recognize speech using Google Speech Recognition
        carID = None
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            carID = r.recognize_google(audio)
        except(sr.UnknownValueError, sr.RequestError):
            pass
        finally:
            return carID
            print(carid)


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


@site.route('/admin/car/issue', methods = ['POST', 'GET', 'PUT'])
def adminCarIssue():
    """Website route for checking issues with cars

    :return: Returns template for admin_cars_report.html, or redirects if wrong
    """
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
            users_roles_roleid = 2 # usertype for maint workers is 2
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
    """Website route for viewing report for issue

    :return: Returns template for admin_cars_report.html or redirects to admin/car
    """
 #Checks to see if user is logged in
    if request.method == 'POST' and 'carid' in request.form and 'notes' in request.form and 'maint' in request.form: #Get contents of post data
        carid = request.form['carid']
        notes = request.form['notes']
        assigned_to = int(request.form['maint'])
        #get engineer pushbullet details
        #Get all engineers to check if engineer was an engineer before
        response = requests.get('http://127.0.0.1:5000/api/users/engineer')
        #format the response in json
        engineers = json.loads(response.text)

        
        for each in engineers:
            if each["userid"] == assigned_to:
                #send pushbullet 
                key = each['pushbullet_api']
                title = "Please check on car: " + str(carid)
                body = "Admin %s has added a new job to your job list. DETAILS: %s" % (session['userid'], notes)
                pushbullet(title, body, key, assigned_to)

                #add to DB
                payload = {"carid":carid, "notes":notes, "assigned_to":assigned_to}
                r = requests.post('http://127.0.0.1:5000/api/car/issue', json=payload)

            
                return redirect('/admin/car')

    return render_template('admin_cars_report.html')

def pushbullet(title, body, key, assigned_to):
    """Uses pushbullet API to notify engineer using the pushbullet app when an admin logs an issue with a car

    :param title: Title of the issue
    :type title: String
    :param body: Body of the message
    :type body: String
    :param key: API Key
    :type key: String
    :param assigned_to: Assigned Engineer
    :type assigned_to: String
    """
    #from pushbullet api docs
    data_send = {"type": "note", "title": title, "body": body}
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        msg = 'Something went wrong'
    else:
        msg = 'Notifction send to %s' % (assigned_to)

@site.route('/admin/car/bookings', methods = ['POST', 'GET'])
def adminCarBookings():
    """Display all bookings for a car

    :return: Returns redirection to admin/car, profile or login, or tempalte for admin_car_bookings.html
    """
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

            #Capture the form data
            response = requests.get('http://127.0.0.1:5000/api/car/b/%s' % (carid))
            #format the response in json
            bookings = json.loads(response.text)

            return render_template('admin_car_bookings.html', carid = carid, bookings = bookings)
        else:
            return redirect('/profile')
    else:
        return redirect('login')

@site.route('/engineer', methods = ['POST', 'GET'])
def engineerJobs():
    """Lists all jobs for a specific engineer

    :return: Returns template for engineer_jobs.html, or redirects
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an admin or a imposter
        if session['userrole'] == 2:
            msg = ''
           
            #get userid
            userid = session['userid']

            #get all tasks.
            p = {'userid':userid}
            response = requests.post('http://127.0.0.1:5000/api/car/issue/list/%s' % (userid,), json=p)
            jobs = json.loads(response.text)
           
            return render_template('engineer_jobs.html', jobs = jobs)
        else:
            return redirect('/profile')
    else:
        return redirect('login')


#Edit selected issue
@site.route('/engineer/issue/edit', methods = ['POST', 'GET', 'PUT'])
def engineerCarIssueUpdate():
    """Changes status of issue when engineer inputs it

    :return: Returns redirection to engineer, or profile, or login
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an engneer or a imposter
        if session['userrole'] == 2:
            msg = ''
            #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'issueid' in request.form and 'carid' in request.form and 'notes' in request.form and 'issue_status' in request.form: #Get contents of post data
                issueid = request.form['issueid']
                #Capture the form data
                notes = request.form['notes']
                issue_status = request.form['issue_status']

                payload = {"notes":notes, "issue_status":issue_status}
                r = requests.put('http://127.0.0.1:5000/api/car/issue/web/%s' % (issueid,) , json=payload)
                

            return redirect('/engineer')
        else:
            return redirect('/profile')
    else:
        return redirect('login')

#get location of car
@site.route('/engineer/carlocation', methods = ['POST', 'GET', 'PUT'])
def engineerCarlocation():
    """Displays car location on google maps, with directions from homebase

    :return: Returns template to engineer_location.html, or redirects
    """
    #Checks to see if user is logged in
    if 'loggedin' in session:
        #Checks to see if user is an engneer or a imposter
        if session['userrole'] == 2:
            msg = ''
            #checking to see if the user has pressed the submit button by looking at POST request
            if request.method == 'POST' and 'carid' in request.form: #Get contents of post data
                    
                #Capture the form data
                carid = request.form['carid']
                #Get cars
                response = requests.get('http://127.0.0.1:5000/api/car/i/%s' % (carid))
                #format the response in json
                car = json.loads(response.text)
                #gcloud key
                key = 'AIzaSyCXZcLU17gaHLQB41T7-zMMM6t2zg1rdh8'
                #office location set to a defult location
                office = "300 collins street melbourne"
                #get the car location from the db
                carlocation = car[0]['location']
                #remove spaces and add + for google url requirments
                office = office.replace(' ','+')
                carlocation = carlocation.replace(' ','+')
                #api end point
                URL = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (carlocation, key)
                # sending get request and saving the response as response object 
                r = requests.get(url = URL) 
                data = json.loads(r.text)
                #Lat and Long for the map to display
                latitude = data['results'][0]['geometry']['location']['lat']
                longitude = data['results'][0]['geometry']['location']['lng']
                
                #api endpint for the directions
                url = 'https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s' % (office, carlocation, key)
                r = requests.get(url = url)
                data = json.loads(r.text)                
                i = 0
                html_instructions = []
                totalduration = data['routes'][0]['legs'][0]['duration']['text']
                while i < len(data['routes'][0]['legs'][0]['steps']):
                    #get length of list to inset at end
                    html_instructions.insert(i ,data['routes'][0]['legs'][0]['steps'][i]['html_instructions'])
                    i += 1

                # creating a map in the view
            return render_template('engineer_location.html', latitude = latitude, longitude = longitude, html_instructions = html_instructions, totalduration = totalduration)

        else:
            return redirect('/profile')
    else:
        return redirect('login')


@site.route('/test', methods = ['POST', 'GET', 'PUT'])
def test():
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 1
    PROMPT_LIMIT = 1

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    for i in range(1):
        for j in range(1):
            print('Guess Speak!')
            ts = recognize_speech_from_mic(recognizer, microphone)
            if ts["transcription"]:
                break
            if not ts["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if ts["error"]:
            print("ERROR: {}".format(ts["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(ts["transcription"]))

        # determine if guess is correct and if any attempts remain
        word = ts["transcription"].lower()
        print("AAA",aaa)
        break
    return render_template('test.html')