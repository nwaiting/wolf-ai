#coding=utf-8

import threading

def main():
    """
        for (var t = "",
        a = 0; a < e.length; a++) {
            var i = e.charCodeAt(a).toString(16);
            2 == i.length ? t += "n" + i: t += i
        }
        return t

    好吃吗
    597d54035417
    啊
    554a
    """
    """
    import binascii
    t = ''
    for i in u'啊':
        j = binascii.b2a_hex(i.encode('utf-8'))
        print j
        if len(j) == 2:
            t += "n" + j
        else:
            t += j
    print t
    print binascii.b2a_hex(u'啊'.encode('utf-8'))

    def toHex(s):
        lst = []
        for ch in s:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0'+hv
            lst.append(hv)

        return reduce(lambda x,y:x+y, lst)
    print 'aaaaa ', toHex(unicode('啊', 'utf-8'))
    print ' 771f76844e0d597d ======='
    print toHex(u'真的不好')

    #print(binascii.b2a_hex('好吃吗'.encode('utf_8')))
    """
def show():
    import time
    print("this is show {0}".format(time.time()))
    scher.enter(2, 1, show)

def show2():
    import time
    print("show2 {0}".format(time.time()))
    scher.enter(3, 1, show2)

if __name__ == '__main__':
    import random
    print(random.random()%1)
    print(random.random()%1)
    print(random.random()%1)
    print(random.random()%1)
    print([0.] * 4)
    import platform
    print(platform.python_version())
    import sys
    sys.exit(0)
    """
    import sched
    import time
    scher = sched.scheduler(time.time, time.sleep)
    scher.enter(2, 1, show, ())
    scher.enter(3, 1, show2, ())
    #scher.run()
    import urllib2
    try:
        res = urllib2.urlopen("http://download.firefox.com.cn/releases-sha2/stub/official/zh-CN/F-latest.exe", timeout=1)
    except Exception as e:
        print "error {0}".format(e)
    res = urllib2.urlopen("http://download.firefox.com.cn/releases-sha2/stub/official/zh-CN/Firefox-latest.exe", timeout=1)
    print res.getcode()
    print len(res.read())
    print "============== urllib"
    import urllib
    res = urllib.urlopen('http://download.firefox.com.cn/releases-sha2/stub/official/zh-CN/Firefox-latest.exe')
    print type(res.getcode()), res.getcode()  #int 200
    print len(res.read())
    """
