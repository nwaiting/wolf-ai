#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

class ModelHandler(object):
    def __init__(self, model_file):
        self.modelfile_ = model_file
        self.unigram = {}
        self.bigram = {}
        self.trigram = {}

    def Init(self):
        flag = 0
        with open(self.modelfile_, "rb") as f:
            for line in f.xreadlines():
                line = line.strip()
                if flag == 0:
                    if line.endswith("1-grams:"):
                        flag = 1
                        continue
                elif flag == 1:
                    if line.endswith("2-grams:"):
                        flag = 2
                        continue
                    result = re.split(" |\t", line)
                    if len(result) == 3:
                        self.unigram[result[1].strip()] = result[0].strip()
                elif flag == 2:
                    if line.endswith("3-grams:"):
                        flag = 3
                        continue
                    result = re.split(" |\t", line)
                    if len(result) == 4:
                        self.bigram[result[1].strip()] = {result[2].strip():result[0].strip()}
                elif flag == 3:
                    result = re.split(" |\t", line)
                    if len(result) == 4:
                        self.trigram[result[1].strip()] = {result[2].strip():{result[3].strip():result[0].strip()}}

    def GetChineseProb(self, first, second):
        """
        计算两个字的概率 字phrase1和字phrase2
        1、如果在二元模型中有词的概率，直接使用概率
        2、如果没有词的概率，则需要使用平滑计算
            delta可以从phrase1->unknown或者从unknown->phrase2获取的概率
            GetUnigram(phrase1) * GetUnigram(phrase2) * (Math.E + delta)
        """
        if self.unigram.has_key(first+second):
            return self.unigram[first+second]
        if self.bigram.has_key(first):
            if self.bigram[first].has_key(second):
                return self.bigram[first][second]
        return None

if __name__ == '__main__':
    model = ModelHandler('text.train')
    model.Init()
    import os
    print os.getcwd()
    print model.GetChineseProb('好','玩')
