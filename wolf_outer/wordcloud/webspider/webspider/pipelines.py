# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

class WebspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class WebspiderPipelineJD(object):
    def __init__(self):
        self.file_name = 'jd.allwords.data'
        self.savefile = None

    def process_item(self, item, spider):
        """
            comments = scrapy.Field()
            referenceName = scrapy.Field()
            referenceTime = scrapy.Field()
            productColor = scrapy.Field()
            productSize = scrapy.Field()
        """
        tmp_dict = {}
        tmp_dict['comments'] = item['comments']
        tmp_dict['referenceName'] = item['referenceName']
        tmp_dict['referenceTime'] = item['referenceTime']
        tmp_dict['productColor'] = item['productColor']
        tmp_dict['productSize'] = item['productSize']
        self.savefile.write(u"{0}\n".format(json.dumps(tmp_dict)))
        #raise DropItem()

    def open_spider(self,spider):
        try:
            self.savefile = open(self.file_name, 'w')
        except Exception as e:
            print("open file {0} error {1}".format(self.file_name, e))

        print('WebspiderPipelineJD open')

    def close_spider(self,spider):
        try:
            self.savefile.close()
        except Exception as e:
            print("close file {0} error {1}".format(self.file_name, e))
        print('WebspiderPipelineJD close')
