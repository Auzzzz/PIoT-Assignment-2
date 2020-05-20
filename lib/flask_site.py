from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import sha256_crypt
import os, requests, json

site = Blueprint("site", __name__)
### User ###
# Client webpage.
@site.route("/")
def index():
    # Use REST API.
    response = requests.get("http://192.168.0.199:5000/person/")
    data = json.loads(response.text)

    return render_template("index.html", people = data)

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
            r = requests.post('http://192.168.0.199:5000/api/person', json=payload)
            print(r.text)
        else:
            msg = "Passwords do not match"
    elif request.method == 'POST':
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('register.html', msg=msg)

@site.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Capture the form data
        username = request.form['username']
        password = request.form['password']
        msg = ''
        if username is None or password is None:
            msg = "Username or Password empty"
        else:
            #send user details of
            response = requests.get('http://192.168.0.199:5000/api/token', auth=(username, password))
            #make response into json format
            data = json.loads(response.text)
            #take token out of json and submit it for access to user info
            token = data['token']
            response = requests.get('http://192.168.0.199:5000/api/login', auth=(token, 'unused'))
            #format the response in json
            data = json.loads(response.text)

    return render_template('index.html', msg = msg)