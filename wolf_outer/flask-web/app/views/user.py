from app.models import db, User
from flask import Blueprint

user = Blueprint('user', __name__)


@user.route('/login', methods=["POST"])
def login():
    db.session.add()
    db.session.commit()
    db.session.close()

    user_list = db.session.query(User).all()
    for row in user_list:
        print(row)
    return "OK"
