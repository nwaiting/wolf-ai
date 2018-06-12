#coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
from matplotlib import pyplot as plt
from pylab import mpl
from snownlp import SnowNLP
import pandas as pd
import os
import re

pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃','?','|','$','#']
pt = set(pointwords)
pointWordsFilter = lambda s: ''.join(filter(lambda x: x not in pt, s))

def sentiment_analysis(file, pos_prob, word_num):
    dr = pd.read_csv(file, header=None, nrows=None, usecols=[7])
    dr = dr.dropna() #删除掉空行
    sentiment_map = {}
    cut_all_words = []
    for lines in dr.values:
        if len(lines) > 0:
            line = lines[0].strip('\r\n\t ')
            line = re.sub(r'[0-9]', '', line)
            line = pointWordsFilter(line)
            snlp = SnowNLP(line)
            cut_all_words.append(' '.join(snlp.words))
            if snlp.sentiments >= pos_prob:
                sentiment_map['pos'] = sentiment_map.get('pos', 0) + 1
            else:
                sentiment_map['neg'] = sentiment_map.get('neg', 0) + 1

    countvec = CountVectorizer()
    countvec_fit = countvec.fit_transform(cut_all_words)
    word_with_count = zip(countvec.get_feature_names(), countvec_fit.toarray().sum(axis=0))
    result_word_sort = sorted(word_with_count, key=lambda x:x[1], reverse=True)

    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.bar(range(len(sentiment_map)), [i for i in sentiment_map.values()], color='rgb', tick_label=[i for i in sentiment_map.keys()])
    plt.title('情感分布图')
    plt.savefig('{0}.{1}'.format(file_name, 'sentiments.jpg'))
    plt.show()

    plt.bar(range(word_num), [i[1] for i in result_word_sort[:word_num]], color='rgb', tick_label=[i[0] for i in result_word_sort[:word_num]])
    plt.title('词频分布')
    plt.savefig('{0}.{1}'.format(file_name, 'words.jpg'))
    plt.show()

if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "weiboData.csv")
    #情感为正的最低概率
    pos_probability = 0.6
    #显示词频的前10个词
    words_show_num = 10
    sentiment_analysis(file_name, pos_probability, words_show_num)
