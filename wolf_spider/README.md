# scrapy-0331
<!--
1、git clone git@github.com:abcd1f2/scrapy-0331.git 拉取代码

每个工程下都有一个settings.py文件里面配置有数据库信息：
db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_passwd = 'root'
db_name = 'spider'

!!!!!!!注意:
需要在本地有安装mysql数据库，用户名root，密码root
每个目录下都有settings.py，查看的时候查看对应的数据表

开始测试：
antionline: done
settings.py文件位置：scrapy-0331/antionline/antionline/settings.py
1、进入scrapy-0331/antionline 目录
2、执行命令 (CONCURRENT_REQUESTS：站点防爬 减缓爬取速度)
scrapy crawl antionline -s CONCURRENT_REQUESTS=25

caas: done
注：我在服务器上测试的时候发现直接连不上这个域名，需要做以下两步：
    1、先在别的机器，比如window上ping出这个域名对于的IP，打开cmd窗口，执行 ping icgr.caas.net.cn
    2、将自己服务器上/etc/hosts中添加 111.203.21.75 icgr.caas.net.cn 这一行
1、进入scrapy-0331/caas 目录
2、执行命令
scrapy crawl caas -s CONCURRENT_REQUESTS=25

chinaseed114: done
1、进入scrapy-0331/chinaseed114 目录
2、执行命令
scrapy crawl chinaseed114

dh31: done
1、进入scrapy-0331/dh31 目录
2、执行命令
scrapy crawl dh31 -s CONCURRENT_REQUESTS=25

dhseed: done
1、进入scrapy-0331/dhseed 目录
2、执行命令
scrapy crawl dhseed

fengle: done
1、进入scrapy-0331/fengle 目录
2、执行命令
scrapy crawl fengle

kiplinger:
1、进入scrapy-0331/kiplinger 目录
2、执行命令
scrapy crawl kiplinger

originseed: done
1、进入scrapy-0331/originseed 目录
2、执行命令
scrapy crawl originseed -s CONCURRENT_REQUESTS=25

seedtest:
注:需要安装Python解析pdf的库，pip install pdfminer
1、进入scrapy-0331/seedtest 目录
2、执行命令
scrapy crawl seedtest -s CONCURRENT_REQUESTS=25

yahoo:

-->

### 爬虫开源资源
https://github.com/Jack-Cherish/python-spider 验证码破解 vip视频破解等
