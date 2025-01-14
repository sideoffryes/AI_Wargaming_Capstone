# navigate to the environment directory and do ".\Scripts\activate"
# navigate to the directory with the flask file and do "python app.py"

from flask import Flask, render_template
 
app = Flask(__name__)
 
 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")
 
if __name__ == "__main__":
   app.run()

from flask import Flask

app = Flask(__name__)
