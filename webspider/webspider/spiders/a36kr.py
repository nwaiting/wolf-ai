# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.cookies import CookieJar
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from webspider.items import WebspiderPipeline36krItem

class A36krSpider(scrapy.Spider):
    name = '36kr'
    allowed_domains = ['36kr.com']
    start_urls = ['http://36kr.com/']

    cookie_jar = {}

    def parse(self, response):
        login_url = 'https://passport.36kr.com/passport/sign_in'
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        for m,n in cookie_jar._cookies.items():
            for m1,n1 in n.items():
                for m2,n2 in n1.items():
                    if m2 in ['aliyungf_tc', 'krnewsfrontss', 'device-uid', 'M-XSRF-TOKEN']:
                        self.cookie_jar[m2] = n2.value
        """
        type:login
        bind:false
        needCaptcha:false
        username:18616561846
        password:abcd.1234
        ok_url:https%3A%2F%2Frong.36kr.com%2Flist%2Fdetail%26%3FsortField%3DHOT_SCORE
        ktm_reghost:null
        """

        yield scrapy.Request(url=login_url,
            method='POST',
            body='type=login&bind=false&needCaptcha=false&username=18616561846&password=abcd.1234&\
                    ok_url=https%3A%2F%2Frong.36kr.com%2Flist%2Fdetail%26%3FsortField%3DHOT_SCORE&ktm_reghost=null',
            headers={'Content-Type':'application/x-www-form-urlencoded'},
            cookies=self.cookie_jar,
            callback=self.login
            )

    @staticmethod
    def restr(instr, pattenstr):
        patten = re.compile(pattenstr)
        return patten.findall(instr)

    def login(self, response):
        print response
        for m,n in response.headers.items():
            if m == 'Set-Cookie':
                for contents in n:
                    if contents.startswith('_kr_p_se'):
                        p = r'(?<=_kr_p_se=).*?(?=;)'
                        res = self.restr(contents, p)
                        if len(res) > 0:
                            self.cookie_jar['_kr_p_se'] = res[0]

                    if contents.startswith('krid_user_version'):
                        p = r'(?<=krid_user_version=).*?(?=;)'
                        res = self.restr(contents, p)
                        if len(res) > 0:
                            self.cookie_jar['krid_user_version'] = res[0]

                    if contents.startswith('krid_user_id'):
                        p = r'(?<=krid_user_id=).*?(?=;)'
                        res = self.restr(contents, p)
                        if len(res) > 0:
                            self.cookie_jar['krid_user_id'] = res[0]

        #print self.cookie_jar
        #request_url = 'https://rong.36kr.com/list/detail&?sortField=HOT_SCORE'
        #request_url = 'https://rong.36kr.com/n/api/column/0/company?sortField=HOT_SCORE&p=1'
        for i in xrange(1, 100):
            request_url = 'https://rong.36kr.com/n/api/column/0/company?sortField=HOT_SCORE&p={0}'.format(i)
            yield scrapy.Request(url=request_url,
                cookies=self.cookie_jar,
                callback=self.parse_detail)

    def parse_detail(self, response):
        print response
        json_contents = json.loads(response.text)
        if json_contents.has_key('data') and json_contents['data'].has_key('pageData') and json_contents['data']['pageData'].has_key('data'):
            for item in json_contents['data']['pageData']['data']:
                i36kr_item = WebspiderPipeline36krItem()
                i36kr_item['name'] = ''
                if item.has_key('name'):
                    i36kr_item['name'] = item['name']

                i36kr_item['brief'] = ''
                if item.has_key('brief'):
                    i36kr_item['brief'] = item['brief']

                i36kr_item['city'] = ''
                if item.has_key('cityStr'):
                    i36kr_item['city'] = item['cityStr']

                i36kr_item['industry'] = ''
                if item.has_key('industryStr'):
                    i36kr_item['industry'] = item['industryStr']

                i36kr_item['time'] = ''
                if item.has_key('startDate'):
                    i36kr_item['time'] =  item['startDate']

                i36kr_item['phase'] = ''
                if item.has_key('phase'):
                    i36kr_item['phase'] =  item['phase']
                yield i36kr_item
