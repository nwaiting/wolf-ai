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

class WebspiderPipelineIqiyiItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    totalsee = scrapy.Field()
    totalcomments = scrapy.Field()
    playcounts = scrapy.Field()
    upcounts = scrapy.Field()
    downcounts = scrapy.Field()
    isvip = scrapy.Field()
    actors = scrapy.Field()
