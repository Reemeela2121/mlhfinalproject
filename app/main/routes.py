from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from flask import Flask, escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


# initialize the database
db = SQLAlchemy()
# migrate = Migrate(main, db)

# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


@main.route("/")
def index():
    return "Welcome"


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["room"] = form.room.data
        return redirect(url_for(".chat"))
    elif request.method == "GET":
        form.name.data = session.get("name", "")
        form.room.data = session.get("room", "")
    return render_template("dashboard.html", form=form)


@main.route("/chat")
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get("name", "")
    room = session.get("room", "")
    if name == "" or room == "":
        return redirect(url_for(".index"))
    return render_template("chat.html", name=name, room=room)


# @main.route("/")
# def index():
#     if "username" in session:
#         username = session["username"]
#     else:
#         username = ""
#     return render_template(
#         "index.html", title="BLOBBER", url="localhost:5000", username=username
#     )  # OR WE COULD CALL IT BLOBBER


@main.route("/register", methods=["GET", "POST"])
def register():
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
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("register.html", error=error)

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error=error)

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
