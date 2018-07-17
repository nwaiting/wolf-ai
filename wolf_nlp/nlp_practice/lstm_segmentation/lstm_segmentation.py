#coding=utf-8

import re
import os
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pandas as pd

#清理不规范的数据
def clean(s):
    if u'“/s' not in s:
        return s.replace(u' ”/s', '')
    elif u'”/s' not in s:
        return s.replace(u'“/s ', '')
    elif u'‘/s' not in s:
        return s.replace(u' ’/s', '')
    elif u'’/s' not in s:
        return s.replace(u'‘/s ', '')
    return s

def get_xy(s):
    s = re.findall('(.)/(.)', s)
    if s:
        #s = np.array(s)
        #return list(s[:, 0]),list(s[:, 1])
        return [i[0] for i in s], [i[1] for i in x]

def trans_one(x):
    #np_utils.to_categorical convert integers to dummy variables (one hot encoding)
    # reshape(-1) 变成一行，reshape(-1, 1)变成一列
    _ = list(pd.get_dummies(tag[x].reshape(-1)))
    _.extend([np.array([[0,0,0,0,1]])] * (max_len - len(x)))
    return np.array(_)

def viterbi(nodes):
    paths = {'b':nodes[0]['b'], 's':nodes[0]['s']}
    for l in range(1, len(nodes)):
        paths_ = paths.copy()
        paths = {}
        for i in nodes[1].keys():
            nows = {}
            for j in paths_.keys():
                if j[-1]+i in zy.keys():
                    nows[j+i] = paths_[j] + nodes[l][i] + zy[j[-1]+i]
            k = np.argmax(nows.values())
            paths[nows.keys()[k]] = nows.values()[k]
    return paths.keys()[np.argmax(paths.values())]

def simple_cut(s):
    if s:
        r = model.predict()
        r = np.log(r)
        nodes = [dict(zip(['s','b','m','e'], i[:4])) for i in r]
        t = viterbi(nodes=nodes)
        words = []
        for i in range(len(s)):
            if t[i] in ['s','b']:
                words.append(s[i])
            else:
                words[-1] += s[i]
        return words
    else:
        return []

not_cuts = re.compile(u'([\da-zA-Z ]+)|[。，、？！\.\>,!]')
def cut_word(s):
    result = []
    j = 0
    for i in not_cuts.finditer(s):
        # extend类似于list + list
        result.extend(simple_cut(s[j:i.start()]))
        result.append(s[i.start():i.end()])
        j = i.end()
    result.extend(simple_cut(s[j:]))
    return result


# 分词后最长的词
max_len = 32
word_size = 128

def main(file):
    s = ''
    with open(file, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            if line:
                line = line.strip('\r\n ')
                s += clean(line) + ' '
    s = re.split(u'[，。！？、]/[bems]', s)

    #生成训练样本
    data = []
    label = []
    for item in s:
        x = get_xy(item)
        if x:
            data.append(x[0])
            label.append(x[1])

    d = pd.DataFrame(index=range(len(data)))
    d['data'] = data
    d['label'] = label
    d = d[d['data'].apply(len) <= max_len]
    d.index = range(len(d))
    #5tag模式，x用于不足32个字符时，填充的字符
    tag = pd.Series({'s':0, 'b':1, 'm':2, 'e':3, 'x':4})

    #统计所有字与编号
    chars = []
    for i in data:
        chars.append(i)
    chars = pd.Series(chars).value_counts()
    chars[:] = range(1, len(chars)+1)

    #生成模型的输入格式
    d['x'] = d['data'].apply(lambda x:np.array(list(chars[x]) + [0]*(max_len - len(x))))
    d['y'] = d['label'].apply(trans_one)

    #设计模型
    lstm_bw_cell = rnn.BasicLSTMCell()
    lstm_fw_cell = rnn.BasicLSTMCell()

    batch_size = 1024
    history = model.fit()

    #转移概率 默认使用等概率
    zy = {'be':0.5,
            'bm':0.5
            'eb':0.5,
            'es':0.5,
            'me':0.5,
            'mm':0.5,
            'sb':0.5,
            'ss':0.5}
    zy = {i:np.log(zy[i]) for i in zy.keys()}





















if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'msr_train.txt')
    #main(file_name)

    data = [1,2,3,4,5,6]
    res = np.array(data)
    print(res)
    res = res.reshape(-1, 1)
    print(res)
    r = pd.get_dummies(data=data)
    print(r)
