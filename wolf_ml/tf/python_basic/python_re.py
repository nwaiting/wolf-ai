#coding=utf-8

"""
    正则表达式
"""

import re

def func1():
    s = 'aa-bb'
    res = re.sub(r'-', '', s)
    print(res) #去除-，'aa-bb' -> aabb
    s = '2014/06/11/16/13'
    res = re.sub(r'\d+/\d+/\d+', '', s)
    print(res) #去除日期 '2014/06/11/16/13' -> /16/13
    s = '16:13'
    res = re.sub(r'[0-2]?[0-9]:[0-6][0-9]', '', s)
    print(res) #去除时间  '16:13' -> ''
    s = 'sdof92034@gmail.com'
    res = re.sub(r'[\w]+@[\.\w]+', '', s)
    print(res) #去除时间  'sdof92034@gmail.com' -> ''

    #英文中去除标点符号等，re.sub(r'[~a-zA-Z]','',text) 将除了a到z和A到Z以外的词替换成空


if __name__ == '__main__':
    func1()
