from flask import Flask, render_template, session, escape, request, redirect, url_for
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
import os

app = Flask(__name__)

load_dotenv(find_dotenv())

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
app.secret_key = "secret-key"
app.config["SECRET_KEY"] = "mysecret"

# initialize the database
db = SQLAlchemy(app)
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
    return "Your best match is with user: " + User.query.filter_by(id=highest_match_id).first().username

@app.route("/")
def index():
    if "username" in session:
        username = session["username"]
    else:
        username = ""
    return render_template(
        "index.html", title="BLOBBER", url="localhost:5000", username=username
    )  # OR WE COULD CALL IT BLOBBER

@app.route("/register", methods=["GET", "POST"])
def register():
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
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("register.html", error=error)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
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


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# not sure if I want loading as a whole render template and rather as just a transition to next page
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


if __name__ == "__main__":
    app.run(debug=True)
