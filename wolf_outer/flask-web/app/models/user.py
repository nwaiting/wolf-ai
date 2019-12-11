from flask_sqlalchemy import Model
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String


class User(Model, UserMixin):
    user_id = Column(Integer, unique=True)
    user_name = Column(String(32))
    create_time = Column(Integer)


