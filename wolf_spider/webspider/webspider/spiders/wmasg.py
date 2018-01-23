# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class WmasgSpider(scrapy.Spider):
    name = 'wmasg'
    allowed_domains = ['wmasg.pl']
    urls_pre = 'http://wmasg.pl'
    start_urls = ['http://wmasg.pl/']

    def parse(self, response):
        print response
        for item in response.xpath('//div[@class="precontent"]/h2/a/@href').extract():
            print item
        for i in xrange(2,706):
            yield Request(url=self.urls_pre + '/?page=' + str(i), callback=self.parse)
