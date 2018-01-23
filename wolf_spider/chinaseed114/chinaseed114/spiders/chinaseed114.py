# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import Chinaseed114Item

class DhseedSpider(scrapy.Spider):
    name = "chinaseed114"
    allowed_domains = ["www.chinaseed114.com"]
    base_url = "http://www.chinaseed114.com/"
    start_urls = ( 
        'http://www.chinaseed114.com/news/yaowen/',
        'http://www.chinaseed114.com/market/yingxiao/',
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        for new_url in response.xpath("//tr/td/a/@href").extract():
            if new_url:
                print "new_url {}".format(new_url)
                yield scrapy.Request(new_url, callback=self.parse_middle)

    def parse_middle(self, response):
        url = response.xpath("//div[@class='pages']/a[last()]/@href").extract()
        if len(url) > 0 and url[0]:
            print "url[0] {}".format(url[0])
            yield scrapy.Request(url[0], callback=self.parse_middle)

        for url in response.xpath("//div[@class='catlist']/ul/li/a/@href").extract():
            if url:
                print "url {}".format(url)
                yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        bitem = Chinaseed114Item()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''
        
        details = response.xpath("//div[@class='left_box']")
        titles = details.xpath("h1/text()").extract()
        if len(titles) > 0:
            bitem['art_title'] = titles[0]

        infos = details.xpath("div[@class='info']/span/text()").extract()
        if len(infos) > 0:
            if len(infos) == 2:
                bitem['art_read'] = infos[1]
            else:
                bitem['art_read'] = infos[0]

        for infos in details.xpath("div[@class='info']/text()").extract():
            # print "infos {0} == {1}".format(infos, len(infos))
            # 发布日期：2015-03-17   来源：中国兴农网   浏览次数：
            # 发布日期：2017-03-29  作者：焦长轶   浏览次数：
            # 布日期：2017-02-24  来源：农财宝典   作者：上兵  浏览次数：
            infos = infos.strip()
            if infos:
                s = infos
                index_1 = s.find(u"20")
                index_2 = s.find(u"来源")
                index_3 = s.find(u"作者")
                index_4 = s.find(u"浏览")
                
                if index_2 > 0 and index_2 > index_1:
                    bitem['art_pub_time'] = s[index_1:index_2].strip()
                if not bitem['art_pub_time'] and index_3 > 0 and index_3 > index_1:
                    bitem['art_pub_time'] = s[index_1:index_3].strip()

                if index_2 > 0 and index_4 > index_2:
                    if index_3 != -1:
                        bitem['art_from'] = s[index_2 + len(u"来源") + 1:index_3]
                    else:
                        bitem['art_from'] = s[index_2 + len(u"来源") + 1:index_4]
                if index_3 > 0 and index_4 > index_3:
                    bitem["art_author"] = s[index_3 + len(u"作者") + 1:index_4]
                # print "time {0} from {1} author {2}".format(bitem['art_pub_time'], bitem['art_from'], bitem["art_author"])

        if not bitem['art_from']:
            infos = details.xpath("div[@class='info']/a/text()").extract()
            if len(infos) > 0:
                bitem['art_from'] = infos[0]

        details = response.xpath(".//*[@id='article']")
        for infos in details.xpath("div/text()").extract():
            bitem['art_content'] += infos.strip()
           
        if not bitem['art_content']:
            for infos in details.xpath("p/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("p/font/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("font/p/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("p/span/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("div/p/text()").extract():
                bitem['art_content'] += infos.strip()        

        if not bitem['art_content']:
            for infos in details.xpath("p/b/text()").extract():
                bitem['art_content'] += infos.strip()    

        if not bitem['art_content']:
            for infos in details.xpath("span/p/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("div/font/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("dl/dd/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content'] and response.url.find("exhibit") != -1:
            for infos in details.xpath("div/div/div/span/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in details.xpath("div/p/font/text()").extract():
                bitem['art_content'] += infos.strip()        

        if not bitem['art_content']:
            for infos in response.xpath(".//*[@id='article']/p/span/span/span/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in response.xpath(".//*[@id='alarmcontent']/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            for infos in response.xpath("//tr/td/p/font/text()").extract():
                bitem['art_content'] += infos.strip() 

        if not bitem['art_content'] and response.url.find("job") != -1:
            for infos in response.xpath("//tr/td/div/text()").extract():
                bitem['art_content'] += infos.strip()

        if not bitem['art_content']:
            print "content null {}".format(response.url)
            
        yield bitem


