from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = "in development"

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
        user=os.getenv("POSTGRES_USER"),
        passwd=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=5432,
        table=os.getenv("POSTGRES_DB"),
    )

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
