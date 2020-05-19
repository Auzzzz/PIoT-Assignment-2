from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import sha256_crypt
import os, requests, json

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
def index():
    # Use REST API.
    response = requests.get("http://192.168.0.199:5000/person/")
    data = json.loads(response.text)

    return render_template("index.html", people = data)

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

        #validate if password matches with confirmPass
        if password == confirmPass:
            #hash the Password
            hashedPass = sha256_crypt.hash(password)

            #check the DB if the user exsits // Add here if we need
            #Add account into the DB
            requests.post('http://192.168.0.199/person', json={"name":name, "username":username, "password":password, "email":email})
            
        else:
            msg = "Passwords do not match"
    elif request.method == 'POST':
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('register.html', msg=msg)

