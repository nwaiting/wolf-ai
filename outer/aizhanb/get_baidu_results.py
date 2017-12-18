#coding=utf-8
import requests
from scrapy.selector import Selector
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

all_words_path = ''
requests_baidu_pre = 'https://www.baidu.com/s?wd={0}&cl=3'
#url = u'https://www.baidu.com/s?wd=百度搜索查询接口&cl=3'
req_headers = {'user-agent':'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2'}

def main():
    line = '王者荣耀女英'
    new_url = requests_baidu_pre.format(line)
    res = requests.get(url=new_url, headers=req_headers)
    if res.text.find('<span class="c-showurl">tieba.baidu.com') != -1:
        print "================= tieba has"
    sel = Selector(text=res.text)
    for item in sel.xpath('//div[@class="c-showurl c-line-clamp1"]/a/span[0]/text()').extract():
        if item:
            index = item.find('tieba')
            if index != -1:
                print "================= {0} tieba has".format(item)
    with open('xxxx.data', 'wb') as f:
        f.write(res.text)
    """
    with open(all_words_path, 'rb') as f:
        for line in f.xreadlines():
            if line:
                line = line.strip()
                new_url = requests_baidu_pre.format(line)
                res = requests.get(url=new_url, headers=req_headers)
    """

if __name__ == '__main__':
    main()
