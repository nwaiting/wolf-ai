#coding=utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from gensim.models.word2vec import Word2Vec
from gensim.models.fasttext import FastText
from lxml import etree
import numpy as np
import os
import jieba

pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃','#']
pt = set(pointwords)
pointWordsFilter = lambda s: ''.join(filter(lambda x: x not in pt,s))

def cal_tfidf():
    """
        计算过程中自动去掉了停用词
        TfidfVectorizer就是可以把CountVectorizer、TfidfTransformer合并起来，直接计算tfidf值
        gensim的corpora和models也有类似的功能
    """
    corpus = ["我 来到 北京 清华大学",
                "他 来到 了 网易 杭研 大厦",
                "小明 硕士 毕业 与 中国 科学院",
                "我 爱 北京 天安门"]
    vectorizer = CountVectorizer() #将文本中的词转换为词频矩阵，矩阵a[i][j]表示j词在i类文本下的词频
    vecs = vectorizer.fit_transform(corpus) #计算词频矩阵
    #统计出所有的词频
    print(vectorizer.get_feature_names())
    #['中国', '北京', '大厦', '天安门', '小明', '来到', '杭研', '毕业', '清华大学', '硕士', '科学院', '网易']

    # 可以看到所有文本的关键字和其位置
    print(vectorizer.vocabulary_)
    # {'来到': 5, '北京': 1, '清华大学': 8, '网易': 11, '杭研': 6, '大厦': 2, '小明': 4, '硕士': 9, '毕业': 7, '中国': 0, '科学院': 10, '天安门': 3}

    print(vecs.toarray()) #计算出词袋矩阵
    """
    [[0 1 0 0 0 1 0 0 1 0 0 0]
     [0 0 1 0 0 1 1 0 0 0 0 1]
     [1 0 0 0 1 0 0 1 0 1 1 0]
     [0 1 0 1 0 0 0 0 0 0 0 0]]
    """

    transformer = TfidfTransformer() #统计每个词的tf-idf权值
    tfidf = transformer.fit_transform(vecs) #就是tf-idf

    words = vectorizer.get_feature_names() #获取词袋中的所有词
    weights = tfidf.toarray() #计算出的tf-idf权重
    print(weights)
    """
    [[ 0.          0.52640543  0.          0.          0.          0.52640543       0.          0.          0.66767854  0.          0.          0.        ]
     [ 0.          0.          0.52547275  0.          0.          0.41428875           0.52547275  0.          0.          0.          0.          0.52547275]
     [ 0.4472136   0.          0.          0.          0.4472136   0.          0.       0.4472136   0.          0.4472136   0.4472136   0.        ]
     [ 0.          0.6191303   0.          0.78528828  0.          0.          0.       0.          0.          0.          0.          0.        ]]
    """
    for i in range(len(weights)):
        print('{0} 的tf-idf权值'.format(corpus[i]))
        for j in range(len(words)):
            print(words[j],weights[i][j])


    """
        使用TfidfVectorizer直接计算tfidf值
        max_df,min_df在建立单词表的时候会取df在[max_df,min_df]区间内的单词，使用整数时，表示单词的频次，浮点数表示频率
        ngram_range: 取ngram的范围
    """
    X_test = ["我 来到 网易 公司"]
    vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
    # 用train_corpus数据来fit
    vectorizer.fit(corpus)
    # 得到tfidf矩阵
    tfidf_train = vectorizer.transform(corpus)
    tfidf_test = vectorizer.transform(X_test)
    print('get train tfidf：')
    print(tfidf_train.toarray())
    print('get test tfidf：')
    print(tfidf_test.toarray())


class TextClassify(object):
    def __init__(self):
        pass




class TextCluster(object):
    """
        对短文进行分类
    """
    def __init__(self, file):
        self.file_name = file
        self.sentiment_contents_all = []
        self.word_vec_size = 100
    def cluster(self):
        xml_file = etree.parse(self.file_name)
        root_node = xml_file.getroot()
        contents_num = 0
        for sents in root_node:
            for sent in sents:
                if sent.get('polarity'):
                    contents_num += 1
                    cuts = jieba.cut(sent.text, cut_all=True)
                    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
                    self.sentiment_contents_all.append(cuts_contents)
        print('contents number ', contents_num)

        model = Word2Vec(size=self.word_vec_size, min_count=5)
        model.build_vocab(self.sentiment_contents_all)
        model.train(self.sentiment_contents_all,total_examples=model.corpus_count,epochs=model.iter)

        train_features = []
        for ite in self.sentiment_contents_all:
            word_arr = np.zeros(self.word_vec_size)
            for word in ite:
                try:
                    word_arr += np.array(model[word])
                except:
                    pass
            train_features.append(word_arr/len(ite))

        k_means = KMeans(n_clusters=5, n_jobs=4)
        k_pre = k_means.fit_predict(train_features)
        #print(k_pre)
        #2个中心
        #print(k_means.cluster_centers_)
        #每个样本所属的簇
        #print(k_means.labels_)
        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        #print(k_means.inertia_)
        for k,v in zip(self.sentiment_contents_all,k_pre):
            print('{0} - {1}'.format(k,v))
        print(k_means.inertia_)

    def cluster_fasttext(self):
        xml_file = etree.parse(self.file_name)
        root_node = xml_file.getroot()
        contents_num = 0
        for sents in root_node:
            for sent in sents:
                if sent.get('polarity'):
                    contents_num += 1
                    cuts = jieba.cut(sent.text, cut_all=True)
                    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
                    self.sentiment_contents_all.append(cuts_contents)
        print('contents number ', contents_num)

        model = FastText(size=self.word_vec_size, min_count=5)
        # update为true时，新加的词会加入到原来的模型中
        model.build_vocab(self.sentiment_contents_all, update=True)
        model.train(self.sentiment_contents_all,total_examples=model.corpus_count,epochs=model.iter)

        train_features = []
        for ite in self.sentiment_contents_all:
            word_arr = np.zeros(self.word_vec_size)
            for word in ite:
                if word in model.wv.vocab:
                    word_arr += np.array(model[word])
            train_features.append(word_arr/len(ite))

        k_means = KMeans(n_clusters=5, n_jobs=4)
        k_pre = k_means.fit_predict(train_features)
        #print(k_pre)
        #2个中心
        #print(k_means.cluster_centers_)
        #每个样本所属的簇
        #print(k_means.labels_)
        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        #print(k_means.inertia_)
        for k,v in zip(self.sentiment_contents_all,k_pre):
            print('{0} - {1}'.format(k,v))
        print(k_means.inertia_)

if __name__ == '__main__':
    flag = 1
    if flag == 0:
        cal_tfidf()
    elif flag == 1:
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..','sentiment_1','weibodata', 'xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml')
        text_clus = TextCluster(file_name)
        text_clus.cluster()
    elif flag == 2:
        print(np.zeros(10))
        print(np.zeros(10).reshape((1,10)))















#
