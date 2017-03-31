# -*- coding: utf-8 -*-
import sys 
import os
import scrapy
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import DhseedItem

reload(sys)
sys.setdefaultencoding('utf-8')

class DhseedSpider(scrapy.Spider):
    name = "dhseed"
    allowed_domains = ["dhseed.com"]
    base_url = "http://www.dhseed.com/news_more.asp?lm=168"
    start_urls = ( 
        'http://www.dhseed.com/news_more.asp?lm2=169',
        'http://www.dhseed.com/news_more.asp?lm2=170',
        'http://www.dhseed.com/news_more.asp?lm2=191'
    )   

    def __init__(self):
        self.all_contents = ""
    
    def parse(self, response):
        print "start parse"  


