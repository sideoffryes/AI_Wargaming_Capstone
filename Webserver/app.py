from flask import Flask, render_template, request, redirect, session
import secrets
from flask_sqlalchemy import SQLAlchemy
from docGen import gen
import os
from datetime import timedelta

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# This is used to sign the session data
app.config['SECRET_KEY'] = os.urandom(24)

# Set session expiry to 1 day
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Models
class Profile(db.Model):
    # Id : Field which stores unique id for every row in database table.
    # username: Used to store the username of the user
    # hash: Used to store hashed password+salt of the user
    # salt: Used to store the salt of the hash
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    hash = db.Column(db.Integer, unique=False)
    salt = db.Column(db.String(16), unique=False, nullable=False)

    # repr method represents how one object of this datatable will look like
    def __repr__(self):
        return f"Username: {self.username}, Hash: {self.hash}, Salt: {self.salt}"

# Initialize the database
with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/output")
@app.route("/output.html")
def home():
    return render_template("output.html")

@app.route("/login")
@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register")
@app.route("/register.html")
def createAcc():
    return render_template("register.html")

@app.route('/logout')
def logout():
    # Remove 'user_id' from session
    session.pop('user_id', None)
    # Redirect to login page
    errorMsg = "Successfully logged out of profile"
    return render_template('login.html', errorMsg=errorMsg)

@app.route('/handle_indexPost', methods=['POST'])
def handle_indexPost():
    if request.method != 'POST':
        errorMsg = "ERROR: Something went wrong, please try again."
        return render_template('index.html', errorMsg=errorMsg)
    
    else:
        artifactType = request.form.get('artifact_type')
        otherInput = request.form.get('artifact_parameters')

        if not isinstance(artifactType, str) or otherInput == "":
            errorMsg = "ERROR: Please select an artifact and give a prompt"
            return render_template('index.html', errorMsg=errorMsg)

        #run the docgen and get output:
        llmOut = gen(2, int(artifactType), otherInput)

        #output result to home.html
        return render_template('output.html', artifactType=artifactType, otherInput=otherInput, llmOut=llmOut)

@app.route('/handle_loginPost', methods=['POST'])
def handle_loginPost():
    if request.method != 'POST':
        errorMsg = "ERROR: Something went wrong, please try again."
        return render_template('index.html', errorMsg=errorMsg)
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        # check credentials:
        # use the username to get the hash and salt from the database
        user = Profile.query.filter_by(username = username).first()
        userHash = user.hash
        userSalt = user.salt

        # combine the given password and salt
        saltedPass = password + userSalt

        # hash the combination
        hashedGiven = hash(saltedPass)

        # compare the given hash with the database hash
        # if they are the same, then create a temporary cookie
        if hashedGiven == userHash:
            session['user_id'] = user.id
            errorMsg = "Successfully logged into: " + username
            return render_template('index.html', errorMsg=errorMsg)
        # else say error and reload the login page with error message
        else:
            errorMsg = "ERROR: Given login credentials were incorrect, please try again."
            return render_template('login.html', errorMsg=errorMsg)

@app.route('/handle_registerPost', methods=['POST'])
def handle_registerPost():
    if request.method != 'POST':
        errorMsg = "ERROR: Something went wrong, please try again."
        return render_template('register.html', errorMsg=errorMsg)
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        # generate salt
        # 8 bytes * 2 characters per byte = 16 characters
        salt = secrets.token_hex(8)

        # combine password and salt
        combo = password + salt

        # hash the combination
        hashed = hash(combo)

        # store the username, hash, and salt in the database
        user = Profile(username = username, passHash = hashed, passSalt = salt)
        db.session.add(user)
        db.session.committ()

        # go to login page and tell user to login
        errorMsg = "NOTICE: Please login using previously created username and password."
        return render_template('login.html', errorMsg=errorMsg)
 
@app.route("/instructions")
@app.route("/instructions.html")
def instructions():
    return render_template("instructions.html")
 
if __name__ == "__main__":
   app.run(port=5000, host="0.0.0.0", debug=True)