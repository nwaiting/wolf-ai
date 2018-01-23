# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import CaasItem

class CaasSpider(scrapy.Spider):
    name = "caas"
    allowed_domains = ["icgr.caas.net.cn"]
    base_url = "http://icgr.caas.net.cn/"

    kp_base_url = "http://icgr.caas.net.cn/kp/"
    disease_base_url = "http://icgr.caas.net.cn/disease/"

    start_urls = ( 
        'http://icgr.caas.net.cn/kp/kpa.html',
        'http://icgr.caas.net.cn/disease/default.html',
        'http://icgr.caas.net.cn/cgris%E8%AE%BA%E6%96%87.html'
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        if response.url.startswith('http://icgr.caas.net.cn/kp'):
            for new_url in response.xpath("//tr/td/p/a/@href").extract():
                new_url = urlparse.urljoin(self.kp_base_url, new_url)
                # print "kp new_url {}".format(new_url)
                yield scrapy.Request(new_url, callback=self.parse)

            for detailurl in response.xpath("//tr/td/a/@href").extract():
                detailurl = urlparse.urljoin(self.kp_base_url, detailurl)
                # print "kp detailurl {}".format(detailurl)
                yield scrapy.Request(detailurl, callback=self.parse_detail)

        if response.url.startswith('http://icgr.caas.net.cn/disease'):
            for new_url in response.xpath("//tr/td/p/font/b/a/@href").extract():
                new_url = urlparse.urljoin(self.disease_base_url, new_url)
                # print "disease new_url {}".format(new_url)
                yield scrapy.Request(new_url, callback=self.parse)

            for detailurl in response.xpath("//tr/td/a/@href").extract():
                detailurl = urlparse.urljoin(self.disease_base_url, detailurl)
                # print "disease detailurl {}".format(detailurl)
                yield scrapy.Request(detailurl, callback=self.parse_detail)                       

        if response.url.startswith('http://icgr.caas.net.cn/cgris'):
            for detailurl in response.xpath("//tr/td/a/@href").extract():
                detailurl = urlparse.urljoin(self.base_url, detailurl)
                # print "cgris {}".format(detailurl)
                yield scrapy.Request(detailurl, callback=self.parse_detail) 


    def parse_detail(self, response):
        bitem = CaasItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''
        
        if response.url.startswith('http://icgr.caas.net.cn/kp'):
            for content in response.xpath("//tr/td/font/p/text()").extract():
                bitem['art_content'] += content.strip()

            for content in response.xpath("//tr/td/p/font/text()").extract():
                bitem['art_content'] += content.strip()

            if not bitem['art_content']:
                for content in response.xpath("//font/p/text()").extract():
                    bitem['art_content'] += content.strip() 

            if not bitem['art_content']:
                for content in response.xpath("//tr/td/p/text()").extract():
                    bitem['art_content'] += content.strip()

            if not bitem['art_content']:
                for content in response.xpath("//tr/td/font/text()").extract():
                    bitem['art_content'] += content.strip()

            if not bitem['art_content']:
                for content in response.xpath("//p/font/text()").extract():
                    bitem['art_content'] += content.strip()

            a_title = response.xpath("//tr/td/font/p[1]/text()").extract()
            if len(a_title) > 0:
                bitem['art_title'] = a_title[0]

            if not bitem['art_title']:
                a_title = response.xpath("//p/font/text()").extract()
                if len(a_title) > 0:
                    bitem['art_title'] = a_title[0]

        if response.url.startswith('http://icgr.caas.net.cn/disease'):
            a_title = response.xpath("//tr/td/p/b/font/text()").extract()
            if len(a_title) > 0:
                bitem['art_title'] = a_title[0]

            for content in response.xpath("//tr/td/p/font/text()").extract():
                bitem['art_content'] += content.strip()

        if response.url.startswith('http://icgr.caas.net.cn/paper'):
            a_title = response.xpath("//p[@align='CENTER']/strong/font/text()").extract()
            if len(a_title) > 0:
                bitem['art_title'] = a_title[0]

            for content in response.xpath("//body/p/font/text()").extract():
                bitem['art_content'] += content.strip()

            if not bitem['art_content']:
                for content in response.xpath("//p/font/text()").extract():
                    bitem['art_content'] += content.strip()
 
                for content in response.xpath("//font/p/text()").extract():
                    bitem['art_content'] += content.strip()           

        if not bitem['art_content']:
            print "content null {}".format(response.url)
        
        if not bitem['art_title']:
            print "title null {}".format(response.url)

        yield bitem


