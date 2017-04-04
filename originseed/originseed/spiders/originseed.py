# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import OriginseedItem

class OriginseedSpider(scrapy.Spider):
    name = "originseed"
    allowed_domains = ["originseed.com.cn"]
    base_url = "http://www.originseed.com.cn/news/"
    start_urls = ( 
        'http://www.originseed.com.cn/news/list.php?pid=15&id=8',
        'http://www.originseed.com.cn/news/list.php?pid=15&id=45',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        sites = response.xpath("//tr[@valign='bottom']/td/div/a[last()]")
        for url in sites.xpath("@href").extract():
            next_curl = sites.xpath("text()").extract()
            if next_curl[0] == "下一页":
                new_url = urlparse.urljoin(self.base_url, url)
                yield scrapy.Request(new_url, callback=self.parse)
        
        for detailurl in response.xpath("//tr/td/li/div[@align='left']/a/@href").extract():
            detailurl = self.base_url + detailurl
            yield scrapy.Request(detailurl, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = OriginseedItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''

        bitem['art_title'] = response.xpath("//td[@class='biaoti']/div/text()").extract()[0].strip()
        #  发布时间 [ 2015-04-28 ]
        date_str = response.xpath("//td[@class='date']/div/text()").extract()
        if len(date_str) > 0:
            index_b = date_str[0].find('[')
            index_end = date_str[0].find(']')
            if index_end > index_b:
                bitem['art_pub_time'] = date_str[0][index_b + 1:index_end].strip()
        result = (''.join(response.xpath("//div[@align='left']/p[@class='MsoNormal']/span/text()").extract())).strip()
        bitem['art_content'] = result

        re_comp = re.compile(r'(?<=\>)(.*?)(?=\<)', re.U | re.S)
        if not result:
            re_hm = str()
            for istr in response.xpath("//div[@align='left']/div/span/span").extract():
                re_hm += istr
            result = str()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            bitem['art_content'] = result

        if not result:
            for istr in response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']/p/span/text()").extract():
                result += istr.strip()
            bitem['art_content'] = result
        
        if not result:
            details = response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']")
            for ite in details.xpath("h2/font/span/text()").extract():
                result += ite.strip()
            for ite in details.xpath("address/font/font/span/text()").extract():
                result += ite.strip()
            for ite in details.xpath("p/font/font/span/span/text()").extract():
                result += ite.strip()
            bitem['art_content'] = result

        if not result:
            details = response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']/p/span")
            re_hm = str()
            for ite in details.xpath("font/span").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            for ite in details.xpath("span/font/text()").extract():
                result += ite.strip()
            bitem['art_content'] = result

        if not result:
            re_hm = str()
            for ite in response.xpath("//div[@style='text-align: justify;']/div/span/span/span").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            bitem['art_content'] = result
        
        if not result:
            re_hm = str()
            for ite in response.xpath("//div[@align='left']/p[@class='MsoNormal']/span/span").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            bitem['art_content'] = result
       
        if not result:
            re_hm = str()
            for ite in response.xpath("//td[@class='zhengwen-zhong']/div/p/font").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            bitem['art_content'] = result
        
        if not result:
            for ite in response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']/text()").extract():
                result += ite.strip()
            bitem['art_content'] = result
        
        if not result:
            re_hm = str()
            for ite in response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']/div/div/span/span").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            bitem['art_content'] = result

        if not result:
            details = response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']")
            re_hm = str()
            for ite in details.xpath("span/p/font/span").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
       
            re_hm = str()
            for ite in details.xpath("p").extract():
                re_hm += ite.strip()
            for ite in re_comp.findall(re_hm):
                result += ite.strip()
            bitem['art_content'] = result

        if not result:
            for ite in response.xpath("//td[@class='zhengwen-zhong']/div[@align='left']/p/text()").extract():
                result += ite.strip()
            bitem['art_content'] = result

        if not result:
            for ite in response.xpath("//p[@class='Section0']/text()").extract():
                result += ite.strip()
            bitem['art_content'] = result

        if not result: 
            print "result null {}".format(response.url)

        yield bitem



