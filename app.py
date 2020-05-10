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

#https://flask.palletsprojects.com/en/1.1.x/quickstart/
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Secrect key for sec
app.secret_key = 'your secret key'

### Database Conn ###
app.config['MYSQL_HOST'] = '34.87.245.145'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'banana192'
app.config['MYSQL_DB'] = 'carshare'

# Intialize MySQL
mysql = MySQL(app)

### Login ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    #error message
    msg = ''
    #Check for when user submits form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Capture the form data
        username = request.form['username']
        password = request.form['password']
        
        #Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users where username = %s and password = %s', (username, password,))
        account = cursor.fetchone()
        # If account exists in database
        if account:
            # Create session data to keep track of user 
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # move user to home page 
            return 'Logged in successfully!' #currently testing
        else:
            #error message
            msg = 'Incorrect username/password!'
    #dispay the login form and any message
    return render_template('index.html', msg=msg)