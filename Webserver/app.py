from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
 
 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/returnpg")
def returnpg():
    return render_template("return.html")

@app.route('/handle_indexPost', methods=['POST'])
def handle_indexPost():
    if request.method == 'POST':
        artifactType = request.form.get('artifact_type')
        otherInput = request.form.get('artifact_parameters')

        if not isinstance(artifactType, str) or otherInput == "":
            errorMsg = "ERROR: Please select an artifact and give a prompt"
            return render_template('index.html', errorMsg=errorMsg)

        #run the docgen and get output:
        #llmOut = docgen(artifactType, otherInput)
        llmOut = "yo wtf I cannot believe this worked"

        #output result to home.html
        return render_template('home.html', artifactType=artifactType, otherInput=otherInput, llmOut=llmOut)
    else:
        render_template("index.html")
 
if __name__ == "__main__":
   app.run()

from flask import Flask

app = Flask(__name__)
