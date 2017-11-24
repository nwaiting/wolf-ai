# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from urlparse import urljoin
from webspider.items import WebspiderPipelineIqiyiItem

class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    allowed_domains = ['iqiyi.com']
    page_pre = 'http://list.iqiyi.com'
    start_urls = ['http://list.iqiyi.com/']

    def parse(self, response):
        response.body.decode("utf-8", "ignore")
        print response
        res = response.xpath('//a[starts-with(@class,"a1") and @data-key="down"]/@href').extract()
        if len(res) > 0:
            yield Request(url=urljoin(self.page_pre, res[0]), callback=self.parse)

        webiqiyi = WebspiderPipelineIqiyiItem()
        for item in response.xpath('//div[@class="wrapper-piclist"]//li'):
            webiqiyi['name'] = item.xpath('//p/a/text()').extract()[0]
            webiqiyi['score'] = item.xpath('//span[@class="score"]/strong/text()').extract()[0]
            webiqiyi['score'] += item.xpath('//span[@class="score"]/text()').extract()[0]
            vipinfo = item.xpath('//span[@class="icon-vip-zx"]').extract()
            if len(vipinfo) > 0:
                webiqiyi['isvip'] = "1"
            else:
                webiqiyi['isvip'] = "0"

            actors = u'主演:'
            for actor in item.xpath('//div[@class="role_info"]/em/a/text()').extract():
                actors += actor.strip() + "+"
            webiqiyi['actors'] = actors
            yield webiqiyi
