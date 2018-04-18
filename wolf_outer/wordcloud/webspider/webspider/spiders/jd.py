#coding=utf8

"""
荣耀v10，oppo r15， vivo x21，小米mix2 销量最好的
'http://item.jd.com/5821455.html',
'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv19694&productId=5821455&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0&rid=0'
'http://item.jd.com/6773559.html',
'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1870&productId=6773559&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0'
'http://item.jd.com/6708229.html',
'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4587&productId=6708229&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0'
'http://item.jd.com/5001209.html'
'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv53841&productId=5001209&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0'
"""

import scrapy
from scrapy.http import Request
from webspider.items import WebspiderJDItem
import json

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
url_v10 = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv19694&productId=5821455&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0&rid=0'
url_r15 = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1870&productId=6773559&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0'
url_x21 = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4587&productId=6708229&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0'
url_mix2 = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv53841&productId=5001209&score=3&sortType=5&page={0}&pageSize=10&isShadowSku=0'

class JDSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    start_urls = ['http://item.jd.com/5821455.html',]

    def start_requests(self):
        url = url_v10
        for i in range(101):
            new_url = url.format(i)
            yield Request(url=new_url, callback=self.parse)

    def parse(self, response):
        contents = response.body.decode(response.encoding)
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
        if 'comments' in json_content:
            for item in json_content['comments']:
                jditem = WebspiderJDItem()
                jditem['comments'] = ''
                if 'content' in item:
                    jditem['comments'] = item['content']
                jditem['referenceName'] = ''
                if 'referenceName' in item:
                    jditem['referenceName'] = item['referenceName']
                jditem['referenceTime'] = ''
                if 'referenceTime' in item:
                    jditem['referenceTime'] = item['referenceTime']
                jditem['productColor'] = ''
                if 'productColor' in item:
                    jditem['productColor'] = item['productColor']
                jditem['productSize'] = ''
                if 'productSize' in item:
                    jditem['productSize'] = item['productSize']
                yield jditem
