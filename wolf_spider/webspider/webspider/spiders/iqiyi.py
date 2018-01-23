# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from urlparse import urljoin
from webspider.items import WebspiderIqiyiItem
import requests
import re

class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    allowed_domains = ['iqiyi.com']
    page_pre = 'http://list.iqiyi.com'
    start_urls = ['http://list.iqiyi.com/']

    totalsee_detail_url_template = 'http://mixer.video.iqiyi.com/jp/mixin/videos/{0}?select=user,credit,focus,star,cast&status=1&callback=playInfo96'

    def parse(self, response):
        print response
        res = response.xpath('//a[starts-with(@class,"a1") and @data-key="down"]/@href').extract()
        if len(res) > 0:
            #print urljoin(self.page_pre, res[0])
            yield Request(url=urljoin(self.page_pre, res[0]), callback=self.parse)

        webiqiyi = WebspiderIqiyiItem()
        try:
            for item in response.xpath('//div[@class="wrapper-piclist"]//li'):
                #print item.xpath('.//a[@class="site-piclist_pic_link"]/@href').extract_first()
                webiqiyi['name'] = None
                name = item.xpath('.//div[@class="mod-listTitle_left"]/p/a/text()').extract_first()
                if name:
                    webiqiyi['name'] = name.strip()

                detail_id = item.xpath('.//div[@class="site-piclist_pic"]/a/@data-qidanadd-tvid').extract_first()

                webiqiyi['score'] = None
                score = item.xpath('.//span[@class="score"]/strong/text()').extract_first()
                if score:
                    webiqiyi['score'] = score.strip()
                score = item.xpath('.//span[@class="score"]/text()').extract_first()
                if score:
                    webiqiyi['score'] += score.strip()

                vipinfo = item.xpath('*//span[@class="icon-vip-zx"]').extract()
                if len(vipinfo) > 0:
                    webiqiyi['isvip'] = "1"
                else:
                    webiqiyi['isvip'] = "0"

                actors = u'主演:'
                for actor in item.xpath('*//div[@class="role_info"]/em/a/text()').extract():
                    actors += actor.strip() + "+"
                webiqiyi['actors'] = actors

                if detail_id:
                    detail_url = self.totalsee_detail_url_template.format(detail_id)
                    detail_res = requests.get(url=detail_url)
                    reres = re.search(r'(?=\"upCount)(.*?)(?=,)', detail_res.text)
                    webiqiyi['upcounts'] = None
                    if reres:
                        webiqiyi['upcounts'] = reres.group()

                    reres = re.search(r'(?=\"downCount)(.*?)(?=,)', detail_res.text)
                    webiqiyi['downcounts'] = None
                    if reres:
                        webiqiyi['downcounts'] = reres.group()

                    reres = re.search(r'(?=\"playCount)(.*?)(?=,)', detail_res.text)
                    webiqiyi['playcounts'] = None
                    if reres:
                        webiqiyi['playcounts'] = reres.group()

                    reres = re.search(r"(?=\"starTotal)(.*?)(?=,)", detail_res.text)
                    webiqiyi['totalcomments'] = None
                    if reres:
                        webiqiyi['totalcomments'] = reres.group()

                yield webiqiyi
                #print u"=================== {0} {1} {2}".format(webiqiyi['name'], webiqiyi['score'], webiqiyi['actors'])

                """
                子页面分数：
                http://score-video.iqiyi.com/beaver-api/get_sns_score?qipu_ids=820545900&appid=21&tvid=820545900&pageNo=1&callback=window.Q.__callbacks__.cb6c2i3y

                子页面评论等：
                http://mixer.video.iqiyi.com/jp/mixin/videos/820545900?select=user,credit,focus,star,cast&status=1&callback=playInfo96
                """

        except Exception as e:
            print "error {0}".format(e)
