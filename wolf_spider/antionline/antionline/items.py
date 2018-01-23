# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AntionlineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    art_title = scrapy.Field()
    art_content = scrapy.Field(serializer=str)
    art_from = scrapy.Field()
    art_author = scrapy.Field()
    art_read = scrapy.Field()
    art_pub_time = scrapy.Field()
