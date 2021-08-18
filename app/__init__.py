from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv, find_dotenv
import os, requests, random

import random

from main.scores import *
from main.db import setup_db

# load environmental variables
load_dotenv(find_dotenv())


app = Flask(__name__)
app.config["SECRET_KEY"] = "in development"


# initializing Socket IO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)


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
db = SQLAlchemy(app)
migrate = Migrate(app, db)


User, Room = setup_db(db)

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


@app.route("/testing", methods=["GET", "POST"])
def testing():
    if "username" in session:
        current_user = session["username"]

    else:
        return "u r not logged in"

    rows = User.query.count()  # get table length

    own_age = User.query.filter_by(username=current_user).first().age
    own_gender = User.query.filter_by(username=current_user).first().gender
    own_personality = User.query.filter_by(username=current_user).first().sexuality
    own_horoscope = User.query.filter_by(username=current_user).first().horoscope
    own_hobbies = User.query.filter_by(username=current_user).first().hobbies
    own_term = User.query.filter_by(username=current_user).first().term
    own_profession = User.query.filter_by(username=current_user).first().profession
    own_music = User.query.filter_by(username=current_user).first().music

    highest_match_value = -1
    highest_match_id = None
    for i in range(2, rows + 2):
        if User.query.filter_by(id=i).first().username == current_user:
            continue

        match_value = 0
        match_value += age_score(own_age, User.query.filter_by(id=i).first().age)
        match_value += gender_score(own_age, User.query.filter_by(id=i).first().gender)

        match_value += sexuality_score(
            own_age, User.query.filter_by(id=i).first().sexuality
        )
        match_value += horoscope_score(
            own_age, User.query.filter_by(id=i).first().horoscope
        )
        match_value += hobbies_score(
            own_age, User.query.filter_by(id=i).first().hobbies
        )
        match_value += term_score(own_age, User.query.filter_by(id=i).first().term)
        match_value += profession_score(
            own_age, User.query.filter_by(id=i).first().profession
        )

        match_value += music_score(own_age, User.query.filter_by(id=i).first().music)

        if match_value > highest_match_value and match_value > 0:
            highest_match_value = match_value
            highest_match_id = i

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
        username = request.form["username"]
        room = request.form["room"]
        # Store the data in session
        session["username"] = username
        session["room"] = room
        return render_template("chat.html", session=session)
    else:
        if session.get("username") is not None:
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
        # hobbies = request.form.get("hobbies")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = User(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            # session["username"] = username
            return redirect(url_for("login"))

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

        # hobby_array = user.hobbies.split(",")
        # session["hobbies"] = hobby_array
        # first_hobby = random.choice(hobby_array)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session["username"] = username
            # session["room"] = first_hobby
            return redirect(url_for("chat"))

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

    # -= old code =-
    # username = session.get("username")
    # join_room(room)
    # emit("status", {"msg": f"{username} has entered the room."}, room=room)

    join_room(room)

    exists = Room.query.filter_by(room_name=room).first() is not None

    # if error is None:
    #     new_user = User(username, generate_password_hash(password), hobbies)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect(url_for("login"))

    capacity = 2

    if exists:
        if Room.query.filter_by(room_name=room).first().occupancy > capacity:
            print("room has reached capacity")
            return
        Room.query.filter_by(room_name=room).first().occupancy += 1
        db.session.commit()

    else:
        new_room = Room(room, 1)
        db.session.add(new_room)
        db.session.commit()
    current_occupancy = str(Room.query.filter_by(room_name=room).first().occupancy)

    emit(
        "status",
        {
            "msg": session.get("username")
            + " has entered the room. The current occupancy is "
            + current_occupancy
            + "."
        },
        room=room,
    )


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    username = session.get("username")
    msg = message["msg"]
    emit("message", {"msg": f"{username} :  {msg}"}, room=room)


@socketio.on("left", namespace="/chat")
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    username = session.get("username")
    Room.query.filter_by(room_name=room).first().occupancy -= 1
    db.session.commit()

    leave_room(room)
    session.clear()
    emit("status", {"msg": f"{username} has left the room."}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True, host="localhost", port=5000)
