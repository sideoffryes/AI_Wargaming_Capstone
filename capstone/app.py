import datetime
import hashlib
import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy

from docGen import gen

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
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, unique=False)
    salt = db.Column(db.String, unique=False, nullable=False)

    # One-to-many relationship: A user can have many generated artifacts
    generated_artifacts = db.relationship('GeneratedArtifact', backref='user', lazy=True)

    # repr method represents how one object of this datatable will look like
    def __repr__(self):
        return f"Username: {self.username}, Hash: {self.hash}, Salt: {self.salt}"
    
class GeneratedArtifact(db.Model):
    # Unique ID for each generated artifact
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to the Profile table
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    # The prompt used to generate the artifact
    prompt = db.Column(db.Text, nullable=False)
    # The generated artifact (text)
    content = db.Column(db.Text, nullable=False)
    # Timestamp for when the artifact was created
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<GeneratedArtifact {self.id} for User {self.user_id}>"

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    .. http:get:: /
        :undocumented:

    .. http:get:: /index
        :undocumented:

    .. http:post:: /index

    **Description:** Handles the submission of the artifact generation form. Based on the form data, it either returns an error message or triggers the artifact generation process and redirects to the output page.

    **Request Body (Form Data):**

    The request body is sent as `application/x-www-form-urlencoded` and contains the following fields:

    * `artifact_type` (integer, required): An integer representing the type of artifact to generate.
    * `model_selection` (integer, required): An integer representing the chosen language model.
    * `artifact_parameters` (string, required if `artifact_type` is not 4): Free-form text providing parameters for the artifact generation.
    * `opord_orientation` (string, required if `artifact_type` is 4): Orientation field for OPORD generation.
    * `opord_situation` (string, required if `artifact_type` is 4): Situation field for OPORD generation.
    * `opord_mission` (string, required if `artifact_type` is 4): Mission field for OPORD generation.
    * `opord_execution` (string, required if `artifact_type` is 4): Execution field for OPORD generation.
    * `opord_admin` (string, required if `artifact_type` is 4): Administration field for OPORD generation.
    * `opord_logistics` (string, required if `artifact_type` is 4): Logistics field for OPORD generation.
    * `opord_command` (string, required if `artifact_type` is 4): Command and Signal field for OPORD generation.

    **Request Body Example (Generic Artifact):**

    .. code-block:: http

        POST /index HTTP/1.1
        Content-Type: application/x-www-form-urlencoded

        artifact_type=2&model_selection=1&artifact_parameters=Provide%20a%20brief%20summary%20of%20the%20topic.

    **Request Body Example (OPORD Artifact):**

    .. code-block:: http

        POST /index HTTP/1.1
        Content-Type: application/x-www-form-urlencoded

        artifact_type=4&model_selection=2&opord_orientation=Terrain%20and%20Weather...&opord_situation=Enemy%20forces...&opord_mission=Conduct%20an%20attack...&opord_execution=Phase%201...&opord_admin=Supply%20point...&opord_logistics=Transportation...&opord_command=Commander's%20intent...

    **Response (Redirect - 302 Found):**

    On successful form submission and artifact generation, the server typically redirects the user to the `/output` route (not documented here) to display the generated artifact.

    :statuscode 302: Found
        :description: Redirects to the `/output` page upon successful artifact generation.

    **Response (Error - 200 OK with HTML):**

    If the `artifact_type` or `model_selection` are missing in the form data, the server returns the `index.html` template with an error message.

    :statuscode 200: OK
        :contenttype text/html:
        :example:

            .. code-block:: html

            <!DOCTYPE html>
            <html>
            <head>
                <title>Artifact Generator</title>
            </head>
            <body>
                <h1>Generate Artifact</h1>
                <p style="color: red;">ERROR: Please select an artifact, model type, and give a prompt.</p>
                </body>
            </html>
    """
    if request.method == 'POST':
        artifactType = request.form.get('artifact_type')
        llmChosen = request.form.get('model_selection')

        # Validation check
        if (artifactType is None) or (llmChosen is None):
            errorMsg = "ERROR: Please select an artifact, model type, and give a prompt."
            return render_template('index.html', errorMsg=errorMsg)
        
        artifactType = int(artifactType)
        llmChosen = int(llmChosen)

        if artifactType == 4:
            #get all inputs
            orientation = request.form.get('opord_orientation')
            situation = request.form.get('opord_situation')
            mission = request.form.get('opord_mission')
            execution = request.form.get('opord_execution')
            admin = request.form.get('opord_admin')
            logistics = request.form.get('opord_logistics')
            command = request.form.get('opord_command')
            #combine them and put into otherInput
            otherInput = f"{orientation}[SEP]{situation}[SEP]{mission}[SEP]{execution}[SEP]{admin}[SEP]{logistics}[SEP]{command}"
            # otherInput = f"Orientation: {orientation}; Situation: {situation}; Mission: {mission}; Execution: {execution}; Administration: {admin}; Logistics: {logistics}; Command and Signal: {command}"
        else:
            otherInput = request.form.get('artifact_parameters')

        # Check if it's a debug artifact
        if artifactType == 1:
            llmOut = "You selected the DEBUG ARTIFACT and gave this prompt: " + otherInput + " Here is a bunch of random numbers: " + str(hash(otherInput))
        else:
            # Run the docgen and get output
            llmOut = gen(llmChosen, artifactType - 1, otherInput)

        if 'user_id' in session:
            user_id = session['user_id']
            new_artifact = GeneratedArtifact(user_id=user_id, prompt=otherInput, content=llmOut)
            db.session.add(new_artifact)
            db.session.commit()

        return render_template('output.html', artifactType=artifactType, otherInput=otherInput, llmOut=llmOut)
    else:
        # If GET request, just render the form
        return render_template("index.html")

@app.route("/output")
def home():
    return render_template("output.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check credentials:
        # use the username to get the hash and salt from the database
        user = Profile.query.filter_by(username = username).first()
        if user is None:
            errorMsg = "ERROR: That username does not exist, please try again."
            return render_template('login.html', errorMsg=errorMsg)
        userHash = user.hash
        userSalt = user.salt

        # hash the combination
        hashedGiven = hashlib.sha256(userSalt + password.encode()).hexdigest()

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
        
    return render_template("login.html")

@app.route("/userprofile", methods=['GET', 'POST'])
def userprofile():
    user_id = session.get('user_id')

    if not user_id:
        return render_template("userprofile.html", username="Not logged in", errorMsg="", successMsg="")

    # Fetch user from database
    user = Profile.query.filter_by(id=user_id).first()

    # Initialize messages
    errorMsg = ""
    successMsg = ""

    if request.method == 'POST':
        current_password = request.form.get('curpwd')
        new_password = request.form.get('newpwd')
        confirm_password = request.form.get('conpwd')

        # Validate current password
        if not user or not current_password or not new_password or not confirm_password:
            errorMsg = "ERROR: Please fill out all fields."
            return render_template("userprofile.html", username=user.username, errorMsg=errorMsg, successMsg=successMsg)

        # Check if current password matches the stored hash
        hashed_given = hashlib.sha256(user.salt + current_password.encode()).hexdigest()
        if hashed_given != user.hash:
            errorMsg = "ERROR: Current password is incorrect."
            return render_template("userprofile.html", username=user.username, errorMsg=errorMsg, successMsg=successMsg)

        # Check if new password and confirm password match
        if new_password != confirm_password:
            errorMsg = "ERROR: New passwords do not match."
            return render_template("userprofile.html", username=user.username, errorMsg=errorMsg, successMsg=successMsg)

        # Generate new salt and hash the new password
        new_salt = os.urandom(16)
        new_hashed_password = hashlib.sha256(new_salt + new_password.encode()).hexdigest()

        # Update user password
        user.salt = new_salt
        user.hash = new_hashed_password
        db.session.commit()

        successMsg = "Password successfully changed."
        return render_template("userprofile.html", username=user.username, errorMsg=errorMsg, successMsg=successMsg)

    return render_template("userprofile.html", username=user.username, errorMsg=errorMsg, successMsg=successMsg)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')

        # Check if the username already exists in the database
        existing_user = Profile.query.filter_by(username=username).first()

        if existing_user:
            errorMsg = "ERROR: This username already exists. Please use a different one."
            return render_template('new_account.html', errorMsg=errorMsg)

        password = request.form.get('ogpassword')
        passwordRetype = request.form.get('repassword')

        if password != passwordRetype:
            errorMsg = "ERROR: The passwords did not match."
            return render_template('new_account.html', errorMsg=errorMsg)

        # generate salt
        salt = os.urandom(16)

        # hash the combination
        hashed = hashlib.sha256(salt + password.encode()).hexdigest()

        # store the username, hash, and salt in the database
        user = Profile(username = username, hash = hashed, salt = salt)
        db.session.add(user)
        db.session.commit()

        # go to login page and tell user to login
        errorMsg = "NOTICE: Please login using previously created username and password."
        return render_template('login.html', errorMsg=errorMsg)

    return render_template("new_account.html")

@app.route('/logout')
def logout():
    # Remove 'user_id' from session
    session.pop('user_id', None)
    # Redirect to login page
    errorMsg = "Successfully logged out of profile"
    return render_template('index.html', errorMsg=errorMsg)
 
@app.route('/my_artifacts', methods=['GET'])
def my_artifacts():
    if 'user_id' not in session:
        errorMsg = "NOTICE: Please login to see your generated artifacts."
        return render_template('login.html', errorMsg=errorMsg)

    # Retrieve the logged-in user's ID from the session
    user_id = session['user_id']

    # Query all generated artifacts for the logged-in user
    user_artifacts = GeneratedArtifact.query.filter_by(user_id=user_id).all()

    # If no artifacts are found, inform the user
    if not user_artifacts:
        errorMsg = "NOTICE: There are no artifacts associated with this account."
        return render_template('index.html', errorMsg=errorMsg)

    # Render the artifacts to the user (you can format this as needed)
    return render_template('my_artifacts.html', artifacts=user_artifacts)

@app.route("/docs/<path:filename>")
def docs(filename):
    return send_from_directory("../docs/build/html", filename)
 
if __name__ == "__main__":
   app.run(port=5050, host="0.0.0.0", debug=True)
