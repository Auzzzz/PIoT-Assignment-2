# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from MasterPi.lib.flask_api import api, db
from MasterPi.lib.flask_site import site
from flask import Flask
from flask_googlemaps import GoogleMaps

app = Flask(__name__, template_folder='MasterPi/lib/templates')
basedir = os.path.abspath(os.path.dirname(__file__))
GoogleMaps(app)

# Update HOST and PASSWORD appropriately.
HOST = "34.87.245.145"
USER = "root"
PASSWORD = "banana123"
DATABASE = "carshare"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '8sOGgEM1Ie2gFer4wMlYbSahMeuf0cki'

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)


if __name__ == "__main__":
    app.run(host = "127.0.0.1", debug = True)
