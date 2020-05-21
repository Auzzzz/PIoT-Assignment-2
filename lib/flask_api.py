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
### Users ###
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

# Endpoint to show all people. #ADMIN
@api.route("/api/person", methods = ["GET"])
def getPeople():
    people = Person.query.all()
    result = personsSchema.dump(people)
    print(result)
    return jsonify(result)

# Endpoint to get person by id. #ADMIN
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
    return jsonify({'userid':g.user.userid, 'username':g.user.username, 'email':g.user.email, 'name':g.user.name})
    


### Cars ###
#Car
class Car(db.Model):
    __tablename__ = "cars"
    carid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    colour = db.Column(db.VARCHAR(100))
    seats = db.Column(db.Integer)
    location = db.Column(db.VARCHAR(100))
    cph = db.Column(db.Integer)
    car_make_makeid = db.Column(db.Integer, db.ForeignKey('car_make.makeid'))
    car_type_typeid = db.Column(db.Integer, db.ForeignKey('car_type.typeid'))

def __init__(self, colour, seats, location, cph, car_make_makeid, car_type_typeid ):
        self.colour = colour
        self.seats = seats
        self.location = location
        self.cph = cph
        self.car_make_makeid = car_make_makeid
        self.car_type_typeid = car_type_typeid

class CarSchema(ma.Schema):    
    class Meta:
        # Fields to expose.
        fields = ("carid", "colour", "location", "cph", "car_make_makeid", "car_type_typeid" )

carSchema = CarSchema()
carsSchema = CarSchema(many = True)
#Car Make
class CarMake(db.Model):
    __tablename__ ="car_make"
    makeid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    make = db.Column(db.VARCHAR(100))

    def __init__(self, make):
        self.make = make

class CarMakeSchema(ma.Schema):    
    class Meta:
        # Fields to expose.
        fields = ("makeid", "make")

carmakeSchema = CarMakeSchema()
carmakesSchema = CarMakeSchema(many = True)


#Car Type
class CarType(db.Model):
    __tablename__ ="car_type"
    typeid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    type = db.Column(db.VARCHAR(100))

    def __init__(self, type):
        self.type = type

class CarTypeSchema(ma.Schema):    
    class Meta:
        # Fields to expose.
        fields = ("typeid", "type")

cartypeSchema = CarTypeSchema()
cartypesSchema = CarTypeSchema(many = True)

#Booking
class Booking(db.Model):
    __tablename__ = "booking"
    bookingid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer, db.ForeignKey('users.usersid'))
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid'))
    bdate = db.Column(db.DATE)
    stime = db.Column(db.TIME)
    etime = db.Column(db.TIME)
    bookingstatus = db.Column(db.Integer)

def __init__(self, userid, carid, bdate, stime, etime, bookingstatus ):
        self.userid = userid
        self.carid = carid
        self.bdate = bdate
        self.stime = stime
        self.etime = etime
        self.bookingstatus = bookingstatus

class BookingSchema(ma.Schema):    
    class Meta:
        # Fields to expose.
        fields = ("bookingid", "userid", "carid", "bdate", "stime", "etime", "bookingstatus" )

bookingSchema = BookingSchema()
bookingsSchema = BookingSchema(many = True)

# Get all cars
@api.route("/api/car", methods = ["GET"])
def getCar():
    car = Car.query.all()
    result = carsSchema.dump(car)
    print(result)
    return jsonify(result)

# Get all car makes
@api.route("/api/car/make", methods = ["GET"])
def getMake():
    make = CarMake.query.all()
    result = carmakesSchema.dump(make)
    print(result)
    return jsonify(result)

# Get all car types
@api.route("/api/car/type", methods = ["GET"])
def getType():
    type = CarType.query.all()
    result = cartypesSchema.dump(type)
    print(result)
    return jsonify(result)


# Endpoint to create new car.
@api.route("/api/car", methods = ["POST"])
def addCar():
    seats = request.json["seats"]
    colour = request.json["colour"]
    cph = request.json["cph"]
    location = request.json["location"]
    car_make_makeid = request.json["car_make_makeid"]
    car_type_typeid = request.json["car_type_typeid"]

    newCar = Car(seats = seats, colour = colour, cph = cph, location = location, car_make_makeid = car_make_makeid, car_type_typeid = car_type_typeid)

    db.session.add(newCar)
    db.session.commit()

    return personSchema.jsonify(newCar)
    
    # Endpoint to create new car.
@api.route("/api/car/booking", methods = ["POST"])
def addCarBooking():
    userid = request.json["userid"]
    bdate = request.json["bdate"]
    stime = request.json["stime"]
    etime = request.json["etime"]
    carid = request.json["carid"]
    bookingstatus = request.json["bookingstatus"]

    newCarBooking = Car(userid = userid, bdate = bdate, stime = stime, etime = etime, carid = carid, bookingstatus = bookingstatus)

    db.session.add(newCarBookin)
    db.session.commit()

    return personSchema.jsonify(newCarBooking)
