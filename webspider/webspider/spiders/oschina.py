# -*- coding: utf-8 -*-
import scrapy


class OschinaSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['oschina.net']
    start_urls = ['http://oschina.net/']

    def parse(self, response):
        pass
