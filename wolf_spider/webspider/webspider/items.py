# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WebspiderIqiyiItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    totalsee = scrapy.Field()
    totalcomments = scrapy.Field()
    playcounts = scrapy.Field()
    upcounts = scrapy.Field()
    downcounts = scrapy.Field()
    isvip = scrapy.Field()
    actors = scrapy.Field()

class WebspiderPPTVItem(scrapy.Item):
    name = scrapy.Field()
    fileurl = scrapy.Field()
    score = scrapy.Field()
    isvip = scrapy.Field()
    details = scrapy.Field()
class WebspiderTieBaFilm(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    authorlevel = scrapy.Field()
    responsenum = scrapy.Field()
    frescontent = scrapy.Field()
    fresuser = scrapy.Field()
    frestime = scrapy.Field()

class Webspider36krItem(scrapy.Item):
    name = scrapy.Field()
    brief = scrapy.Field()
    #行业
    industry = scrapy.Field()
    # 第几轮
    phase = scrapy.Field()
    #所在地
    city = scrapy.Field()
    #成立时间
    time = scrapy.Field()

class WebspiderAizhanItem(scrapy.Item):
    word = scrapy.Field()

class WebspiderJDItem(scrapy.Item):
    comments = scrapy.Field()
