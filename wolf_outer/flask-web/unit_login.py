from flask import Flask, request
from flask_login import current_user, login_manager, login_required, login_user, logout_user, UserMixin, LoginManager


flask_app = Flask(__name__)
flask_app.secret_key = 'aldfsidi'


login_manager = LoginManager()
login_manager.init_app(flask_app)


@login_manager.user_loader
def load_user(userid):
    return UserObj(100, 'hhh')


class UserObj(UserMixin):
    def __init__(self, _user_id, _user_name):
        self.id = _user_id
        self.user_name = _user_name


@flask_app.route('/login', methods=['GET'])
def login():
    u_id = request.args['user_id']
    u_name = request.args['user_name']
    login_user(UserObj(u_id, u_name))
    return "hello - {} - {}".format(u_id, u_name)


@flask_app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return "logout success"


@flask_app.route('/test1', methods=['GET'])
def test1():
    return "test1"


@flask_app.route('/test2', methods=['GET'])
@login_required
def test2():
    return "test2 {} {}".format(current_user.id, current_user.user_name)


if __name__ == "__main__":
    flask_app.run()




