# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.cookies import CookieJar
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
        print self.cookie_jar
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
        print '==================='
        print response.request.headers
        print response.request.body
        print '==================='
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
        request_url = 'https://rong.36kr.com/list/detail&?sortField=HOT_SCORE'
        yield scrapy.Request(url=request_url,
            cookies=self.cookie_jar,
            callback=self.parse_detail
            )

    def parse_detail(self, response):
        print response
