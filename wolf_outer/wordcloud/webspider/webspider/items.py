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

class WebspiderJDItem(scrapy.Item):
    comments = scrapy.Field()
    referenceName = scrapy.Field()
    referenceTime = scrapy.Field()
    productColor = scrapy.Field()
    productSize = scrapy.Field()
