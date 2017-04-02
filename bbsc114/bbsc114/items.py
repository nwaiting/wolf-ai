# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Bbsc114Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_name = scrapy.Field()
    title_type = scrapy.Field()
    answers = scrapy.Field()
    status = scrapy.Field()
    handle_time = scrapy.Field()
    title_content = scrapy.Field(serializer=str)
    
