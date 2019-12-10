from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, unique=True)
    user_name = db.Column(db.String(32))
    create_time = db.Column(db.Integer)


