# -*- coding: utf-8 -*-
import scrapy
import urlparse

class BaidusearchSpider(scrapy.Spider):
    name = 'baidusearch'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/s?wd=%E5%BC%A0%E8%BF%91%E4%B8%9C&rsv_spt=1&rsv_iqid=0xe00d664300003df4&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&oq=%25E5%25BC%25A0%25E9%259D%2599%25E5%2588%259D&inputT=375&rsv_t=9edcC3n24M79hgQF4h02nvuPWbD4xPSc%2Ffdf1zMI8%2BdabsaiMUcQlO%2FrcRtmwD2SCa%2FZ&rsv_pq=deb028c600005ea8&rsv_sug3=25&rsv_sug1=19&rsv_sug7=100&bs=%E5%BC%A0%E9%9D%99%E5%88%9D']
    next_pre = 'https://www.baidu.com'

    def parse(self, response):
        for item in response.xpath('//div[starts-with(@class,"result-op c-container") or starts-with(@class,"result c-container")]'):
            print '============ {0} {1}'.format(item.xpath('./h3/a/text()').extract_first(), item.xpath('//div[@class="c-abstract"]/text()').extract_first())

        next_page = response.xpath('//a[starts-with(@class,"n")]/@href').extract_first()
        print "next_page"
        if next_page:
            new_page = urlparse.urljoin(next_pre, next_page)
            print "new_page ", new_page
            yield scrapy.Request(url=new_page, callback=self.parse)
