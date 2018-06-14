# -*- coding: utf-8 -*-
import scrapy

"""
    https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E6%9D%A8%E5%B9%82
    http://sinanews.sina.cn/interface/type_of_search.d.html?callback=initFeed&keyword=%E6%98%8E%E6%98%9F&page=30&type=siftWb&size=20&newpage=0&chwm=&imei=&token=&did=&from=&oldchwm=
"""

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    def parse(self, response):
        pass
