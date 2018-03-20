#coding=utf8

"""
参考：https://www.jianshu.com/p/1e498888f505
    概述：
        可以计算单词与句子、句子与句子、单词与文档、句子与文档的相关性得分

        通常用作搜索相关性评分，对查询语句进行分词，计算每个词与搜索结果D的相关性得分，最后
            将每个词对于搜索结果D进行加权求和，从而得到查询语句与搜索结果D的相关性得分

    bm25算法相关性得分总结：
        score(Q,d) = IDF(qi) * (fi * (k1 + 1)) / (fi + k1 * (1 - b + b * (dl / avgdl)))
        fi为qi在d中的出现频率
    IDF公式：
        idf(qi) = log((N - n(qi) + 0.5) / n(qi) + 0.5)
        N为全部文档数，n(qi)为包含qi的文档数
"""

import math

class BM25(object):
    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = sum([len(item)+0.0 for item in docs]) / self.D
        self.docs = docs
        self.f = [] #列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
        self.df = {} #存储每个词及出现了该词的文档数量
        self.idf = {} #存储每个词的idf值
        self.k1 = 1.5 #经验值
        self.b = 0.75 #经验值
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for key in doc:
                tmp[key] = tmp.get(key, 0) + 1
            self.f.append(tmp)
            for key in tmp.keys():
                self.df[key] = self.df.get(key, 0) + 1
            for k,v in self.df.items():
                self.idf[k] = math.log(self.D - v + 0.5) -  math.log(v + 0.5)

    def sim(self, doc, index):
        score = 0.0
        for key in doc:
            if key not in self.f[index]:
                continue
            d = len(self.docs[index])
            # 根据 bm25公式
            score += (self.idf[key] * self.f[index][key] * (self.k1 + 1)) / (self.f[index][key] + self.k1 * (1 - self.b + self.b * d / self.avgdl))
        return score

    def simall(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores

def main():
    text = '''
            自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
            它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
            自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
            因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
            所以它与语言学的研究有着密切的联系，但又有重要的区别。
            自然语言处理并不是一般地研究自然语言，
            而在于研制能有效地实现自然语言通信的计算机系统，
            特别是其中的软件系统。因而它是计算机科学的一部分。
            '''
    #分词后结果
    text = [['自然语言', '计算机科学', '领域', '人工智能', '领域', '中', '一个', '方向'],
        ['研究', '人', '计算机', '之间', '自然语言', '通信', '理论', '方法'],
        ['自然语言', '一门', '融', '语言学', '计算机科学', '数学', '一体', '科学'],
        [],
        ['这一', '领域', '研究', '涉及', '自然语言'],
        ['日常', '语言'],
        ['语言学', '研究'],
        ['区别'],
        ['自然语言', '研究', '自然语言'],
        ['在于', '研制', '自然语言', '通信', '计算机系统'],
        ['特别', '软件系统'],
        ['计算机科学', '一部分']]
    bm = BM25(text)
    #print(bm.f)
    #print(bm.idf)
    print(bm.simall(['自然语言', '计算机科学', '领域', '人工智能', '领域']))


if __name__ == "__main__":
    main()
