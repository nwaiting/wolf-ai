# -*- coding: utf-8 -*-
import scrapy


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.cn']
    start_urls = ['http://chouti.cn/']

    def parse(self, response):
        pass
