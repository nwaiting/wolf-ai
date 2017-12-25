# -*- coding: utf-8 -*-
import scrapy
import requests
from aizhanb.items import WebspiderAizhanItem
from aizhanb.settings import WORDS_SOURCE_DIR, USERS_COOKIE_INFO
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
    cookie_user_sec = ''
    cookie_user_id = ''
    cookie_user_name = ''
    def toHex(self,s):
        lst = list()
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0' + hv
            if len(hv) == 2:
                hv = 'n' + hv
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
        if not os.path.exists(USERS_COOKIE_INFO):
            print "!!!!!!!!!!!!!! file {0} not exists".format(USERS_COOKIE_INFO)
            return

        with open(USERS_COOKIE_INFO, 'rb') as f:
            contens = f.read()
            first_index = contens.find('userSecure')
            if first_index != -1:
                first_contents = contens[first_index:]
                second_index = first_contents.find('=')
                third_index = first_contents.find(';')
                if second_index != -1:
                    self.cookie_user_sec = first_contents[second_index+1:third_index]
                    print "user secret ", self.cookie_user_sec

            first_index = contens.find('userId')
            if first_index != -1:
                first_contents = contens[first_index:]
                second_index = first_contents.find('=')
                third_index = first_contents.find(';')
                if second_index != -1:
                    self.cookie_user_id = first_contents[second_index+1:third_index]
                    print "user id ", self.cookie_user_id

            first_index = contens.find('userName')
            if first_index != -1:
                first_contents = contens[first_index:]
                second_index = first_contents.find('=')
                third_index = first_contents.find(';')
                if second_index != -1:
                    self.cookie_user_name = first_contents[second_index+1:third_index]
                    print "user name ", self.cookie_user_name

        with open(WORDS_SOURCE_DIR, 'rb') as f:
            for line in f.xreadlines():
                if line:
                    line = line.strip()
                    trans_code = self.toHex(unicode(line, 'utf-8'))
                    print u'start get {0} {1}'.format(line, trans_code)
                    url = self.start_urls[0] + trans_code + '/'
                    """
                    """
                    self.cookie_jar={'userId':'{0}'.format(self.cookie_user_id)
                                ,'userName':'{0}'.format(self.cookie_user_name)
                                ,'userGroup':'1'
                                ,'userSecure':'{0}'.format(self.cookie_user_sec)
                                }
                    yield scrapy.Request(url=url,
                            cookies=self.cookie_jar,
                            callback=self.parse)

    def parse(self, response):
        #print response
        for item_word in response.xpath('//td[@class="title"]/a/@title').extract():
            if item_word:
                item_word = item_word.strip()
                print u'{0}'.format(item_word)
                if self.maybeTieba(item_word):
                    aizhanitem = WebspiderAizhanItem()
                    aizhanitem['word'] = item_word.strip()
                    yield aizhanitem
        yield scrapy.Request(url=response.url + "2/", cookies=self.cookie_jar, callback=self.pase_next)

    def pase_next(self, response):
        #print response
        for item_word in response.xpath('//td[@class="title"]/a/@title').extract():
            if item_word:
                item_word = item_word.strip()
                print u'{0}'.format(item_word)
                if self.maybeTieba(item_word):
                    aizhanitem = WebspiderAizhanItem()
                    aizhanitem['word'] = item_word.strip()
                    yield aizhanitem
