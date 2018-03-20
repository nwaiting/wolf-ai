#coding=utf8

"""
自动文摘主要算法:
    1、基于统计：统计词频、位置等信息，计算句子权重
    2、基于图模型：构建拓扑结构图，对句子排序，如TextRank/LexRank
    3、基于潜在语义：使用主题模型，挖掘语句隐藏信息，如LDA/HMM等
    4、基于整数规划：将文摘问题转化为整数线性规划，求全局最优解

自动摘要算法：
    1、tf-idf，最常见也是最容易实现的算法，但是效果一般
    2、TextRank算法效果好于tf-idf
        针对文本里的句子设计权重算法，利用投票原理，让每一个句子给它的邻居投票，票的权重取决于自己的票数

TextRank算法应用：
    1、文本生成关键词
    2、文本自动摘要

TextRank算法来提取文章的摘要，TextRank类似于PageRank算法，借助于PageRank的算法思想
两个算法区别：
    PageRank的边是没有权值的，TextRank的边是有权值的，TextRank边表示两个句子的相似性，
    边的权值计算：
        (1)Jaccard similarity coefficient就是交集数目除以并集数目
        (2)cosine的余弦夹角
        (3)bm25一类的算法(snowNLP使用的算法)

1、提取关键词：
    流程：
        (1)、分词，选取其中的名词、动词、形容词、副词
        (2)、每个词作为一个节点，设定窗口大小n，每个单词将票投给它身前身后距离5以内的单词
        (3)、迭代计算，阻尼系数一般设置为0.85，直到图中任意一点的误差率小于给定的极限值就可以达到收敛，一般极限值为0.0001

2、提取摘要
    流程：
        (1)：预处理，将文本分割成句子，构建图，将句子分词，得到每个句子的分词
        (2)：句子相识度计算，算法有：编辑距离、基于语义词典、余弦相似度、BM25等
        (3)：迭代计算句子权重得分，进行排序，抽取最高权重的前N的句子

BM25算法：
    概述：通常用作搜索相关性评分，对查询语句进行分词，计算每个词与搜索结果D的相关性得分，最后
        将每个词对于搜索结果D进行加权求和，从而得到查询语句与搜索结果D的相关性得分。

        判断一个词与一个文档的相关性的权重，常用的是IDF：
        IDF(qi) = log((N - n(qi) + 0.5) / (n(qi) + 0.5))
        N就是索引中的全部文档，n(qi)为包含qi的文档数
        根据公式可以看出，对于给定的文档集合，包含qi的文档越多，qi的权重越低

TextRank提取摘要即提取关键句子：
    1、将文本分成很多句子
    2、将句子分词
    3、计算每个句子之间的权值，有多种方法，
        a:  similarity(si,sj) = ((tk ∈ si)&(tk ∈ sj)) / (log(si) + log(sj))
            在si和sj中都有的单词与分母的比值，分母是si和sj词数量的对数
        b:  使用BM25算法计算两个句子的权值
    4、迭代计算，最后排序，将重要度最高的句子选取出来作为文摘


    PageRank公式：
        S(vi) = (1 - d) + d * ∑(1 / |out(vj)|) * S(vj)
                             j∈in(vi)
        阻尼系数，代表从某一点指向其他任意点的概率，一般取值为0.85
        in(vi)--为指向改顶点的点集合(比如单词A跟着单词B，则A属于in(B))
        out(vi)--为vi指向的点集合

    TextRank公式：
        S(vi) = (1 - d) + d * ∑(wji / ∑vk∈out(vj) wjk) * S(vj)
                             j∈in(vi)
        阻尼系数，代表从某一点指向其他任意点的概率，一般取值为0.85
        wij就是节点vi到vj的边的权值
        in(vi)--为指向vi顶点的点集合(比如单词A跟着单词B，则A属于in(B))
        out(vi)--为vi指向的点集合 从节点vi出发的节点
        s(vj)代表上次迭代到j的权重
"""

class TextRank(object):
    def __init__(self, docs):
        self.docs = docs
        self.D = len(docs)
        self.bm25 = BM25(docs)
        self.d = 0.85
        self.weight = []
        self.weight_sum = []
        self.vertex = []
        self.max_iter = 200
        self.min_diff = 0.001
        self.top = []

    def text_rank(self, text):
        for i,doc in enumerate(self.docs):
            scores = self.bm25.simall(doc)
            self.weight.append(scores)
            # 求分母
            self.weight_sum.append(sum(scores) - scores[i])
            #初始化所有的TextRank值
            self.vertex.append(1.0)
        for _ in range(self.max_iter):
            m = []
            max_diff = 0.0
            for i in range(self.D):
                m.append(1 - self.d)
                for j in range(self.D):
                    if j == i and self.weight_sum[j] == 0:
                        continue
                    m[-1] += (self.d * self.weight[j][i] / self.weight_sum[j] * self.vertex[j])
                if abs(m[-1] - self.vertex[i]) > max_diff:
                    max_diff = abs(m[-1] - self.vertex[i])
            self.vertex = m
            if max_diff <= self.min_diff:
                #收敛 退出循环
                break
            self.top = list(enumerate(self.vertex))
            self.top = sorted(self.top, key=lambda x: x[1], reverse=True)

    def top(self, limit):
        return list(map(lambda x:self.docs[x[0]], self.top))

    def top_index(self, limit):
        return list(map(lambda x:x[0], self.top))[:limit]

def main():
    pass















if __name__ == '__main__':
    main()
