# -*- coding: utf-8 -*-
import scrapy
from webspider.items import WebspiderAizhanItem

class AizhanSpider(scrapy.Spider):
    name = "aizhan"
    allowed_domains = ["aizhan.com"]
    start_urls = ['https://ci.aizhan.com/']

    def toHex(self,s):
        lst = []
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)
        return reduce(lambda x,y:x+y, lst)

    def start_requests(self):
        first_word = u'啊'
        url = self.start_urls[0] + self.toHex(first_word) + '/'
        #url = u'https://www.baidu.com/s?wd=百度搜索查询接口&cl=3'
        """
        _csrf=9c866db7c7828fbf5d7143a686b37fb92c88045a987441d831f3ec08b170bdf4a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227_-H_gtIVP3wnC605wUvb5uVRfbd-79R%22%3B%7D;
        userId=1018843;
        userName=798990255%40qq.com;
        userGroup=1;
        userSecure=0s9R%2BC%2Fr4s%2F7RWcD7TbcGD78p2cbY3VVTXqtuc0RXLfD7Av7n%2B%2FAu%2BYjJIT9wjk%2FrfksUA%3D%3D;
        Hm_lvt_b37205f3f69d03924c5447d020c09192=1513565471;
        Hm_lpvt_b37205f3f69d03924c5447d020c09192=1513565491
        """
        cookie_jar={'_csrf':'9c866db7c7828fbf5d7143a686b37fb92c88045a987441d831f3ec08b170bdf4a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227_-H_gtIVP3wnC605wUvb5uVRfbd-79R%22%3B%7D'
                    #,'Hm_lvt_b37205f3f69d03924c5447d020c09192':'1513565471'
                    #,'Hm_lvt_48ab1161bd8d22a908e781b591c6ff51':'1513436785'
                    #,'Hm_lpvt_48ab1161bd8d22a908e781b591c6ff51':'1513436813'
                    ,'userId':'1018843'
                    ,'userName':'798990255%40qq.com'
                    ,'userGroup':'1'
                    ,'userSecure':'0s9R%2BC%2Fr4s%2F7RWcD7TbcGD78p2cbY3VVTXqtuc0RXLfD7Av7n%2B%2FAu%2BYjJIT9wjk%2FrfksUA%3D%3D'
                    #,'Hm_lpvt_b37205f3f69d03924c5447d020c09192':'1513565491'
                    }
        yield scrapy.Request(url=url,
                cookies=cookie_jar,
                callback=self.parse)

    def parse(self, response):
        print response
        print "request_url =========== ", response.url
        for item_word in response.xpath('//td[@class="title"]/a/@title').extract():
            if item_word:
                aizhanitem = WebspiderAizhanItem()
                aizhanitem['word'] = item_word.strip()
                yield aizhanitem
        yield scrapy.Request(url=response.url + "2/", callback=self.pase_next)

    def pase_next(self, response):
        print response
        for item_word in response.xpath('//td[@class="title"]/a/@title').extract():
            if item_word:
                aizhanitem = WebspiderAizhanItem()
                aizhanitem['word'] = item_word.strip()
                yield aizhanitem
