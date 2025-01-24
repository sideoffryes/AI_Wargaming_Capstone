from flask import Flask, render_template, request, redirect, session

from scripts.docGen import gen

app = Flask(__name__)

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
        llmOut = gen(1, int(artifactType), otherInput)
        #llmOut = "yo wtf I cannot believe this worked"

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
        #check credentials
        #if valid, then create a temporary cookie
        #else say error and reload the login page with error message
 
if __name__ == "__main__":
   app.run()

from flask import Flask

app = Flask(__name__)
