# -*- coding: utf-8 -*-
import sys
import os
import scrapy
import urlparse
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import Bbsc114Item

reload(sys)
sys.setdefaultencoding('utf-8')

class Bbsc114Spider(scrapy.Spider):
    name = "bbsc114"
    allowed_domains = ["www.originseed.com"]
    base_url = "http://www.originseed.com.cn/news/"
    start_urls = (
        'http://www.originseed.com.cn/news/view.php?pid=15&id=892',
    )
    
    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        details = response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']/p/span")
        re_hm = str()
        result = str()
        re_comp = re.compile(r'(?<=\>)(.*?)(?=\<)', re.U | re.S)
        for ite in details.xpath("font/span").extract():
            re_hm += ite.strip()
        for ite in re_comp.findall(re_hm):
            result += ite.strip()
        for ite in details.xpath("span/font/text()").extract():
            result += ite.strip()
        print result
        return
    
        # sites = response.xpath(".//div[@id='main']/div[@id='middle']/div[@id='left2']/div[@class='w100']/div[@id='pg']/a[last()-1]@href").extract()
	sites = response.xpath(".//*[@id='pg']/a[10]/text()").extract()
        print "sites {}".format(sites)
	return
        for url in sites.xpath("@href").extract():
        #for url in response.xpath(".//div[@id='main']/div[@id='middle']/div[@id='left2']/div[@class='w100']/div[@id='pg']/a[last()-1]/@href").extract():
            next_curl = sites.xpath("text()").extract()
            if next_curl[0] == "下一页":
                new_url = urlparse.urljoin(self.base_url, url)
                #print "enter next page {0} {1}\n".format(next_curl[0], new_url)
                yield scrapy.Request(new_url, callback=self.parse)
        
        for detailinfo in response.xpath("//tr"):
            title = detailinfo.xpath("td/span/a/text()").extract()
            if title:
                bitem = Bbsc114Item()
                bitem['title_name'] = title[0]
                bitem['title_type'] = detailinfo.xpath("td/span/span/a/text()").extract()[0]
                two_items = detailinfo.xpath("td[@align='center']/text()").extract()
                #print "len(two_items) {0}".format(len(two_items))
                if len(two_items) == 2:
                    bitem['answers'] = two_items[0]
                    bitem['handle_time'] = two_items[1]
                url = detailinfo.xpath("td/span/a/@href").extract()
                detailurl = urlparse.urljoin(self.base_url, url[0])
                self.all_contents = ""
                yield scrapy.Request(detailurl, callback=self.parse_detail)
                bitem['title_content'] = self.all_contents
                yield bitem
                
    def parse_detail(self, response):
        #content_sites = response.xpath(".//div/div[@id='middle']/div[@id='left2']/div[@class='b3 bcg mb12']/div[@class='w100']/div[@class='w100_3']")
        self.all_contents += response.xpath(".//*[@id='left2']/div[2]/div/div/div[3]/text()").extract()[0]
        for c in response.xpath(".//*[@class='f14']/text()").extract():
            self.all_contents += c
        for contents in response.xpath(".//*[starts-with(@class, 'f14 ')]/text()").extract():
            self.all_contents += contents
        print "self.all_contents {0}".format(self.all_contents)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
