# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from dbhandler import DBManager


class DhseedPipeline(object):
    def process_item(self, item, spider):
        sql = "INSERT INTO EMPLOYEE() VALUES ()".format('Mac', 'Mohan', 20, 'M', 2000)

        db = DBManager.get_db()
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        return item






