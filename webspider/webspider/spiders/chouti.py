# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.http.cookies import CookieJar
import urlparse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.cn']

    page_pre = 'http://dig.chouti.com'
    login_url = 'http://dig.chouti.com/login'
    like_page_template = 'http://dig.chouti.com/link/vote?linksId={0}'

    start_urls = ['http://dig.chouti.com/']

    cookie_dict = dict()

    def start_requests(self):
        flag = 0
        if flag:
            url = 'http://dig.chouti.com/link/vote?linksId=15499806'
            yield Request(url=url,
                method='POST',
                body='linksId=15499806',
                cookies={'gpsd':'fc66b83a2a50501cac42d0969f799718',
                        #'gpid':'b64c06d3d4ab43189888e26be81b7a9b',
                        #'JSESSIONID':'aaaQv4X1OwyR97igGL2-v',
                        #'route':'340ad5ec7bdbaaaa2d4d12be04eae5d2',
                        #'_pk_ref.1.a2d5':'%5B%22%22%2C%22%22%2C1511768007%2C%22http%3A%2F%2Fdig.chouti.com%2F%22%5D',
                        #'puid':'81a6d213a393c652e55771010a5d4d44',
                        #'puid':'cdu_51140466163',
                        #'_pk_id.1.a2d5':'287e58bf8ba06508.1511142587.6.1511769506.1511768007.',
                        #'_pk_ses.1.a2d5':'*'
                        },
                callback=self.login
                )
        else:
            url = self.start_urls[0]
            yield Request(url=url, callback=self.login)
    """
        模拟登陆步骤：
        1、获取cookie，
        2、使用cookie、用户名、密码登陆
        3、当验证通过后，后面携带cookie请求
    """
    def login(self, response):
        print response
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        #print cookie_jar._cookies.items()
        for k,v in cookie_jar._cookies.items():
            print k
            for i,j in v.items():
                for m,n in j.items():
                    self.cookie_dict[m] = n.value

        yield Request(url=self.login_url,
            method='POST',
            headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},
            body='phone=8618616561846&password=woshiniba&oneMonth=1',
            cookies=self.cookie_dict,
            dont_filter = True,
            callback=self.login_check)

    def login_check(self, response):
        print response
        #print "response.request.headers =============",response.request.headers
        #print "response.headers ============", response.headers

        """
        for k,v in response.headers.items():
            if k == 'Set-Cookie':
                for m in v:
                    if m.startswith('puid'):
                        first = m.find('=')
                        second = m.find(';')
                        if first and second:
                            self.cookie_dict['puid'] = m[first+1:second]
        print self.cookie_dict
        """
        yield Request(url=self.start_urls[0],
            cookies=self.cookie_dict,
            dont_filter=True,
            callback=self.parse_detail)
        """
        print "response ", response
        cookiejar = CookieJar()
        cookiejar.extract_cookies(response, response.request)
        for k, v in cookiejar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        # to to ...
        #for con in response.xpath('//div[@class="part1"]/a[starts-with(@class,"show-content")]/@href').extract():
        #    print con.strip()

        for item in response.xpath('//div[@class="news-content"]'):
            print "item ", item
            print item.xpath('*/a[@class="show-content color-chag"]/@href').extract()

        res = response.xpath('//a[@class="ct_page_edge"]/@href').extract()
        next_page = None
        if len(res) > 1:
            next_page = res[-1]
        else:
            next_page = res[0]

        # yield Request(url=urlparse.urljoin(self.page_pre, next_page),
        #     cookies=self.cookie_dict,
        #     callback=self.parse,
        #     dont_filter=True)
        """

    def parse_detail(self, response):
        print response
        for i in response.xpath('//div[@class="part2"]/@share-linkid').extract():
            print self.like_page_template.format(i)
            body_args = 'linksId={0}'.format(i)
            yield Request(url=self.like_page_template.format(i),
                method='POST',
                body=body_args,
                cookies=self.cookie_dict,
                dont_filter = True,
                callback=self.like_show
                )

    def like_show(self, response):
        print response
