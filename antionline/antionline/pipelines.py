# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from dbhandler import DBManager
from settings import BOT_NAME
from datetime import datetime

class AntionlinePipeline(object):
    def process_item(self, item, spider):
        sql = "INSERT INTO {0}(id, art_title, art_content, art_from, art_author, art_read, art_pub_time, art_create_time) ".format('db_' + BOT_NAME)
        sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        args = (0, 
               item['art_title'],
               item['art_content'],
               item['art_from'],
               item['art_author'],
               item['art_read'],
               item['art_pub_time'],
               datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               )   
        db = DBManager.get_db()
        cursor = db.cursor()
        try:
            cursor.execute(sql, args)
            db.commit()
        except Exception as e:
            print "error {0} sql {1}".format(e, sql)
            db.rollback()
