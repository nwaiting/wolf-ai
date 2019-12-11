from flask_sqlalchemy import SQLAlchemy
from .user import User

db = SQLAlchemy(session_options={
        'autocommit': True,
        'autoflush': True,
        'expire_on_commit': True,
        })

# 创建时带的参数即为使用时，不用db.session.commit()和db.session.close()