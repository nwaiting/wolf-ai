# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import gzip
import marshal
from math import log, exp

from ..utils.frequency import AddOneProb


class Bayes(object):

    def __init__(self):
        self.d = {}
        self.total = 0

    def save(self, fname, iszip=True):
        d = {}
        d['total'] = self.total
        d['d'] = {}
        for k, v in self.d.items():
            d['d'][k] = v.__dict__
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            marshal.dump(d, open(fname, 'wb'))
        else:
            f = gzip.open(fname, 'wb')
            f.write(marshal.dumps(d))
            f.close()

    def load(self, fname, iszip=True):
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            d = marshal.load(open(fname, 'rb'))
        else:
            try:
                f = gzip.open(fname, 'rb')
                d = marshal.loads(f.read())
            except IOError:
                f = open(fname, 'rb')
                d = marshal.loads(f.read())
            f.close()
        self.total = d['total']
        self.d = {}
        for k, v in d['d'].items():
            self.d[k] = AddOneProb()
            self.d[k].__dict__ = v

    def train(self, data):
        for d in data:
            c = d[1]
            if c not in self.d:
                self.d[c] = AddOneProb()
            for word in d[0]:
                self.d[c].add(word, 1)
        self.total = sum(map(lambda x: self.d[x].getsum(), self.d.keys()))

    def classify(self, x):
        """
            获取x在哪一类中出现的概率最大
        """
        tmp = {}
        #遍历每个分类标签
        for k in self.d:
            #获取每个分类标签下的总词数和所有标签总词数，求对数(某类标签下的总词数/所有标签总词数)
            tmp[k] = log(self.d[k].getsum()) - log(self.total)
            for word in x:
                #获取每个单词出现的频率log[(某标签下的总词数/所有标签总词数)*单词出现频率]
                #如果需要分类的词在k中出现越大，那么tmp[k]越大
                tmp[k] += log(self.d[k].freq(word))
        ret, prob = 0, 0
        for k in self.d:
            now = 0
            try:
                for otherk in self.d:
                    now += exp(tmp[otherk]-tmp[k])
                now = 1/now
            except OverflowError:
                now = 0
            if now > prob:
                ret, prob = k, now
        return (ret, prob)
