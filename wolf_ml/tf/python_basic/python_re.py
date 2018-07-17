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

def func2():
    """
        “.”的作用是匹配除“\n”以外的任何字符

        字符串分割：
            re.split(r'[\s\,\;]+', 'a,b;; c  d') 结果为：['a', 'b', 'c', 'd']
            \s：用于匹配单个空格符，包括tab键和换行符等任何不可见字符
            \S：用于匹配除单个空格符之外的所有字符；
            \d：用于匹配从0到9的数字；
            . ：用于匹配除换行符之外的所有字符。
            \w：用于匹配字母，数字或下划线字符；
            \W：用于匹配所有与\w不匹配的字符；
            例如：
                regex=re.compile("\w+\s+\w+");
                regex.findall('2345  3456  4567  5678');
                第一次匹配到'2345  3456'，由于是贪婪模式会继续匹配，第二次从'4567'开始，匹配到结果'4567  5678'

        元字符：
            较为常用的元字符包括： “+”， “*”，以及 “?”
            “+”元字符规定其前导字符必须在目标对象中连续出现一次或多次
            “*”元字符规定其前导字符必须在目标对象中出现零次或连续多次
            “?”元字符规定其前导对象必须在目标对象中连续出现零次或一次
    """

def func3():
    """
        贪婪和非贪婪：
            贪婪：python里数量词默认是贪婪的（在少数语言里也可能默认是非贪婪的），总数尝试匹配尽可能多的字符
                在'* ? + {m,n}'后面加上?，使贪婪变成非贪婪
            非贪婪：总数尝试匹配尽可能少的字符
            例子：
                example = "abbbbbbc"
                pattern = re.compile("ab+")
                贪婪模式：最大匹配，匹配结果为abbbbbb
                非贪婪模式：匹配结果为ab
    """
    #贪婪模式
    example = "abbbbbbc"
    pattern = re.compile("ab+")
    print(pattern.findall(example))
    #非贪婪模式
    pattern = re.compile("ab+?")
    print(pattern.findall(example))


def func4():
    """
        1、re.match(pattern, string)
            匹配成功，返回match对象
        2、re.search(pattern, string)
            匹配成功，返回Match对象，如果string中存在多个patten子串，只返回一个
        3、re.findall(pattern, string)
            返回搜优匹配的字符串，数组形式
        4、re.finditer(pattern, string)
            返回匹配的所有字符串，迭代器形式
    """







if __name__ == '__main__':
    #func1()

    func3()
