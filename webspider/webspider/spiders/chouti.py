# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.http.cookies import CookieJar
import urlparse

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.cn']
    page_pre = 'http://dig.chouti.com'
    start_urls = ['http://dig.chouti.com/all/hot/recent/1']

    cookie_dict = dict()

    def parse(self, response):
        print "response ", response
        cookiejar = CookieJar()
        cookiejar.extract_cookies(response, response.request)
        for k, v in cookiejar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        # to to ...
        #for con in response.xpath('//div[@class="part1"]/a[starts-with(@class,"show-content")]/@href').extract():
        #    print con.strip()

        for item in response.xpath('//div[@class="news-content"]'):
            print "item ", item
            print item.xpath('*/a[@class="show-content color-chag"]/@href').extract()

        res = response.xpath('//a[@class="ct_page_edge"]/@href').extract()
        next_page = None
        if len(res) > 1:
            next_page = res[-1]
        else:
            next_page = res[0]

        # yield Request(url=urlparse.urljoin(self.page_pre, next_page),
        #     cookies=self.cookie_dict,
        #     callback=self.parse,
        #     dont_filter=True)
