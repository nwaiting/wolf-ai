# -*- coding: utf-8 -*-
import scrapy
from webspider.items import WebspiderPipelineTieBaFilm
import re

class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['baidu.com']
    start_urls = ['http://tieba.baidu.com/f?kw=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1&ie=utf-8&pn=0']

    def parse(self, response):
        print response
        contents = response.body

        #self.parse_detail(response=contents)

        p_nextpage = r'(?<=href=\").*?(?=\" class=\"next pagination-item)'
        patten_nextpage = re.compile(p_nextpage)
        next_pages = patten_nextpage.findall(contents)
        print next_pages
        if next_pages:
            yield scrapy.Request(url='http:' + next_pages[0], callback=self.parse)

    def parse_detail(self, response):
        for item in response.xpath('//div[@class="t_con cleafix"]'):
            tieba = WebspiderPipelineTieBaFilm()
            tieba['responsenum'] = item.xpath('./div[@class="col2_left j_threadlist_li_left"]/span/text()').extract_first()
            tieba['title'] = item.xpath('.//div[@class="threadlist_lz clearfix"]/div/a/text()').extract_first()
            tieba['author'] = item.xpath('//span[@class="frs-author-name-wrap"]/a/text()').extract_first()
            tieba['authorlevel'] = item.xpath('.//div[@class="threadlist_lz clearfix"]//a[@class="j_icon_slot"]/@title').extract_first()
            item_items = item.xpath('.//div[@class="threadlist_detail clearfix"]')
            if item_items:
                tieba['frescontent'] = item_items.xpath('./div/div/text()').extract_first()
                tieba['frestime'] = item_items.xpath('./div/span/text()').extract_first()
                tieba['fresuser'] = item_items.xpath('./div/span/a/text()').extract_first()
            yield tieba
