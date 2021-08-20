from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import requests
from dotenv import load_dotenv, find_dotenv


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


# Database Schema
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    pronouns = db.Column(db.String(), nullable=True)

    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(), nullable=True)
    sexuality = db.Column(db.String(), nullable=True)
    personality = db.Column(db.String(), nullable=True)
    horoscope = db.Column(db.String(), nullable=True)
    hobbies = db.Column(db.String(), nullable=True)
    term = db.Column(db.String(), nullable=True)
    profession = db.Column(db.String(), nullable=True)
    music = db.Column(db.String(), nullable=True)

    def __init__(self, username, password, pronouns):
        self.username = username
        self.password = password
        self.pronouns = pronouns

    def __repr__(self):
        return f"<User {self.username}>"


# Room Model
class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String())
    occupancy = db.Column(db.Integer, nullable=False)

    def __init__(self, room_name, occupancy):
        self.room_name = room_name
        self.occupancy = occupancy

    def __repr__(self):
        return f"{self.id},{self.room_name}"


# Google reCaptcha sitekey
site_key = os.getenv("SITE_KEY")


# reCaptcha verification
def is_human(captcha_response):
    secret = os.getenv("RECAP_KEY")
    payload = {"response": captcha_response, "secret": secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=payload
    )
    response_text = response.json()
    return response_text["success"]


# Routes

# Home page
@app.route("/")
def index():
    return render_template("index.html", title="BLOBBER")


# dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session.get("username") is None:
        return redirect(url_for("login"))
    username = session.get("username")
    pronouns = session.get("pronouns")
    if request.method == "POST":
        session["room"] = request.form.get("hobbies")
        return redirect(url_for("chat"))

    return render_template("dashboard.html", username=username, pronouns=pronouns)


# chat-room
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if session.get("username") is not None:
        return render_template("chat.html", session=session)
    else:
        return redirect(url_for("login"))


# user register
@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        pronouns = request.form.get("pronouns")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        captcha_response = request.form["g-recaptcha-response"]

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif password != password2:
            error = "Password not the same."
        elif User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if is_human(captcha_response):

            if error is None:
                new_user = User(username, generate_password_hash(password), pronouns)
                db.session.add(new_user)
                db.session.commit()
                flash("Congratulations, you are now a registered user of blobber chat!")
                return redirect(url_for("login"))

        else:
            error = "reCaptcha required."
    return render_template("register.html", error=error, site_key=site_key)


# user login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if "username" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form["g-recaptcha-response"]
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif password is None:
            error = "Incorrect password."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if is_human(captcha_response):
            if error is None:
                session["username"] = username
                session["pronouns"] = user.pronouns
                return redirect(url_for("dashboard"))

        else:
            error = "reCaptcha required."
    return render_template("login.html", error=error, site_key=site_key)


# user logout
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


@app.errorhandler(404)
def page_not_found(e):
    return "<h1> Not Found</h1>", 404


# SocketIO events
@socketio.on("join", namespace="/chat")
def join(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""

    room = session.get("room")
    username = session.get("username")
    join_room(room)
    emit("status", {"msg": f"{username} has entered the room."}, room=room)


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
    # Room.query.filter_by(room_name=room).first().occupancy -= 1
    # db.session.commit()
    leave_room(room)
    session.clear()
    emit("status", {"msg": f"{username} has left the room."}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True, host="localhost", port=5000)
