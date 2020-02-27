### sqlalchemy
- **概述：**
>
>        db+scheme://user:password@host:port/dbname
>

- **连接配置通用格式：**
>        db+scheme://user:password@host:port/dbname
>
>
>
>

- **flask_sqlalchemy 配置：**
>       SQLALCHEMY_TRACK_MODIFICATIONS
>           如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
>
>
>
>
>
>
>
>
>
>
>
>

- **查询使用：**
>       查询支持原生和对象的查询模式
>           1、原生查询
>           2、对象查询
>
>       返回值：
>           fetchall()  获取全部
>           fetchone()  获取一个
>               返回结果：(13,)  获取结果：res[0]
>           返回值是一个list类型，如:
>           [('bb113f50-6e6a-470c', 1575869478), ('9ec5bd99-2fdd-4b9b-9e08', 1575870644)]
>           可以通过数组或者字典获取
>

- **SQLAlchemy tuple to mysql WHERE IN:**
>       参考：http://www.cocoachina.com/articles/62792     SQLAlchemy WHERE IN单值(原始SQL)
>           https://blog.xupeng.me/2013/09/25/mysqldb-args-processing/      MySQLdb 参数处理的坑
>

- **如何在models定义两个不同数据库，表名相同（__tablename__）的class？**
>       class AAA(db.Model):
>           __bind_key__ = 'db1'
>           __tablename__ = 'hello'
>
>       class BBB(db.Model):
>           __bind_key__ = 'db2'
>           __tablename__ = 'hello'
>           metadata = MetaData()
>
>       flask sqlalchemy 如何在models定义两个不同数据库，表名相同（__tablename__）的class
>       定义不同的 metadata 就可以了
>
>
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/huchong/p/8274510.html       Flask-SQLAlchemy常用操作
>           https://www.cnblogs.com/chen0427/p/8783817.html     Sqlalchemy limit, offset slice操作
>           https://www.jianshu.com/p/d08a63170714      灵活使用 SQLAlchemy 中的 ORM 查询
>           https://www.cnblogs.com/shangerzhong/articles/10381793.html     Flask-----sqlalchemy 增删改查操作
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
