

class BaseConfig(object):
    """mysql db"""
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_HOST = '192.168.0.104'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'web1'
    mysql_url = 'mysql+mysqlconnector://%s:%s@%s:%d/%s?charset=utf8' % (
        MYSQL_USER,
        MYSQL_PASSWORD,
        MYSQL_HOST,
        MYSQL_PORT,
        MYSQL_DATABASE
    )
    SQLALCHEMY_DATABASE_URI = mysql_url
    """sqlalchemy默认数据库连接uri"""
    SQLALCHEMY_BINDS = {
        'session': mysql_url,
        'sessionschedule': mysql_url,
        'task': mysql_url,
        'result': mysql_url,
        'tguser': mysql_url,
        'phonetag': mysql_url,
        'tgusertag': mysql_url,
        'tguseridtag': mysql_url,
        'tgusernametag': mysql_url,
        'tgphoneinfolatest': mysql_url,
        'userbackend': mysql_url,
        'department': mysql_url,
    }

    """sqlalchemy每个表对应数据库连接uri"""
    SQLALCHEMY_AUTOCOMMIT = True
    SQLALCHEMY_AUTOFLUSH = True
    SQLALCHEMY_EXPIRE_ON_COMMIT = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    """是否输出详细sql信息，调试时使用"""
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False



