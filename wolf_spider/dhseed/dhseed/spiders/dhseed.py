# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import DhseedItem

class DhseedSpider(scrapy.Spider):
    name = "dhseed"
    allowed_domains = ["dhseed.com"]
    base_url = "http://www.dhseed.com"
    start_urls = ( 
        'http://www.dhseed.com/news_more.asp?lm2=169',
        'http://www.dhseed.com/news_more.asp?lm2=170',
        'http://www.dhseed.com/news_more.asp?lm2=191'
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        sites = response.xpath("//td[@valign='top']/center/a[last()-1]")
        if sites.xpath("text()").extract()[0] == "下一页":
            new_url = urlparse.urljoin(self.base_url, sites.xpath("@href").extract()[0].strip())
            yield scrapy.Request(new_url, callback=self.parse)

        for detailurl in response.xpath("//td/a[@target='_top']/@href").extract():
            detailurl = urlparse.urljoin(self.base_url, detailurl)
            yield scrapy.Request(detailurl, callback=self.parse_detail)

    def parse_detail(self, response):
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
        detail_infos = details.xpath("text()").extract()
        if len(detail_infos) > 0:
            detail_info = detail_infos[0]
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

        if not bitem['art_content'] and response.url.find("news_view.asp") != -1:
            for info in response.xpath(".//*[@id='content']/div[3]/text()").extract():
                bitem['art_content'] += info.strip()

            if not bitem['art_content']:
                for info in response.xpath(".//*[@id='content']/div[3]/p/font/text()").extract():
                    bitem['art_content'] += info.strip()

        if not bitem['art_content']:
            print "{}".format(response.url)
        yield bitem


