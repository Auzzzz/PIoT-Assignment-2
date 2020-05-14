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
from passlib.hash import sha256_crypt

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

        #get password from database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select password from users where username = %s', (username,))
        passFromDB = cursor.fetchone()
        cursor.close()
        hashedPass = ""

        #check if password matches
        if sha256_crypt.verify(password, passFromDB['password']):
            hashedPass = passFromDB['password']

        #Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users where username = %s and password = %s', (username, hashedPass,))
        account = cursor.fetchone()
        cursor.close()
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

### Logout ###
@app.route('/logout')
def logout():
    #remove all session data to log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    #move to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
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

        #check the DB if the user exsits
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users where username = %s', (username,))
        account = cursor.fetchone()

        #if the account exists
        if account:
            msg = 'Username is already taken'
        elif password != confirmPass:
            msg = 'Passwords do not match'
        else:
            #Add account into the DB
            hashedPass = sha256_crypt.hash(password)
            cursor.execute("insert into users values (NULL, %s, %s, %s, %s, NULL, NULL)", (name, username, email, hashedPass,)) ##TODO: add password hashing
            mysql.connection.commit()
            msg = 'Registration successful!'
    elif request.method == 'POST':
            #error message
            msg = 'Please fill out the form correctly'
    return render_template('register.html', msg=msg)
