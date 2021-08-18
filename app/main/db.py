from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def setup_db(db):
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

        def __init__(self, username, password):
            # def __init__(self, username, password, pronouns, age, gender, sexuality, personality, horoscope, hobbies, term, profession, music):
            self.username = username
            self.password = password

        # self.pronouns = pronouns

        #        self.age = age
        #        self.gender = gender
        #        self.sexuality = sexuality
        #        self.personality = personality  # introvert / extrovert / ambivert
        #        self.horoscope = horoscope
        #        self.hobbies = hobbies
        #        self.term = term  # long term friend or short term friend
        #        self.profession = profession
        #        self.music = music  # music taste

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

    return (User, Room)
