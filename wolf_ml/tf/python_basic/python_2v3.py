#coding=utf-8

"""
    python的编程规范中：
        只有类名为驼峰表达形式，其余都是小写形式
        大驼峰：第一个字母大写
        小驼峰：第一个字母小写
"""

"""
    urllib库的区别：
        在Pytho2.x中使用import urllib2——-对应的，在Python3.x中会使用import urllib.request，urllib.error。
        在Pytho2.x中使用import urllib——-对应的，在Python3.x中会使用import urllib.request，urllib.error，urllib.parse。
        在Pytho2.x中使用import urlparse——-对应的，在Python3.x中会使用import urllib.parse。
        在Pytho2.x中使用import urlopen——-对应的，在Python3.x中会使用import urllib.request.urlopen。
        在Pytho2.x中使用import urlencode——-对应的，在Python3.x中会使用import urllib.parse.urlencode。
        在Pytho2.x中使用import urllib.quote——-对应的，在Python3.x中会使用import urllib.request.quote。
        在Pytho2.x中使用cookielib.CookieJar——-对应的，在Python3.x中会使用http.CookieJar。
        在Pytho2.x中使用urllib2.Request——-对应的，在Python3.x中会使用urllib.request.Request。

    py3使用例子：
        import urllib.request
        import urllib.parse
        import urllib.error
        import http.cookiejar

        url='http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=La2A2'
        data={
            'username':'zhanghao',
            'password':'mima',
        }
        postdata=urllib.parse.urlencode(data).encode('utf8')
        header={
            'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        request=urllib.request.Request(url,postdata,headers=header)
        #使用http.cookiejar.CookieJar()创建CookieJar对象
        cjar=http.cookiejar.CookieJar()
        #使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
        cookie=urllib.request.HTTPCookieProcessor(cjar)
        opener=urllib.request.build_opener(cookie)
        #将opener安装为全局
        urllib.request.install_opener(opener)

        try:
            reponse=urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)

    返回数据的文件编码格式：
        response = urllib.urlopen(dsturl)
        content = response.read().decode('utf-8', 'ignore')

"""
