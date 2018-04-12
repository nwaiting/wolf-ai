#coding=utf8

"""
荣耀v10，oppo r15， vivo x21，小米mix2 销量最好的
'http://item.jd.com/5821455.html',
'http://item.jd.com/6773559.html',
'http://item.jd.com/6708229.html',
'http://item.jd.com/5001209.html'
"""

import scrapy
from scrapy.http import Request
from webspider.items import WebspiderJDItem
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JDSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    start_urls = ['http://item.jd.com/5821455.html',]

    def start_requests(self):
        url = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv19694&productId=5821455&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0&rid=0'
        for i in range(101):
            new_url = url.format(i)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = response.body
        first_index = contents.find('{')
        last_index = contents.rfind('}')
        if first_index != -1 and last_index != -1:
            contents = contents[first_index:last_index+1]

        json_content = None
        try:
            json_content = json.loads(contents)
        except Exception as e:
            print('json error {0}'.format(e))
            return
        if json_content.has_key('comments'):
            for item in json_content['comments']:
                if item.has_key('content'):
                    jditem = WebspiderJDItem()
                    jditem['comments'] = item['content']
                    yield jditem


















a
