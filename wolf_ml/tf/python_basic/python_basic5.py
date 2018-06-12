#coding=utf-8

def func1():
    """
    set的使用功能
    """
    a = set()
    a.add('a')
    a.add('b')
    print(a)

    #set转list
    print(list(a))

    #list转set
    b = ['a','b','a']
    print(set(b))

    #set求并集
    c = {'a','b','c'}
    print(a|c)

    #这种方法只能使用if不能使用else
    d = [1 for i in c if i in a]
    #生成集合
    d = {1 for i in c if i in a}
    #生成字典
    d = {i:i for i in c if i in a}
    print(d)

    #使用if和else 都可以使用
    d = [1 if i in a else 0 for i in c]
    print(d)

def func2():
    """
    math的功能使用
    """
    import math
    print(math.pow(2, 4))  #2^4
    print(math.sqrt(5))

def func3():
    punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
            ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
            々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
            ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    # 对str/unicode
    filterpunt = lambda s: ''.join(filter(lambda x: x not in punct, s))
    # 对list
    filterpuntl = lambda l: list(filter(lambda x: x not in punct, l))
    st = '好,不.好!吧'
    print(filterpunt(st)) #好不好吧

    """
    方法二：使用re
    注：1、字符编码问题
        2、pointwords中大小顺序问题  re.sub() 过滤使用的屏蔽字符从小到大
    """
    import re
    pointwords = ['，', '、', '[', ']', '（', '）', '：',
        '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
        '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
        '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃']
    line = '好,不.好!吧'
    line = re.sub(pointwords, '', line)
    print(line)

def func4():
    from gensim.models.keyedvectors import KeyedVectors
    from gensim.models.word2vec import Word2Vec
    import os
    bin_file = 'vectors.bin'
    text_file = 'vectors.txt'
    bin_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), bin_file)
    text_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), text_file)
    model = KeyedVectors.load_word2vec_format(bin_file, binary=True)
    model.save_word2vec_format(text_file, binary=False)

    model = Word2Vec()
    model.wv.save_word2vec_format('a.txt', binary=False)

def func5():
    from collections import Counter
    """
        两个dict合并：
            方法1：(速度较慢)
                dictMerged1=dict(dict1.items()+dict2.items())
            方法2：
                dictMerged2=dict(dict1, **dict2)
            方法2等同于：
                dictMerged=dict1.copy()
                dictMerged.update(dict2)
            方法4：
                dictMerged=dict(dict1)
                dictMerged.update(dict2)
    """
    d1 = {'1':1,'2':2}
    d2 = {"4":4,"5":5, '2':6}
    d2 = dict(d1, **d2)

    d3 = d1.copy()
    d3.update(d2)

    d2 = dict(Counter(d1)+Counter(d2))
    print(d2)

def func6():
    """
        一个星（*）：表示接收的参数作为元组来处理
        两个星（**）：表示接收的参数作为字典来处理
    """
    a = [('1',1),('2',2),('3',3)]
    x,y = zip(*a)  #这里如果不加*的话，就会报错
    print('x ', x)
    print('y ', y)

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    #func5()
    func6()
