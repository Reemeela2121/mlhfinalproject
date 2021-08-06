from flask import Flask, render_template, session, escape, request, redirect, url_for
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
import os

main = Flask(__name__)

load_dotenv(find_dotenv())

# add database
main.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)
main.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
main.secret_key = "secret-key"
main.config["SECRET_KEY"] = "mysecret"

# initialize the database
db = SQLAlchemy(main)
migrate = Migrate(main, db)

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


# not sure if I want loading as a whole render template and rather as just a transition to next page
@main.route("/loading")
def loading_screen():
    return render_template()


@main.route("/create_profile")
def create_profile():
    return render_template()


@main.route("/profile")
def profile():
    return render_template()


@main.route("/quiz")
def questionnaire():
    return render_template()


@main.route("/open_chat")
def open_chat():
    return render_template()
