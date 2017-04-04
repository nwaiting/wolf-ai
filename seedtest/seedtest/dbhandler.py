#!/usr/bin/env python
# coding: utf-8

"""
@file: dbhandler.py
@time: 2017/4/1 14:50
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from settings import db_host, db_passwd, db_user, db_port, db_name, BOT_NAME

class DBManager(object):
    g_db = None
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        if not DBManager.g_db:
            DBManager.g_db = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_passwd, db=db_name, charset='utf8')
            sql = "CREATE TABLE IF NOT EXISTS {0}(" \
                  "id int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增长id'," \
                  "art_title VARCHAR(1024) NOT NULL COMMENT 'article title'," \
                  "art_content MediumText NULL COMMENT 'article content'," \
                  "art_from VARCHAR(1024) NULL COMMENT 'article from',"\
                  "art_author VARCHAR(1024) NULL COMMENT 'article author'," \
                  "art_read int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'article read num'," \
                  "art_pub_time VARCHAR(1024) NULL COMMENT '文章发布时间'," \
                  "art_create_time datetime NULL COMMENT '入库时间'," \
                  "PRIMARY KEY (`id`)" \
                  ") ENGINE=InnoDB DEFAULT CHARSET=utf8;".format('db_' + BOT_NAME)
            cursor = DBManager.g_db.cursor()
            try:
                cursor.execute(sql)
                print "sql {}".format(sql)
                DBManager.g_db.commit()
            except Exception as e:
                print "except {}".format(e)
                DBManager.g_db.rollback()
        return DBManager.g_db

    @staticmethod
    def release_db():
        if DBManager.g_db:
            DBManager.g_db.close()


if __name__ == "__main__":
    DBManager.get_db()
    DBManager.release_db()


