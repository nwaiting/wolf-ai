#coding=utf-8

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
from sklearn.datasets.base import Bunch
from sklearn.metrics.pairwise import euclidean_distances
import pickle

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
1、分词
2、将词频转化为向量
"""

def calc_tfidf(f_name):
    train_copy = None
    with open(f_name, 'r') as fd:
        train_copy = fd.readlines()
    # 将文本中的词语转换为词频矩阵 a[i][j]表示j词在i类文本下的词频
    count_vector = CountVectorizer()
    tfidf_vector = TfidfVectorizer(max_df=0.95, min_df=2)
    # 统计每个词语的tfidf权值
    tfidf_transformer = TfidfTransformer()
    # tfidf_vector.fit_transform 文本转为词频矩阵
    # tfidf_transformer.fit_transform 计算tf-idf值
    tfidf = tfidf_transformer.fit_transform(tfidf_vector.fit_transform(train_copy))
    #获取词袋模型中的所有词语
    words = tfidf_vector.get_feature_names()
    weights = tfidf.toarray()

def bunchSave():
    from sklearn.metrics import accuracy_score
    x = [0,2,1,3]
    y = [0,1,2,3]
    print accuracy_score(x,y)

def calc_distance():
    corpus = [
    'UNC played Duke in basketball',
    'Duke lost the basketball game',
    'I ate a sandwich'
    ]
    vector = CountVectorizer()
    counts = vector.fit_transform(corpus).todense()
    for x,y in [[0,1],[0,2],[1,2]]:
        dist = euclidean_distances(counts[x], counts[y])
        print 'text {} and text {} distance {}'.format(x,y,dist)

def msum(l):
    if not l:
        return 0
    return l[0] + msum(l[1:])

if __name__ == '__main__':
    #raise Exception("not main")
    #bunchSave()
    ld = [1,2,3,4,5]
    print msum(ld)

    import sys
    sys.exit(0)

    f = None
    try:
        f = open('aaaaaaa.txt','rb')
        f.write('aaaaaaaa')
    except:
        pass
    finally:
        print "finally"

    import StringIO
    s = StringIO.StringIO()
    s.write('hello')
    sa = ['123','456']
    s.write(sa)
    s.writelines(sa)
    s.seek(0)
    print s.read()
