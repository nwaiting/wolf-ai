#coding=utf-8

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

#去除标点符号
pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃']
pt = set(pointwords)
pointWordsFilter = lambda s: ''.join(filter(lambda x: x not in pt, s))

def func1():
    #帮助函数
    #文本分类，判断一个词的重要性的指标
    help(TfidfVectorizer)

def func2():
    #TextRank 算法抽取关键词
    #类似搜索引擎的pagerank
    pass

def func3():
    #LDA主题模型
    #文档主题概率分布、主题词语概率分布
    from gensim import corpora,models
    sents = [['作为 赵本山 最疼 爱的 孩子 , 很多 网友 对于 球球 赵一涵 都是 相当 熟悉 的 。 特别 是从 2 年前 开始 , 球球 就 正式 进入 到了 主播 界 , 当 起了 一名 网红 , 现如今 早 已是 拥有 上 百万 粉丝 的 大 主播 , 事业 发展 的 可谓 顺风 顺水'],
                    ['除了 事业 之外 , 她的 感情生活 也是 备受 网友 们 的 期待 , 毕竟 已经 是 大姑娘 了 , 没个 男朋友 貌似 也 说不过去 啊 , 其实 从 2017年 下半 年开始 , 球球 就 和 另外 一个 当红 主播 九局 打的 是 火热'],
                    ['球球 和 九局 不仅 一 起拍 了 很多 时尚 杂志和 宣传 照 , 而且 在 镜 头中 都 是以 绯闻 情侣 的 名义 出现 的 , 出了 公开场合 的 活动 之外 , 私底下 两个 人的 交流 也是 颇多 , 比如 会相 约去 打 篮球 什么 的 , 当时 很多 人都 觉得 , 他们 俩 以后 肯 定会 发展 成为 真实 的 情侣 关系'],
                    ['但是 让人 没想到 的 是 , 就在 昨天 晚上 的 直播 中 , 球球 居然 大方 的 公 开了 自己的 男友 , 他 之前 曾经 给 球球 刷过 很 多的 礼物 , 登上 过球 球 的 土豪 榜 , 一来 二 去就 这么 认识 了'],
                    ['当然 直播 的 内容 主 要是 为了 宣传 她自己 刚发 行的 新歌 , 但 是在 直播 过程中 , 球球 也是 谈到 , 自己 明白 自身 的 优缺点 , 但是 这个 男人 会 包容 他的 任性 , 也 希望 能做 她的 白马王子'],
                    ['只不过 实话 实话 , 要说 这位 男友 对 球球 是 一往情深 , 大家 也 没什么 话说 , 但是 要说 他是 白马王子 估计 就 应该 去 看看 眼科 了吧 。 就 算是 开了 美颜 , 上了 滤镜 , 这位 兄弟 长得 都 只能 说是 一般']]
    #创建字典
    sentiments = []
    for item in sents:
        sentiments.append([i for i in item[0].strip().split() if pointWordsFilter(i)])

    dictionary = corpora.Dictionary(sentiments)
    #
    corpus = [dictionary.doc2bow(sentence) for sentence in sentiments]
    #设置主题的分类 num_topics
    lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=2, id2word=dictionary)
    #打印某一个分类
    print(lda.print_topic(1, topn=10))
    print('----------------------')

    #打印排名在前面的分类
    print(lda.print_topics(num_topics=5, num_words=10))

def func4():
    #bayes 朴素贝叶斯分类
    #数据足够，效果不错
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB,GaussianNB,BernoulliNB,BaseDiscreteNB
    #analyzer设置最小分割为词粒度
    vec = CountVectorizer(analyzer='word', max_features=1000)
    #vec.fit(raw_documents) #构造词向量
    #vec.transform(words) #获取词向量

    #vec.fit_transform() #一步解决
    print(help(CountVectorizer))

    classifier = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    classifier.fit(vec.fit_transform(x_train), y_train)

    #查看准确率
    classifier.score(vec.fit_transform(x_test), y_test)

    #！！！！！！！！！！！！！！！！优化！！！！！！！！
    #！！！！！！！！！！！！！！！！优化！！！！！！！！
    #！！！！！！！！！！！！！！！！优化！！！！！！！！
    # 1、ngram_range=(1, 3) 范围为[1,3)
    # 2、更高的词频
    CountVectorizer(analyzer='word', ngram_range=(1, 3), max_features=2000)

    #交叉验证
    # K折交叉验证 当有多分类时需要分层抽样
    from sklearn.cross_validation import StratifiedKFold
    #from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import accuracy_score, precision_score
    import random
    stratifiedk_fold = StratifiedKFold(y, n_folds=5, shuffle=random.shuffle)
    for train_index,test_index in stratifiedk_fold:
        x_train,x_test = x[train_index], x[test_index]
        y_train = y[train_index]
        classifier.fit(x_train,y_train)
        y_pred[test_index] = classifier.predict(x_test)

def func5():
    from sklearn.svm import SVC
    #rbf的kernel非常慢
    svm = SVC(kernel='linear')
    svm.fit()
    svm.socre()

class TextClassifier(object):
    def __init__(self, classifier=None):
        """
            分类器可以自由选择
            特征构造也可以自由选择，比如CountVectorizer或者TfidfVectorizer
        """
        if not classifier:
            self.classifier = MultinomialNB()
        else:
            self.classifier = classifier


if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    func5()
