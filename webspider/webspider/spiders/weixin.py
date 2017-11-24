# -*- coding: utf-8 -*-
import scrapy


class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com']
    start_urls = ['http://weixin.sogou.com/']

    def parse(self, response):
        #response.body.decode('utf-8','ignore')
        for result in response.xpath('//div[starts-with(@class, "txt-box")]'):
            print result.xpath('./h3/a/@href').extract()
            print result.xpath('./p/text()').extract()
