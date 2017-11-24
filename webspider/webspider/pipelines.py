# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class WebspiderPipeline(object):
    def __init__(self,v=None):
        self.value = v

    def process_item(self, item, spider):
        #to do 存储等
        print 'WebspiderPipeline process'
        return item

    @classmethod
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:
        :return:
        """
        #val = crawler.settings.getint('MMMM')
        #return cls(val)
        return cls()

    def open_spider(self,spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        print('WebspiderPipeline open')

    def close_spider(self,spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        print('WebspiderPipeline close')

class WebspiderPipelineIqiyi(object):
    def __init__(self):
        self.file_name = 'iqiyi.log'
        self.savefile = None
        pass

    def process_item(self, item, spider):
        #to do 存储等
        #from webspider.items import WebspiderPipelineIqiyiItem
        #item = WebspiderPipelineIqiyiItem()
        s = "{0}, {1}, {2}, {3}".format(item.name, item.score, item.actors, item.isvip)
        self.savefile.write(s)
        #raise DropItem()

    def open_spider(self,spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        try:
            self.savefile = open(self.file_name, 'w')
        except Exception as e:
            print "open file {0} error {1}".format(self.file_name, e)

        print('WebspiderPipelineIqiyi open')

    def close_spider(self,spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        try:
            self.savefile.close()
        except Exception as e:
            print "close file {0} error {1}".format(self.file_name, e)
        print('WebspiderPipelineIqiyi close')