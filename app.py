#from flask import Flask
#
#app = Flask(__name__)
#
#@app.route('/')
#def index():
#	return "Hello World"
#
#if __name__ == "__main__":
#	app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '34.87.245.145'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'banana192'
app.config['MYSQL_DB'] = 'carshare'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html', msg='')