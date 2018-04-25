# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 12:37:24 2018

@author: Administrator
"""

"""
Created on 2018-04-17 @author: Eastmount
分词
输入：文件夹中对应0001.txt-2000.txt
输出：一个2000篇txt整合所有文本 每行对应一个文本分词结果
"""

import sys
import re
import codecs
import os
import shutil
import jieba
import jieba.analyse


#Read file and cut
def read_file_cut():

    #去除标点符号
    pointwords = ['，', '、', '[', ']', '（', '）', '：',
        '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
        '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
        '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃']
    pt = set(pointwords)
    fp = lambda s: ''.join(filter(lambda x: x not in pt, s))

    #create path
    pathBaidu = "./BaiduSpiderCountry/"
    resName = "Result_Country.txt"
    if os.path.exists(resName):
        os.remove(resName)

    result = open(resName, 'wb')

    for num in range(1,2001):
        name = "%04d" % num
        fileName = pathBaidu + str(name) + ".txt"
        if os.path.exists(fileName):
            with open(fileName, 'r', encoding='utf-8') as source:
                for line in source.readlines():
                    line = line.strip('\r\n ')
                    if line:
                        #line = re.sub(pointwords, '', line)
                        line = fp(line)
                        seglist = jieba.cut(line,cut_all=False)  #精确模式
                        result.write(('{0}\n'.format(' '.join(list(seglist)))).encode('utf-8'))
    result.close()
    print('end ')

if __name__ == '__main__':
    read_file_cut()
