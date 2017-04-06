# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import AntionlineItem

class AntionlineSpider(scrapy.Spider):
    name = "antionline"
    allowed_domains = ["antionline.com"]
    base_url = "http://www.antionline.com/"
    start_urls = ( 
        'http://www.antionline.com/',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        # total 0405
        for site in response.xpath("//h2[@class='forumtitle']/a/@href").extract():
            new_url = urlparse.urljoin(self.base_url, site)
            yield scrapy.Request(new_url, callback=self.middle_parse)

    def middle_parse(self, response):
        # next page 0405
        for detailurl in response.xpath("//span[@class='prev_next']/a/@href").extract():
            detailurl = urlparse.urljoin(self.base_url, detailurl)
            yield scrapy.Request(detailurl, callback=self.middle_parse)

        # on one page 0405
        for detail in response.xpath("//h3[@class='threadtitle']/a/@href").extract():
            detail_url = urlparse.urljoin(self.base_url, detail)
            yield scrapy.Request(detail_url, callback=self.parse_detail)

        for detail in response.xpath("//span[@class='prev_next']/a/@href").extract():
            detail_url = urlparse.urljoin(self.base_url, detail)
            scrapy.Request(detail_url, callback=self.middle_parse_page)
            break

    def middle_parse_page(self, response):
        for detail in response.xpath("//span[@class='prev_next']/a/@href").extract():
            detail_url = urlparse.urljoin(self.base_url, detail)
            yield scrapy.Request(detail_url, callback=self.middle_parse_page)

        for detail in response.xpath("//h3[@class='threadtitle']/a/@href").extract():
            detail_url = urlparse.urljoin(self.base_url, detail)
            yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = AntionlineItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''
        
        # content 0405
        for info in response.xpath("//div[@class='quote_container']/text()").extract():
            bitem['art_content'] += info.strip()
            
        titles = response.xpath("//span[@class='threadtitle']/a/text()").extract()
        if len(titles) > 0:
            bitem['art_title'] = titles[0].strip()

        infos = response.xpath("//span[@class='postdate old']/span[@class='date']/text()").extract()
        if len(infos):
            bitem['art_pub_time'] = infos[0].strip()

        yield bitem


