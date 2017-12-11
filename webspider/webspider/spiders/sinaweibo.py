# -*- coding: utf-8 -*-
import scrapy


class SinaweiboSpider(scrapy.Spider):
    name = 'sinaweibo'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    def parse(self, response):
        pass
