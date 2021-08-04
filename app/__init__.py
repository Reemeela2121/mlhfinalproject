
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title="BLOBBER", url="localhost:5000") #OR WE COULD CALL IT BLOBBER
#BLOB ABOUT ANYTHING WITH NEW FRIENDS
@app.route("/login") #methods=('GET', 'POST')
def login():
    return render_template()

#not sure if I want loading as a whole render template and rather as just a transition to next page
@app.route("/loading")
def loading_screen():
    return render_template()

@app.route("/create_profile")
def create_profile():
    return render_template()

@app.route("/profile")
def profile():
    return render_template()

@app.route("/quiz")
def questionnaire():
    return render_template()

@app.route("/dashboard")
def chat_dashboard():
    return render_template()

@app.route("/open_chat")
def open_chat():
    return render_template()