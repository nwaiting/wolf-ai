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
from items import Dh31Item

class Dh31Spider(scrapy.Spider):
    name = "dh31"
    allowed_domains = ["31dh.com"]
    base_url = "http://www.31dh.com"
    news_base_url = "http://www.31dh.com/news/"
    pro_base_url = "http://www.31dh.com/pro/"
    start_urls = ( 
        'http://www.31dh.com/news/news.asp?ClassID=1',
        'http://www.31dh.com/pro/pro.asp?ClassID=5',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        for new_url in response.xpath("//div[@class='left_content']/div[@class='fenlei']/ul/li/a/@href").extract():
            if new_url.startswith(".."):
                new_url = new_url[2:]
            new_url = urlparse.urljoin(self.base_url, new_url)
            print "new_url {}".format(new_url)
            yield scrapy.Request(new_url, callback=self.parse)

        for detailurl in response.xpath("//div[@class='page_nav']/select[@id='jumpMenu']/option/@value").extract():
            if response.url.find("news.asp") != -1:
                detailurl = urlparse.urljoin(self.news_base_url, detailurl)
            if response.url.find("pro.asp") != -1:
                detailurl = urlparse.urljoin(self.pro_base_url, detailurl)
            print "detailurl {}".format(detailurl)
            yield scrapy.Request(detailurl, callback=self.parse)

        if response.url.find("news.asp") != -1:
            for detailurl in response.xpath("//div[@class='right_news']/ul/li/a/@href").extract():
                detailurl = urlparse.urljoin(self.news_base_url, detailurl)
                print "news.asp detailurl {}".format(detailurl)
                yield scrapy.Request(detailurl, callback=self.parse_detail)

        if response.url.find("pro.asp") != -1:
            for detailurl in response.xpath("//div[@class='cp']/div[@class='cp_title']/a/@href").extract():
                detailurl = urlparse.urljoin(self.pro_base_url, detailurl)
                print "pro.asp detailurl {}".format(detailurl)
                yield scrapy.Request(detailurl, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = Dh31Item()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''

        details = response.xpath("//div[@class='right_xx']")
        a_title = details.xpath("div[@class='wzbt']/text()").extract()
        if len(a_title) > 0:
            bitem['art_title'] = a_title[0]
        
        infos = details.xpath("div[@class='laiy']/text()").extract()
        if len(infos) > 0:
            # 发布时间：01.12  浏览：560 次
            s = infos[0]
            index_1 = s.find(":")
            index_2 = s.find("浏览")
            index_3 = s.rfind(":")
            index_4 = s.find("次")
            if index_2 > index_1:
                bitem['art_pub_time'] = s[index_1 + 1:index_2].strip()
            if index_4 > index_3:
                bitem['art_read'] = s[index_3 + 1:index_4].strip()

        for ite in details.xpath("div[@class='nei-xx']/p/span/text()").extract():
            bitem['art_content'] += ite

        if not bitem['art_content']:
            for ite in details.xpath("div[@class='nei-xx']/div/p/text()").extract():
                bitem['art_content'] += ite

        if not bitem['art_content']:
            for ite in details.xpath("div[@class='nei-xx']/p/text()").extract():
                bitem['art_content'] += ite
        
        if not bitem['art_content']:
            for ite in details.xpath("div[@class='nei-xx']/span/p/span/text()").extract():
                bitem['art_content'] += ite

        if not bitem['art_content']:
            print "content null {}".format(response.url)

        yield bitem


