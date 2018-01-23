# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import DhseedItem

class DhseedSpider(scrapy.Spider):
    name = "kiplinger"
    allowed_domains = ["kiplinger.com"]
    base_url = "http://www.kiplinger.com"
    start_urls = ( 
        'http://www.kiplinger.com/fronts/channels/investing/index.html',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        self.parse_detail(response)
        self.middle_parse(response)

    def middle_parse(self, response):
        time_stamp = int(time.time() * 1000) - 3 * 60
        box_id = 4
        # url = 'http://www.kiplinger.com/requires/nextrecent.php?boxId={0}&frontId=7&frontType=channels&globalAgg=0&catFilter=0&_={1}'.format(box_id, time_stamp)
        for i in xrange(1, 30):
            url = 'http://www.kiplinger.com/requires/nextrecent.php?boxId={0}&frontId=7&frontType=channels&globalAgg=0&catFilter=0&_={1}'.format(box_id, time_stamp)
            box_id += 1
            time_stamp += 1
            yield scrapy.Request(url, callback=self.parse_detail_list)
            
    def parse_detail_list(self, response):
        for url in response.xpath("//div[@class='kip-thumb pull-left']/a/@href").extract():
            url = urlparse.urljoin(self.base_url, url)
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        if response.status != 200:
            print "{0} {1}".format(response.status, response.url)
            return

        bitem = DhseedItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''
        
        details = response.xpath("//p[@class='kip-byline clearfix']")
        infos = details.xpath("text()").extract()
        if len(infos) > 0:
            bitem['art_pub_time'] = infos[-1].strip()

        infos = details.xpath("i/text()").extract()
        if len(infos) > 0:
            bitem['art_from'] = infos[0].strip()

        names = details.xpath("a/text()").extract()
        if len(names) > 0:
            bitem['art_author'] = names[0].strip()

        infos = response.xpath("//div[@class='kip-head row']/div/h1/text()").extract()
        if len(infos) > 0:
            bitem['art_title'] = infos[0].strip()

        for info in response.xpath("//div[@class='kip-content']/p/text()").extract()
            bitem['art_content'] += info.strip()
            
        yield bitem


