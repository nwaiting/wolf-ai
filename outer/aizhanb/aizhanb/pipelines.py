# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WebspiderPipelineAizhan(object):
    def __init__(self):
        self.file_name = 'aizhan.allwords.data'
        self.savefile = None

    def process_item(self, item, spider):
        """
        """
        self.savefile.write(u"{0}\n".format(item['word']))
        #raise DropItem()

    def open_spider(self,spider):
        try:
            self.savefile = open(self.file_name, 'w')
        except Exception as e:
            print "open file {0} error {1}".format(self.file_name, e)

        print('WebspiderPipelineAizhan open')

    def close_spider(self,spider):
        try:
            self.savefile.close()
        except Exception as e:
            print "close file {0} error {1}".format(self.file_name, e)
        print('WebspiderPipelineAizhan close')
