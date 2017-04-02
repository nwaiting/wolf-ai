# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import OriginseedItem

class OriginseedSpider(scrapy.Spider):
    name = "originseed"
    allowed_domains = ["originseed.com.cn"]
    base_url = "http://www.originseed.com.cn/news/"
    start_urls = ( 
        'http://www.originseed.com.cn/news/list.php?pid=15&id=8',
        #'http://www.originseed.com.cn/news/list.php?pid=15&id=45',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        #with open('a.log', 'w') as f:
        #    f.write(''.join(response.body))
        #return
        sites = response.xpath("html")
        print "sites {}".format(sites)
        return 
        for url in sites.xpath("/@href").extract():
            next_curl = sites.xpath("/text()").extract()
            if next_curl[0] == "下一页":
                new_url = urlparse.urljoin(self.base_url, url)
                yield scrapy.Request(new_url, callback=self.parse)

        for detailinfo in response.xpath(".//*[@id='content']/div[2]/table/tbody/tr[2]/td/table/tbody"):
            detailurl = detailinfo.xpath("td[2]/a/@href").extract()
            detailurl = self.base_url + detailurl
            yield scrapy.Request(detailurl, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = DhseedItem()
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


