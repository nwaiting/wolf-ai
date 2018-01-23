# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from webspider.items import WebspiderTieBaFilm
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['baidu.com']
    start_urls = ['http://tieba.baidu.com/f?kw=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1&ie=utf-8&pn=0']

    def parse(self, response):
        print response
        contents = response.body

        first = contents.find('<ul id="thread_list" class="threadlist_bright j_threadlist_bright">')
        second = contents.find('<div class="thread_list_bottom clearfix">')
        if first and second:
            hse = Selector(text=contents[first:second])
            for item in hse.xpath('//div[@class="t_con cleafix"]'):
                tieba = WebspiderTieBaFilm()
                tieba['responsenum'] = None
                responsenum = item.xpath('./div[@class="col2_left j_threadlist_li_left"]/span/text()').extract_first()
                if responsenum:
                    tieba['responsenum'] = responsenum.strip()

                tieba['title'] = None
                title = item.xpath('.//div[@class="threadlist_lz clearfix"]/div/a/text()').extract_first()
                if title:
                    tieba['title'] = title.strip()

                tieba['author'] = None
                author = item.xpath('//span[@class="frs-author-name-wrap"]/a/text()').extract_first()
                if author:
                    tieba['author'] = author.strip()

                tieba['authorlevel'] = None
                authorlevel = item.xpath('.//div[@class="threadlist_lz clearfix"]//a[@class="j_icon_slot"]/@title').extract_first()
                if authorlevel:
                    tieba['authorlevel'] = authorlevel.strip()

                item_items = item.xpath('.//div[@class="threadlist_detail clearfix"]')
                if item_items:
                    tieba['frescontent'] = None
                    frescontent = item_items.xpath('./div/div/text()').extract_first()
                    if frescontent:
                        tieba['frescontent'] = frescontent.strip()

                    tieba['frestime'] = None
                    frestime = item_items.xpath('./div/span/text()').extract_first()
                    if frestime:
                        tieba['frestime'] = frestime.strip()

                    tieba['fresuser'] = None
                    fresuser = item_items.xpath('./div/span/a/text()').extract_first()
                    if fresuser:
                        tieba['fresuser'] = fresuser.strip()
                yield tieba

        p_nextpage = r'(?<=href=\").*?(?=\" class=\"next pagination-item)'
        patten_nextpage = re.compile(p_nextpage)
        next_pages = patten_nextpage.findall(contents)
        print "next ", next_pages
        if next_pages:
            yield scrapy.Request(url='http:' + next_pages[0], callback=self.parse)
