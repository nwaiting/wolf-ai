# -*- coding: utf-8 -*-
import scrapy
from webspider.items import WebspiderPPTVItem

class PptvSpider(scrapy.Spider):
    name = 'pptv'
    allowed_domains = ['pptv.com']
    next_page_template = 'http://list.pptv.com/channel_list.html?page={0}&type=1&sort=1'
    start_urls = ['http://list.pptv.com/?type=1&sort=1']

    def parse(self, response):
        print response
        for pitem in response.xpath('//ul[@class="cf"]/li'):
            pptvitem = WebspiderPPTVItem()
            item = pitem.xpath('./a[@class="ui-list-ct"]')
            parseres = item.xpath('.//em[@class="cover ico_4 cf"]').extract()
            pptvitem['isvip'] = "0"
            if len(parseres) > 0:
                pptvitem['isvip'] = "1"
            pptvitem['fileurl'] = item.xpath('./@href').extract_first()
            pptvitem['name'] = item.xpath('./p[@class="ui-txt"]/span/text()').extract_first()
            pptvitem['score'] = item.xpath('./p[@class="ui-txt"]/em/text()').extract_first()

            detail = ''
            for itemchild in pitem.xpath('.//div[@class="v_info"]/p'):
                s = itemchild.xpath('./em/text()').extract_first()
                if s:
                    detail += s.strip()
                detail += '+'
                s = itemchild.xpath('./text()').extract_first()
                if s:
                    detail += s.strip()
            pptvitem['details'] = detail
            yield pptvitem
        for i in xrange(2, 151):
            yield scrapy.Request(url=self.next_page_template.format(i), callback=self.parse_addpage)

    def parse_addpage(self, response):
        print response
        for pitem in response.xpath('//li'):
            pptvitem = WebspiderPPTVItem()
            item = pitem.xpath('./a[@class="ui-list-ct"]')
            parseres = item.xpath('.//em[@class="cover ico_4 cf"]').extract()
            pptvitem['isvip'] = "0"
            if len(parseres) > 0:
                pptvitem['isvip'] = "1"
            pptvitem['fileurl'] = item.xpath('./@href').extract_first()
            pptvitem['name'] = item.xpath('./p[@class="ui-txt"]/span/text()').extract_first()
            pptvitem['score'] = item.xpath('./p[@class="ui-txt"]/em/text()').extract_first()

            detail = ''
            for itemchild in pitem.xpath('.//div[@class="v_info"]/p'):
                s = itemchild.xpath('./em/text()').extract_first()
                if s:
                    detail += s.strip()
                detail += '+'
                s = itemchild.xpath('./text()').extract_first()
                if s:
                    detail += s.strip()
            pptvitem['details'] = detail
            yield pptvitem
