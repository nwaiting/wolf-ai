#coding=utf8

"""
BeautifulSoup 是一个库，xpath是一种技术，Python中常用的xpath库是lxml
对于lxml和BeautifulSoup原理不一样，BeautifulSoup是基于DOM的，lxml是用c写的，BeautifulSoup是用Python写的，性能方面有差距
使用BeautifulSoup开发方便
"""

from bs4 import BeautifulSoup
webdata = requests.get(url).content
soup = BeautifulSoup(webdata, 'lxml')
soup.select()
