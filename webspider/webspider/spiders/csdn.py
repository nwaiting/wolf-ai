# -*- coding: utf-8 -*-
import scrapy


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net/']

    def parse(self, response):
        pass


if __name__ == '__main__':
    import json
    a = {'a':'b','c':'d'}
    print json.dumps(a)
