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
        
        details = response.xpath("//div[@id='content']/div")
        titles = details.xpath("font/text()").extract()
        if len(titles) > 0:
            bitem['art_title'] = titles[0]

        infos = details.xpath("span/text()").extract()
        if len(infos) > 0:
            bitem['art_read'] = infos[0]

        #  2017-3-23 14:28:44 编辑：dhseed 来源：敦煌种业 浏览次数：
        detail_info = details.xpath("text()").extract()[0]
        t_index = detail_info.find("编辑：")
        if t_index:
            bitem['art_pub_time'] = detail_info[:detail_info.find("编辑：")].strip()
        t_index = detail_info.find("编辑：") + len("编辑：")
        t_index_2 = detail_info.find("来源：")
        if t_index_2 > t_index:
            bitem['art_author'] = detail_info[t_index:t_index_2].strip()
        t_index = detail_info.find("来源：") + len("来源：")
        t_index_2 = detail_info.find("浏览次数：")
        if t_index_2 > t_index:
            bitem['art_from'] = detail_info[t_index:t_index_2].strip()

        for info in details.xpath("p/text()").extract():
            bitem['art_content'] += info.strip()
        yield bitem


