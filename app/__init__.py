from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from dotenv import load_dotenv, find_dotenv
import os, requests, random

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

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String())
    occupancy = db.Column(db.Integer, nullable=False)

    def __init__(self, room_name, occupancy):
        self.room_name = room_name
        self.occupancy = occupancy

    def __repr__(self):
        return f'{self.id},{self.room_name}'

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    pronouns = db.Column(db.String(), nullable=True)

    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(), nullable=True)
    personality = db.Column(db.String(), nullable=True)
    zodiac = db.Column(db.String(), nullable=True)
    # hobbies = db.Column(db.String(), nullable=True)
    term = db.Column(db.String(), nullable=True)
    profession = db.Column(db.String(), nullable=True)
    music = db.Column(db.String(), nullable=True)


    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.pronouns = None

        self.age = None
        self.gender = None
        self.sexuality = None
        self.personality = None # introvert / extrovert / ambivert
        self.zodiac = None
        self.hobbies = None
        self.term = None # long term friend or short term friend
        self.profession = None
        self.music = None # music taste

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

def age_score(own_age, other_age):
    if own_age == None or other_age == None:
        return 0
    diff = abs(own_age - other_age)
    if diff == 0:
        diff = 1
    return 5/diff

def gender_score(own_gender, other_gender):
    if own_gender == None or other_gender == None:
        return 0
    if own_gender == other_gender:
        return 3
    else:
        return 1

def personality_score(own_personality, other_personality):
    if own_personality == None or other_personality == None:
        return 0
    if own_personality == other_personality:
        return 3
    elif own_personality == 'ambivert' or other_personality == 'ambivert':
        return 1.5
    else:
        return 0

def zodiac_score(own_zodiac, other_zodiac): # i dont believe in zodiacs but this is kinda fun
    if own_zodiac == None or other_zodiac == None:
        return 0
    if (own_zodiac == 'cancer' or other_zodiac == 'cancer') and (own_zodiac == 'saggitarius' or other_zodiac == 'saggitarius'):
        return 3
    elif (own_zodiac == 'taurus' or other_zodiac == 'taurus') and (own_zodiac == 'pisces' or other_zodiac == 'pisces'):
        return 3
    elif (own_zodiac == 'gemini' or other_zodiac == 'gemini') and (own_zodiac == 'capricorn' or other_zodiac == 'capricorn'):
        return 3
    elif (own_zodiac == 'libra' or other_zodiac == 'libra') and (own_zodiac == 'leo' or other_zodiac == 'leo'):
        return 3
    elif (own_zodiac == 'scorpio' or other_zodiac == 'scorpio') and (own_zodiac == 'aries' or other_zodiac == 'aries'):
        return 3
    elif (own_zodiac == 'virgo' or other_zodiac == 'virgo') and (own_zodiac == 'aquarius' or other_zodiac == 'aquarius'):
        return 3
    else:
        return 0

def hobby_score(own_hobbies, other_hobbies):
    if own_hobbies == None or other_hobbies == None:
        return 0
    own_hobbies_arr = own_hobbies.split(", ")
    other_hobbies_arr = other_hobbies.split(", ")
    common = list(set(own_hobbies_arr).intersection(other_hobbies_arr))
    return len(common)

def term_score(own_term, other_term):
    if own_term == None or other_term == None:
        return 0
    if own_term == other_term:
        return 4
    else:
        return 0

def profession_score(own_profession, other_profession):
    if own_profession == None or other_profession == None:
        return 0
    if own_profession == other_profession:
        return 3
    else:
        return 0

def music_score(own_music, other_music):
    if own_music == None or other_music == None:
        return 0
    own_music_arr = own_music.split(", ")
    other_music_arr = other_music.split(", ")
    common = list(set(own_music_arr).intersection(other_music_arr))
    return len(common)


def get_match():
    if "username" in session:
        current_user = session["username"]

    else:
        return "u r not logged in"
    rows = User.query.count() # get table length

    own_age = User.query.filter_by(username=current_user).first().age
    own_gender = User.query.filter_by(username=current_user).first().gender
    own_zodiac = User.query.filter_by(username=current_user).first().zodiac
    # own_hobbies = User.query.filter_by(username=current_user).first().hobbies
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
        match_value += zodiac(own_zodiac, User.query.filter_by(id=i).first().zodiac)

        # match_value += hobbies_score(own_age, User.query.filter_by(id=i).first().hobbies)
        match_value += term_score(own_age, User.query.filter_by(id=i).first().term)
        match_value += profession_score(own_age, User.query.filter_by(id=i).first().profession)
        match_value += music_score(own_age, User.query.filter_by(id=i).first().music)

        if match_value > highest_match_value and match_value > 0:
            highest_match_value = match_value
            highest_match_id = i

    if highest_match_id == None:
        return "you r forever alone"

    return (User.query.filter_by(id=highest_match_id).first().username)


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


@app.route("/questions", methods=["GET", "POST"])
def questionnaire():
    if request.method == "POST":
        age = request.form.get("age")
        gender = request.form.get("gender")
        zodiac = request.form.get("zodiac")
        personality = request.form.get("personality")
        music = request.form.get("music")
        term = request.form.get("term")
        current_user = session["username"]

        User.query.filter_by(username=current_user).first().age = age
        User.query.filter_by(username=current_user).first().gender = gender
        User.query.filter_by(username=current_user).first().zodiac = zodiac
        User.query.filter_by(username=current_user).first().personality = personality
        User.query.filter_by(username=current_user).first().music = music
        User.query.filter_by(username=current_user).first().term = term

        db.session.commit()

        print(User.query.filter_by(username=current_user).first().age)

        best_match = get_match()
        return(best_match)
    return render_template("questions.html", title="questionnaire", url="questions")



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


    exists = Room.query.filter_by(room_name=room).first() is not None


        # if error is None:
        #     new_user = User(username, generate_password_hash(password), hobbies)
        #     db.session.add(new_user)
        #     db.session.commit()
        #     return redirect(url_for("login"))

    capacity = 2

    if exists:
        if Room.query.filter_by(room_name=room).first().occupancy >= capacity:
            print("room has reached capacity")
            return
        Room.query.filter_by(room_name=room).first().occupancy += 1
        db.session.commit()

    else:
        new_room = Room(room, 1)
        db.session.add(new_room)
        db.session.commit()
    current_occupancy = str(Room.query.filter_by(room_name=room).first().occupancy)

    join_room(room)

    emit(
        "status", {"msg": session.get("username") + " has entered the room. The current occupancy is " + current_occupancy + "."}, room=room
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
    Room.query.filter_by(room_name=room).first().occupancy -= 1
    db.session.commit()

    leave_room(room)
    session.clear()
    emit("status", {"msg": f"{username} has left the room."}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)
