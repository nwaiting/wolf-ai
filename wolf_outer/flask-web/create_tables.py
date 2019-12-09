from app import flask_app
from app.models import sql_model

# 离线创建数据库表脚本

# 注意：在sql_model=SQLAlchemy()创建之前，需要先到导入所有的数据表的model模块

with flask_app.app_context():   #加载配置信息到local中，然后在create_all()中会被调用
    sql_model.create_all()

