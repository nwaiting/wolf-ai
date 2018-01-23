# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse
import re
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import FengleItem

class DhseedSpider(scrapy.Spider):
    name = "fengle"
    allowed_domains = ["fengle.com.cn"]
    base_url = "http://www.fengle.com.cn/list"
    detail_base_url = 'http://www.fengle.com.cn'
    start_urls = ( 
        'http://www.fengle.com.cn/list/?116_1.html',
        'http://www.fengle.com.cn/list/?118_1.html',
        'http://www.fengle.com.cn/list/?135_1.html',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        for new_url in response.xpath("//div[@class='wp-pagenavi']/select/option/@value").extract():
            new_url = urlparse.urljoin(self.base_url, new_url)
            print "new_url {}".format(new_url)
            yield scrapy.Request(new_url, callback=self.parse)

        for detailurl in response.xpath("//div[@class='sright_c']/ul/li/a/@href").extract():
            detailurl = urlparse.urljoin(self.base_url, detailurl)
            print "detailurl {}".format(detailurl)
            yield scrapy.Request(detailurl, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = FengleItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''

        details = response.xpath("//div[@class='content2']")
        a_title = details.xpath("div/h1/text()").extract()
        if len(a_title) > 0:
            bitem['art_title'] = a_title[0]
        
        a_read = details.xpath("div/span/font/script/@src").extract()
        if len(a_read) > 0:
            new_url = urlparse.urljoin(self.detail_base_url, a_read[0])
            r = requests.get(new_url, timeout=2)
            s = r.content
            index_1 = s.find("(")
            index_2 = s.find(")")
            if index_2 > index_1:
                bitem['art_read'] = s[index_1 + 1:index_2]

        a_ds = details.xpath("div/span/text()").extract()
        if len(a_ds) > 0:
            # 来源: | 发布时间:2017-3-24 17:33:55 | 浏览次数：
            s = a_ds[0]
            index_1 = s.find(":")
            index_2 = s.find("|")
            index_3 = s.rfind("|")
            if index_2 > index_1 and index_3 > index_2:
                bitem['art_from'] = s[index_1 + 1:index_2].strip()
                b_s = s[index_2 + 1: index_3].strip()
                index_4 = b_s.find(":")
                if index_4 != -1:
                    bitem['art_pub_time'] = b_s[index_4 + 1:]

        for ite in details.xpath("div[@class='scont']/p/text()").extract():
            bitem['art_content'] += ite

        if not bitem['art_content']:
            for ite in details.xpath("div[@class='scont']/div/text()").extract():
                bitem['art_content'] += ite

        if not bitem['art_content']:
            for ite in details.xpath("div[@class='scont']/p/span/font/text()").extract():
                bitem['art_content'] += ite

        if not bitem['art_content']:
            for ite in details.xpath("div[@class='scont']/p/span/text()").extract():
                bitem['art_content'] += ite

        if not bitem['art_content']:
            print "content null {}".format(response.url)

        yield bitem


