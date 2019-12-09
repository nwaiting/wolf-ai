from .. import models
from flask import Blueprint

user = Blueprint('user', __name__)


@user.route('/login', methods=[POST])
def login():
    db.session.add()
    db.session.commit()
    db.session.close()

    user_list = db.session.query(User).all()
    db.session.close()