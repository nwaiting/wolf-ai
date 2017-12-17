# -*- coding: utf-8 -*-
import scrapy


class AizhanSpider(scrapy.Spider):
    name = "aizhan"
    allowed_domains = ["aizhan.com"]
    start_urls = ['https://ci.aizhan.com/']

    def start_requests(self):
        first_word = u'怎么样啊'
        url = self.start_urls[0] + self.toHex(first_word) + '/'
        url = u'https://www.baidu.com/s?wd=百度搜索查询接口&cl=3'
        """
         Hm_lpvt_b37205f3f69d03924c5447d020c09192=1513444078
         Hm_lvt_48ab1161bd8d22a908e781b591c6ff51=1513436785;
         Hm_lpvt_48ab1161bd8d22a908e781b591c6ff51=1513436813;
         Hm_lvt_b37205f3f69d03924c5447d020c09192=1513433584;

         _csrf=a89cfe7b05c491eb2759fcdb64e3e4df686afd02d04c3771cd8514094cbbfe8da%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Jqo2x5uuBXMzvNZyONprYdBO9FoPT6_5%22%3B%7D;
         Hm_lvt_b37205f3f69d03924c5447d020c09192=1513433584;
          Hm_lvt_48ab1161bd8d22a908e781b591c6ff51=1513436785;
           Hm_lpvt_48ab1161bd8d22a908e781b591c6ff51=1513436813;
           userId=1018843;
           userName=798990255%40qq.com;
           userGroup=1;
           userSecure=eLpy6YL1m%2B96i1idK7dK7csucrbyvUtMeFlCpxlve51zH5ImT0CXFZWNEaKclm42PJDLSg%3D%3D;
           Hm_lpvt_b37205f3f69d03924c5447d020c09192=1513446228
_csrf=a89cfe7b05c491eb2759fcdb64e3e4df686afd02d04c3771cd8514094cbbfe8da%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Jqo2x5uuBXMzvNZyONprYdBO9FoPT6_5%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1513433584; Hm_lvt_48ab1161bd8d22a908e781b591c6ff51=1513436785;
Hm_lpvt_48ab1161bd8d22a908e781b591c6ff51=1513436813;
 userId=1018843;
 userName=798990255%40qq.com;
 userGroup=1;
 userSecure=Wa6vLbwrHTQlYtKnZK2y2E2htWY97amflsYpnjGs9IK1E2zLysdL1eWBMcPB3JMR;
  Hm_lpvt_b37205f3f69d03924c5447d020c09192=1513447267
        """
        cookie_jar={'_csrf':'a89cfe7b05c491eb2759fcdb64e3e4df686afd02d04c3771cd8514094cbbfe8da%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Jqo2x5uuBXMzvNZyONprYdBO9FoPT6_5%22%3B%7D'
                    ,'Hm_lvt_b37205f3f69d03924c5447d020c09192':'1513433584'
                    ,'Hm_lvt_48ab1161bd8d22a908e781b591c6ff51':'1513436785'
                    ,'Hm_lpvt_48ab1161bd8d22a908e781b591c6ff51':'1513436813'
                    ,'userId':'1018843'
                    ,'userName':'798990255%40qq.com'
                    ,'userGroup':'1'
                    ,'userSecure':'Wa6vLbwrHTQlYtKnZK2y2E2htWY97amflsYpnjGs9IK1E2zLysdL1eWBMcPB3JMR'
                    ,'Hm_lpvt_b37205f3f69d03924c5447d020c09192':'1513447267'
                    }
        yield scrapy.Request(url=url,
                #cookies=cookie_jar,
                callback=self.parse)

    def parse(self, response):
        print "==============================="
        print response
        print response.text

    def toHex(self,s):
        lst = []
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)
        return reduce(lambda x,y:x+y, lst)
