# -*- coding: utf-8 -*-
import scrapy
import requests
from aizhanb.items import WebspiderAizhanItem
from aizhanb.settings import WORDS_SOURCE_DIR
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging
logging.getLogger('requests').setLevel(logging.ERROR)

class AizhanSpider(scrapy.Spider):
    name = "aizhanb"
    allowed_domains = ["aizhan.com"]
    start_urls = ['https://ci.aizhan.com/']
    cookie_jar = {}
    def toHex(self,s):
        lst = list()
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)
        return reduce(lambda x,y:x+y, lst)

    def maybeTieba(self, checkword):
        requests_baidu_pre = 'https://www.baidu.com/s?wd={0}&cl=3'
        req_headers = {'user-agent':'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2'}

        new_url = requests_baidu_pre.format(checkword)
        res = requests.get(url=new_url, headers=req_headers)
        if res.status_code == 200:
            if res.text.find('<span class="c-showurl">tieba.baidu.com') != -1:
                return True
        return False

    def start_requests(self):
        if not os.path.exists(WORDS_SOURCE_DIR):
            print "!!!!!!!!!!!! file {0} not exists".format(WORDS_SOURCE_DIR)
            return
        with open(WORDS_SOURCE_DIR, 'rb') as f:
            for line in f.xreadlines():
                if line:
                    line = line.strip()
                    trans_code = self.toHex(unicode(line, 'utf-8'))
                    print u'start get {0} {1}'.format(line, trans_code)
                    url = self.start_urls[0] + trans_code + '/'
                    """
                    _csrf=9c866db7c7828fbf5d7143a686b37fb92c88045a987441d831f3ec08b170bdf4a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227_-H_gtIVP3wnC605wUvb5uVRfbd-79R%22%3B%7D;
                    userId=1018843;
                    userName=798990255%40qq.com;
                    userGroup=1;
                    userSecure=0s9R%2BC%2Fr4s%2F7RWcD7TbcGD78p2cbY3VVTXqtuc0RXLfD7Av7n%2B%2FAu%2BYjJIT9wjk%2FrfksUA%3D%3D;
                    Hm_lvt_b37205f3f69d03924c5447d020c09192=1513565471;
                    Hm_lpvt_b37205f3f69d03924c5447d020c09192=1513565491
                    """
                    self.cookie_jar={'userId':'1018843'
                                ,'userName':'798990255%40qq.com'
                                ,'userGroup':'1'
                                ,'userSecure':'RXC7jh5E5%2Fnjw3NYMj3F4McV%2B36Mnp2E5UXyxB1Ex6%2BCLzpCavJAL8FbZEp2p9OA'
                                }
                    yield scrapy.Request(url=url,
                            cookies=self.cookie_jar,
                            callback=self.parse)

    def parse(self, response):
        #print response
        for item_word in response.xpath('//td[@class="title"]/a/@title').extract():
            if item_word:
                item_word = item_word.strip()
                print item_word
                if self.maybeTieba(item_word):
                    aizhanitem = WebspiderAizhanItem()
                    aizhanitem['word'] = item_word.strip()
                    yield aizhanitem
        yield scrapy.Request(url=response.url + "2/", cookies=self.cookie_jar,callback=self.pase_next)

    def pase_next(self, response):
        print response
        for item_word in response.xpath('//td[@class="title"]/a/@title').extract():
            if item_word:
                item_word = item_word.strip()
                print "======", item_word
                if self.maybeTieba(item_word):
                    aizhanitem = WebspiderAizhanItem()
                    aizhanitem['word'] = item_word.strip()
                    yield aizhanitem
