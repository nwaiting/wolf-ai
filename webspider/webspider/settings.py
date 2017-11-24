# -*- coding: utf-8 -*-

# Scrapy settings for webspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'webspider'

SPIDER_MODULES = ['webspider.spiders']
NEWSPIDER_MODULE = 'webspider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webspider (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#    'Accept-Encoding': 'gzip, deflate, sdch',
#    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
#    'Cache-Control': 'no-cache',
#    'Cookie': 'CXID=21DFA4BB4F4AC8AC1D7B654C27A86E6E; SUID=DC3F6E244B6C860A568F3438000BBA02; SUV=00F22484246E3FDC5698E3B23EF02547; GOTO=; ld=Tkllllllll2ga@pYqh@euOtsDBPga@pzJpc@Tlllll9llllxjK@@@@@@@@@@@@@@; cd=1462759834&0e4f734bc44c6b94eb0c55d652856a58; rd=Tkllllllll2ga@pYqh@euOtsDBPga@pzJpc@Tlllll9llllxjK@@@@@@@@@@@@@@; ABTEST=2|1463014549|v1; weixinIndexVisited=1; SNUID=DC3E6F24000432CA00010C9A01146570; sct=10; JSESSIONID=aaas3h6v8QyHibVAGsnrv; PHPSESSID=f5f6fj5qermt5kmjkmvd7d3u86; SUIR=DC3E6F24000432CA00010C9A01146570; ad=8MLRxZllll2Q08yclllllVtfbIUlllllJpc@Tlllllwlllll9ylll5@@@@@@@@@@; IPLOC=CN1100; LSTMV=315%2C189; LCLKINT=9279',
#    'Upgrade-Insecure-Requests': '1',
#    #'Referer': 'http://weixin.sogou.com/weixin?query=%E5%A4%A7%E6%95%B0%E6%8D%AE%E6%96%87%E6%91%98',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'webspider.middlewares.WebspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'webspider.middlewares.MyCustomDownloaderMiddleware': 543,
    'webspider.middlewares.RandomUserAgentDownMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'webspider.pipelines.WebspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 1
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DEPTH_LIMIT = 2
