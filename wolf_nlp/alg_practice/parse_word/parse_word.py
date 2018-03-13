# -*- coding: UTF-8 -*-

import math

"""
http://www.isnowfy.com/python-chinese-segmentation/
使用了dp算法
根据马尔科夫链，求概率最大值
注：
    1、如果词语在词典中没有出现，会出现概率为0的情况，所以需要smooth
    2、如果计算概率的时候，由于归一化之后，频率都是小于1的，所以乘太多的话，会变成0，影响整个算法，
        理论上用log的计算方法是最好的，将多个概率相乘变成概率相加
"""

d = {}
log = lambda x: float('-inf') if not x else math.log(x)
prob = lambda x: d[x] if x in d else 0 if len(x)>1 else 1

def init(filename='SogouLabDic.dic'):
    d['_t_'] = 0.0
    with open(filename, 'r') as handle:
        for line in handle:
            word, freq = line.split('\t')[0:2]
            d['_t_'] += int(freq)+1  #smooth
            try:
                d[word.decode('gbk')] = int(freq)+1
            except:
                d[word] = int(freq)+1

def solve(s):
    l = len(s)
    p = [0 for i in range(l+1)]
    t = [0 for i in range(l)]
    for i in xrange(l-1, -1, -1):
        p[i], t[i] = max((log(prob(s[i:i+k])/d['_t_'])+p[i+k], k)
                        for k in xrange(1, l-i+1))
    while p[l]<l:
        yield s[p[l]:p[l]+t[p[l]]]
        p[l] += t[p[l]]

if __name__ == '__main__':
    #init()
    s = u'其中最简单的就是最大匹配的中文分词'
    print(len(s))
    #print ' '.join(list(solve(s)))
    dd = {}
    dd['a'] = 3
    dd['b'] = 4
    pro = lambda x: dd[x] if x in dd else 0 if len(x)>1 else 1
    print(pro('cc'))
    print(pro('a'))
