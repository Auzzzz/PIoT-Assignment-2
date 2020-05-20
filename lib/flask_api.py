from flask import Flask, Blueprint, request, jsonify, render_template, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.hash import sha256_crypt


##https://requests.readthedocs.io/en/master/user/authentication/

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()
auth = HTTPBasicAuth()

# Declaring the model.
class Person(db.Model):
    __tablename__ = "users"
    userid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.VARCHAR)
    username = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(320))
    password = db.Column(db.VARCHAR(200))

    #generate the auth token for login
    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'userid': self.userid})

    #verify password for reg
    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)

    #verify the auth token on retun to the web server
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = Person.query.get(data['userid'])
        return user

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

class PersonSchema(ma.Schema):    
    class Meta:
        # Fields to expose.
        fields = ("userid", "name", "username", "email", "password")

personSchema = PersonSchema()
personsSchema = PersonSchema(many = True)

# Endpoint to show all people.
@api.route("/api/person", methods = ["GET"])
def getPeople():
    people = Person.query.all()
    result = personsSchema.dump(people)
    print(result)
    return jsonify(result)

# Endpoint to get person by id.
@api.route("/api/person/<id>", methods = ["GET"])
def getPerson(id):
    person = Person.query.get(id)

    return personSchema.jsonify(person)

# Endpoint to create new person.
@api.route("/api/person", methods = ["POST"])
def addPerson():
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    password = sha256_crypt.hash(password)
    newPerson = Person(name = name, username = username, email = email, password = password)

    db.session.add(newPerson)
    db.session.commit()

    return personSchema.jsonify(newPerson)

# Endpoint to update person.
@api.route("/api/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = request.json["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/api/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person)

#verify the user password then set the user
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Person.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = Person.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

#end point for token request
@api.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 10})

#end point for login requests
@api.route('/api/login')
@auth.login_required
def get_resource():
    return jsonify({'userid':g.user.userid, 'username':g.user.username})
    



