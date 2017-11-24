# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class OschinaSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['oschina.net']
    user_pre = 'http://oschina.net'
    start_urls = ['http://www.oschina.net/news/industry']

    def parse(self, response):
        print "start ", response
        for url in response.xpath('//div[@class="main-info box-aw"]/a/@href').extract():
            print url
        re_url = 'http://www.oschina.net/action/ajax/get_more_news_list?newsType=industry&p='
        for i in xrange(2,5):
            new_url = re_url + str(i)
            yield Request(url=new_url, callback=self.parse)
