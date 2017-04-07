# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import scrapy
import urlparse
import re

from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO  import StringIO

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
            print "new_url {}".format(new_url)
            yield scrapy.Request(new_url, callback=self.middle_parse)

    def middle_parse(self, response):
        new_url = response.url
        if new_url.find("ista-strategy-_content") != -1:
            for detail_url in response.xpath("//tr/td[@class='norm editorcontent']/a/@href").extract():
                if not detail_url.startswith("http"):
                    detail_url = urlparse.urljoin(self.base_url, detail_url)
                print "strategy {}".format(detail_url)
                yield scrapy.Request(detail_url, callback=self.parse_detail)
        elif new_url.find("the-articles-of-ista") != -1:
            infos = response.xpath("//tr[@valign='top']/td[@class='norm']/a[@target='_blank']/@href").extract()
            if len(infos) > 0:
                detail_url = urlparse.urljoin(self.base_url, infos[0])
                print "articles {}".format(detail_url)
                yield scrapy.Request(detail_url, callback=self.parse_detail)
        elif new_url.find("ordinary-general-meeting-minutes") != -1:
            for url in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/strong/a/@href").extract():
                url = urlparse.urljoin(self.base_url, url)
                print "ordinary {}".format(url)
                yield scrapy.Request(url, callback=self.parse_detail)
        elif new_url.find("activity-reports") != -1:
            for url in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/strong/a/@href").extract():
                url = urlparse.urljoin(self.base_url, url)
                print "reports {}".format(url)
                yield scrapy.Request(url, callback=self.parse_detail)  
        elif new_url.find("position-papers") != -1:
            for url in response.xpath("//tr[@valign='top']/td[@class='norm editorcontent']/strong/a/@href").extract():
                url = urlparse.urljoin(self.base_url, url)
                print "papers {}".format(url)
                yield scrapy.Request(url, callback=self.parse_detail)
        elif new_url.find("press-releases") != -1:
            for url in response.xpath("//tr[@valign='top']/td[@class='norm']/a[@target='_blank']/@href").extract():
                url = urlparse.urljoin(self.base_url, url)
                print "releases {}".format(url)
                yield scrapy.Request(url, callback=self.parse_detail)
        else:
            print "other {}".format(new_url)
            yield scrapy.Request(new_url, callback=self.parse_detail)

    def parse_detail(self, response):
        if not response.body:
            print "body null {}".format(response.body)
            return
        bitem = SeedtestItem()
        bitem['art_title'] = ''
        bitem['art_content'] = ''
        bitem['art_from'] = ''
        bitem['art_author'] = ''
        bitem['art_read'] = ''
        bitem['art_pub_time'] = ''
        
        if response.url.find(".pdf") != -1:
            output = StringIO()
            input_io = StringIO(response.body)
            pagenos = set()
            codec = 'utf-8'
            laparams = LAParams()
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # 处理文档对象中每一页的内容
            for page in PDFPage.get_pages(input_io, pagenos, check_extractable=True):
                interpreter.process_page(page)
            
            output_str = output.getvalue()
            input_io.close()
            output.close()
            device.close()

            for line in output_str:
                if not len(line):
                    continue
                bitem['art_content'] += line.strip()
        else:
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

            if response.url.find("press-releases") != -1 or response.url.find("cms") != -1:
                try:
                    for istr in response.xpath(".//*[@class='textLayer']/xhtml:div/text()").extract():
                        bitem['art_content'] += istr.strip()
                except Exception as e:
                    print "exception {0} {1} ===== {2} {3}".format(response.status, response.url, len(response.body), e)

            if not bitem['art_content']:
                try:
                    for istr in response.xpath("//tr/td[@class='norm editorcontent']/text()").extract():
                        bitem['art_content'] += istr.strip()
                except Exception as e:
                    print "exception {0} {1} ===== {2} {3}".format(response.status, response.url, len(response.body), e)

        if not bitem['art_content']:
            print "content null {}".format(response.url)

        yield bitem


