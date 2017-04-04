# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import SeedtestItem

class SeedtestSpider(scrapy.Spider):
    name = "seedtest"
    allowed_domains = ["seedtest.org"]
    base_url = "http://www.seedtest.org"
    start_urls = ( 
        'https://www.seedtest.org/en/about-ista-_content---1--1011.html',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        for new_url in response.xpath("//tr/td[@class='norm']/span/a/@href").extract():
            if not new_url.startswith("http"):
                new_url = urlparse.urljoin(self.base_url, new_url)
            if new_url.find("ista-strategy-_content") != -1:
                for detail_url in response.xpath("//tr/td[@class='norm editorcontent']/a/@href").extract():
                    if not detail_url.startswith("http"):
                        detail_url = urlparse.urljoin(self.base_url, detail_url)
                    yield scrapy.Request(detail_url, callback=self.parse_detail)
            elif new_url.find("the-articles-of-ista") != -1:
                infos = response.xpath("//tr[@valign='top']/td[@class='norm']/a[@target='_blank']/@href").extract()
                if len(infos) > 0:
                    detail_url = urlparse.urljoin(self.base_url, infos[0])
                    yield scrapy.Request(detail_url, callback=self.parse_detail)
            elif new_url.find("ordinary-general-meeting-minutes") != -1:
                for url in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/strong/a/@href").extract():
                    url = urlparse.urljoin(self.base_url, url)
                    yield scrapy.Request(url, callback=self.parse_detail)
            elif new_url.find("activity-reports") != -1:
                for url in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/strong/a/@href").extract():
                    url = urlparse.urljoin(self.base_url, url)
                    yield scrapy.Request(url, callback=self.parse_detail)  
            elif new_url.find("position-papers") != -1:
                for url in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/strong/a/@href").extract():
                    url = urlparse.urljoin(self.base_url, url)
                    yield scrapy.Request(url, callback=self.parse_detail)
            elif new_url.find("press-releases") != -1:
                for url in response.xpath("//tr[@valign='top']/td[@class='norm']/a[@target='_blank']/@href").extract():
                    url = urlparse.urljoin(self.base_url, url)
                    yield scrapy.Request(url, callback=self.parse_detail)
            else:
                yield scrapy.Request(new_url, callback=self.parse_detail)



    def parse_detail(self, response):
        bitem = SeedtestItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''
        
        if response.url.find("about-ista") != -1:
            titles = response.xpath("//td[@class='title']/span[@class='title']/text()").extract()
            if len(titles) > 0:
                bitem['art_title'] = titles[0]

            re_comp = re.compile(r'(?<=\>)(.*?)(?=\<)', re.U | re.S)
            re_hm = str()
            for istr in response.xpath("//tr/td[@class='norm editorcontent']").extract():
                re_hm += istr

            for ite in re_comp.findall(re_hm):
                bitem['art_content'] += ite.strip()

        if response.url.find("ista-strategy") != -1:
            for istr in response.xpath("//xhtml:div[@class='textLayer']/xhtml:div/text()").extract():
                bitem['art_content'] += istr.strip()

        if response.url.find("secretariat") != -1:
            for istr in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/text()").extract():
                bitem['art_content'] += istr.strip()

            titles = response.xpath("//td[@class='title']/span[@class='title']/text()").extract()
            if len(titles) > 0:
                bitem['art_title'] = titles[0]

        if response.url.find("executive-committee") != -1:
            titles = response.xpath("//td[@class='title']/span[@class='title']/text()").extract()
            if len(titles) > 0:
                bitem['art_title'] = titles[0]

            for istr in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/text()").extract():
                bitem['art_content'] += istr.strip()

        if response.url.find("the-articles-of-ista") != -1:
            for istr in response.xpath("//xhtml:div[@class='textLayer']/xhtml:div/text()").extract():
                bitem['art_content'] += istr.strip()

            num_list = [19, 20, 21, 22, 13]
            for i in num_list:
                re_str = ".//*[@id='pageContainer1']/xhtml:div[2]/xhtml:div[{0}]/text()".format(i)
                titles = response.xpath(re_str).extract()
                if len(titles) > 0:
                    bitem['art_title'] = titles[0]

        if response.url.find("ordinary-general-meeting-minutes") != -1:
            for istr in response.xpath("//xhtml:div[@class='textLayer']/xhtml:div/text()").extract():
                bitem['art_content'] += istr.strip()

        if response.url.find("activity-reports") != -1:
            for istr in response.xpath("//xhtml:div[@class='textLayer']/xhtml:div/text()").extract():
                bitem['art_content'] += istr.strip()

        if response.url.find("position-papers") != -1:
            for istr in response.xpath("//xhtml:div[@class='textLayer']/xhtml:div/text()").extract():
                bitem['art_content'] += istr.strip() 

        if response.url.find("press-releases") != -1:
            for istr in response.xpath("//xhtml:div[@class='textLayer']/xhtml:div/text()").extract():
                bitem['art_content'] += istr.strip() 

        yield bitem


