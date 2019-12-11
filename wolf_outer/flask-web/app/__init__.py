from flask import Flask
from app.models import db


def creat_app():
    flask_app = Flask(__name__)
    db.init_app(flask_app)

    return flask_app