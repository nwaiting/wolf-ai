# -*- coding: utf-8 -*-
import scrapy


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://zhaopin.com/']
    start_first_url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&p=1&isadv=0'

    def start_requests(self):
        yield scrapy.Request(url=self.start_first_url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath('//table[@cellpadding="0"]'):
            pass
