from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from dotenv import load_dotenv, find_dotenv
import os, requests

import random

# load environmental variables
load_dotenv(find_dotenv())


app = Flask(__name__)
app.config["SECRET_KEY"] = "in development"


# initializing Socket IO
socketio = SocketIO(app, async_mode=None)

# add database
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the database
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    hobbies = db.Column(db.String(), nullable=False)

    def __init__(self, username, password, hobbies):
        self.username = username
        self.password = password
        self.hobbies = hobbies

    def __repr__(self):
        return f"<User {self.username}>"


# Google reCaptcha sitekey
# site_key = os.getenv("SITE_KEY")

# reCaptcha verification
# def is_human(captcha_response):
#     secret = os.getenv("SECRET_KEY")
#     payload = {"response": captcha_response, "secret": secret}
#     response = requests.post(
#         "https://www.google.com/recaptcha/api/siteverify", data=payload
#     )
#     response_text = response.json()
#     return response_text["success"]

# matching algorithm
def match(own_hobbies, current_user_hobbies):
    own_hobbies_arr = own_hobbies.split(", ")
    current_user_hobbies_arr = current_user_hobbies.split(", ")
    common = list(set(own_hobbies_arr).intersection(current_user_hobbies_arr))
    return len(common)


@app.route("/testing", methods=["GET", "POST"])
def testing():
    if "username" in session:
        current_user = session["username"]
        print(current_user)
        print(User.query.filter_by(username=current_user).first().hobbies)
    else:
        return "u r not logged in"
    own_hobbies = User.query.filter_by(username=current_user).first().hobbies
    rows = User.query.count()
    highest_match_value = -1
    highest_match_id = None
    for i in range(2, rows + 2):
        if User.query.filter_by(id=i).first().username == current_user:
            continue
        current_user_hobbies = User.query.filter_by(id=i).first().hobbies
        match_value = match(own_hobbies, current_user_hobbies)
        if match_value > highest_match_value and match_value > 0:
            highest_match_value = highest_match_value
            highest_match_id = i
        print(current_user_hobbies)
    if highest_match_id == None:
        return "you r forever alone"
    return (
        "Your best match is with user: "
        + User.query.filter_by(id=highest_match_id).first().username
    )


# Home page
@app.route("/")
def index():
    return render_template("index.html", title="BLOBBER", url="localhost:5000")


# dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


# chat-room
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        room = request.form["room"]
        # Store the data in session
        session["room"] = room
        return render_template("chat.html", session=session)
    else:
        if session.get("username") is not None:
            session["room"] = random.choice(session.get("hobbies", "didn't work"))
            return render_template("chat.html", session=session)
        else:
            return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hobbies = request.form.get("hobbies")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not hobbies:
            error = "Hobbies is required."
        elif User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = User(username, generate_password_hash(password), hobbies)
            db.session.add(new_user)
            db.session.commit()
            # session["username"] = username
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error=error)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = User.query.filter_by(username=username).first()
        hobby_array = user.hobbies.split(",")
        session["hobbies"] = hobby_array
        # first_hobby = random.choice(hobby_array)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session["username"] = username
            # session["room"] = first_hobby
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ", url="faq")


@app.route("/about")
def about():
    return render_template("about.html", title="about", url="about")


@app.route("/quiz")
def questionnaire():
    return render_template("questions.html", title="questionnaire", url="quiz")


# @app.route("/loading")
# def loading_screen():
#     return render_template()


# @app.route("/create_profile")
# def create_profile():
#     return render_template()


# @app.route("/profile")
# def profile():
#     return render_template()


# SocketIO events
@socketio.on("join", namespace="/chat")
def join(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    join_room(room)
    emit(
        "status", {"msg": session.get("username") + " has entered the room."}, room=room
    )


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    emit(
        "message", {"msg": session.get("username") + " : " + message["msg"]}, room=room
    )


@socketio.on("left", namespace="/chat")
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    username = session.get("username")
    leave_room(room)
    session.clear()
    emit("status", {"msg": f"{username} has left the room."}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)
