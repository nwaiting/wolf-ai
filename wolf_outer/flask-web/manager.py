from app import creat_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


flask_app = creat_app()
manager = Manager(flask_app)
migrate = Migrate(flask_app, db)

"""
    python manager.py db init
    python manager.py db migrate
    python manager.py db upgrade
"""
manager.add_command('db', MigrateCommand)


@manager.command
def custom(args):
    """
    执行命令： python manager.py custom 123
    :param args:
    :return:
    """
    print("custom args {}".format(args))


@manager.option('-n', '--name', dest='name')
@manager.option('-u', '--url', dest='url')
def op_cmds(name, url):
    """
    执行命令：python manager.py op_cmds -n aaa -u http:localhost:8080/login
    :param name:
    :param url:
    :return:
    """
    print("name {} url {}".format(name, url))


if __name__ == "__main__":
    """
    启动任务：python manager.py runserver
    带参数的运行：python manager.py runserver --help 查看具体参数
    """
    manager.run()





