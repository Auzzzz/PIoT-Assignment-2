from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Person(db.Model):
    __tablename__ = "users"
    userid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.VARCHAR)
    username = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(320))
    password = db.Column(db.VARCHAR(200))

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
@api.route("/person", methods = ["GET"])
def getPeople():
    people = Person.query.all()
    result = personsSchema.dump(people)
    print(result)
    return jsonify(result)

# Endpoint to get person by id.
@api.route("/person/<id>", methods = ["GET"])
def getPerson(id):
    person = Person.query.get(id)

    return personSchema.jsonify(person)

# Endpoint to create new person.
@api.route("/person", methods = ["POST"])
def addPerson():
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    newPerson = Person(name = name, username = username, email = email, password = "hello")

    db.session.add(newPerson)
    db.session.commit()

    return personSchema.jsonify(newPerson)

# Endpoint to update person.
@api.route("/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = request.json["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person)
