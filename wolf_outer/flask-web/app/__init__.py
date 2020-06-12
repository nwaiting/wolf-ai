from flask import Flask
from app.models import db


def creat_app():
    _app = Flask(__name__)
    db.init_app(_app)

    return _app


flask_app = creat_app()




