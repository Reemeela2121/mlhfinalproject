import os
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title="BLOBBER", url="localhost:5000/") #OR WE COULD CALL IT BLOBBER
#BLOB ABOUT ANYTHING WITH NEW FRIENDS
@app.route("/login") #methods=('GET', 'POST')
def login():
    return render_template('login.html', title="Login and Sign-up", url=os.getenv("URL"))

@app.route("/register")
def register():
    return render_template("register.html", title="Register", url=os.getenv("URL"))
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

@app.route("/faq")
def faq():
    return render_template('faq.html', title="FAQ", url="faq")

@app.route("/about")
def about():
    return render_template('about.html', title="about", url="about")

   
@app.route("/quiz")
def questionnaire():
    return render_template('questions.html', title="questionnaire", url="quiz")

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title="chat dashboard", url=os.getenv("URL"))

@app.route("/open_chat")
def open_chat():
    return render_template()