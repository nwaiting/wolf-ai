# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class Bbsc114Pipeline(object):
    def process_item(self, item, spider):
        print "enter Bbsc114Pipeline {0}, type {1}".format(item, type(item))
        with open("a.txt", 'a+') as f:
            f.write(json.dumps(dict(item), ensure_ascii=False) + "\n")

