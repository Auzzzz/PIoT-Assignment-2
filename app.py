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
import re
from lib.db_connection import DB
app = Flask(__name__)

# Secrect key for sec
app.secret_key = 'your secret key'
### User ###
# Login #
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
        with DB() as db:
            account = db.loginUser(username,password)
            
            if account:
                # If account exists in database
                # Create session data to keep track of user 
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[2]
                # move user to home page 
                return redirect(url_for('home'))
            else:
                msg='Password or Username incorrect'
    #dispay the login form and any message
    return render_template('index.html', msg=msg)

# Logout #
@app.route('/logout')
def logout():
    #remove all session data to log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    #move to login page
    return redirect(url_for('login'))


##Register #
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
        email = request.form['email']

        #check the DB if the user exsits // Add here if we need
        #Add account into the DB
        with DB() as db:
            if(db.insertUser(name, username, email, password)):
                msg = 'Error.... Oh Well'
            else:
                msg = 'Congratz You have been registered......'
    elif request.method == 'POST':
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('register.html', msg=msg)

# Home Page #
@app.route('/home')
def home():
    if 'loggedin' in session:
        #When the user is logged in show them this top secret page
        return render_template('home.html', username=session['username'])
    #If not bye bye
    return redirect(url_for('login'))

# Profile Page #
@app.route('/profile')
def profile():
    # check if the user is logged in
    if 'loggedin' in session:
        # get account info
        with DB() as db:
            account = db.accountUser(id = session['id'])
            print(account)
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

### Cars ###
# insert car #
@app.route('/newcar', methods=['GET', 'POST'])
def newcar():
    carmake = DB().getCarMake()
    cartype = DB().getCarType()
    #error message
    msg = ''
    #checking to see if the user has pressed the submit button by looking at POST request
    if request.method == 'POST': #and 'colour' in request.form and 'seats' in request.form and 'cph' in request.form and 'email' in request.form:
    #Capture the form data
        colour = request.form['colour']
        seats = request.form['seats']
        location = request.form['location']
        cph = request.form['cph']
        cmake = request.form['cmake']
        ctype = request.form['ctype']
        #check the DB if the user exsits // Add here if we need
        #Add account into the DB
        with DB() as db:
            if(db.insertNewCar(colour, seats, location, cph, cmake, ctype)):
                msg = 'Error.... Oh Well'
            else:
                msg = 'Congratz You have been registered......'
    elif request.method == 'POST':
            #error message
            msg = 'Fill the form out you ido*'
    return render_template('newcar.html', carmake=carmake, cartype=cartype, msg=msg)
