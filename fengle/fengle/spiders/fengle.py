# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse
from scrapy.selector import Selector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import FengleItem

class DhseedSpider(scrapy.Spider):
    name = "fengle"
    allowed_domains = ["fengle.com.cn"]
    base_url = "http://www.fengle.com.cn"
    start_urls = ( 
        'http://www.fengle.com.cn/list/?116_1.html',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        sites = response.xpath("html/body/div[2]/div[2]/div/div[2]/div/div/a[1]/text()").extract()
        sites = Selector(response=response).xpath('html/body/div[2]/div[2]/div/div[2]/div/div/a[1]/text()').extract()
        print "sites {}".format(sites)
        return 
        for url in sites.xpath("@href").extract():
            next_curl = sites.xpath("/text()").extract()
            if next_curl[0] == "下一页":
                new_url = urlparse.urljoin(self.base_url, url)
                yield scrapy.Request(new_url, callback=self.parse)

        for detailinfo in response.xpath(".//*[@id='content']/div[2]/table/tbody/tr[2]/td/table/tbody"):
            detailurl = detailinfo.xpath("td[2]/a/@href").extract()
            detailurl = self.base_url + detailurl
            yield scrapy.Request(detailurl, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = FengleItem()
        bitem['art_title'] = response.xpath(".//*[@id='content']/div[1]/font/text()")
        #  2017-3-23 14:28:44 编辑：dhseed 来源：敦煌种业 浏览次数：
        detail_info = response.xpath(".//*[@id='content']/div[2]/text()")
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
        bitem['art_read'] = response.xpath(".//*[@id='hits']/text()")
        bitem['art_content'] = response.xpath(".//*[@id='content']/div[3]/p[1]/text()")
        yield bitem


