#coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
from matplotlib import pyplot as plt
from pylab import mpl
from snownlp import SnowNLP
from wordcloud import WordCloud
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
    pf_data = pd.read_csv(file, header=None, nrows=None, usecols=[5,7])
    pf_data = pf_data.dropna() #删除掉空行
    #print(pf_data.head())
    #print(pf_data[5].head())
    #print(pf_data[7].values)

    #groupby_user = pf_data.groupby([5]).count()
    #groupby_user = pf_data.groupby([5]).size()
    #浏览随时间变化趋势图
    scan_pre = []
    #情感随时间变化趋势图
    sentiments_split_records = {}
    #总的情感分布图
    sentiment_map = {}
    #总的切分后的词
    cut_all_words = []
    cut_all_words_str = ''
    groupby_user = pf_data.groupby([5])

    for k,v in groupby_user:
        if k.find(':') != -1:
            k = k.split(':')[0]
        scan_pre.append((k, v.count()[7]))

        tmp_sentiment_records = [0,0]
        for lines in v[7].values:
            if len(lines) > 0:
                line = lines.strip('\r\n\t ')
                line = re.sub(r'[0-9]', '', line)
                line = pointWordsFilter(line)
                if line:
                    snlp = SnowNLP(line)
                    tmp_cut_words = ' '.join(snlp.words)
                    cut_all_words_str += tmp_cut_words
                    cut_all_words.append(tmp_cut_words)
                    if snlp.sentiments >= pos_prob:
                        sentiment_map['pos'] = sentiment_map.get('pos', 0) + 1
                        tmp_sentiment_records[0] += 1
                    else:
                        sentiment_map['neg'] = sentiment_map.get('neg', 0) + 1
                        tmp_sentiment_records[1] += 1

        sentiments_split_records[k] = tmp_sentiment_records[:]

    countvec = CountVectorizer()
    countvec_fit = countvec.fit_transform(cut_all_words)
    word_with_count = zip(countvec.get_feature_names(), countvec_fit.toarray().sum(axis=0))
    result_word_sort = sorted(word_with_count, key=lambda x:x[1], reverse=True)

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    records_len = len(sentiments_split_records)
    pos_values = [v[0] for v in sentiments_split_records.values()]
    neg_values = [v[1] for v in sentiments_split_records.values()]
    key_values = [k for k in sentiments_split_records.keys()]
    plt.bar(range(records_len), pos_values, color='r', tick_label=key_values, label='积极情绪')
    plt.bar(range(records_len), neg_values, color='b', bottom=pos_values, label='消极情绪')
    plt.legend()
    plt.title('情感随时间变化趋势')
    plt.xlabel('时间')
    plt.ylabel('话题个数')
    plt.savefig('{0}.{1}'.format(file_name, 'sentiment_time.jpg'))
    plt.show()

    records_len = len(scan_pre)
    y_values = [i[1] for i in scan_pre]
    x_values = [i[0] for i in scan_pre]
    plt.bar(range(records_len), y_values, color='b', tick_label=x_values)
    plt.title('关注度随时间变化趋势')
    plt.xlabel('时间')
    plt.ylabel('话题相关数量')
    plt.savefig('{0}.{1}'.format(file_name, 'follows.jpg'))
    plt.show()

    y_values = [i for i in sentiment_map.values()]
    x_values = [i for i in sentiment_map.keys()]
    plt.bar(range(len(sentiment_map)), y_values, color='r', tick_label=x_values)
    plt.title('情感分布图')
    plt.xlabel('情感状态(neg:消极 pos:积极)')
    plt.ylabel('话题个数')
    plt.savefig('{0}.{1}'.format(file_name, 'sentiments.jpg'))
    plt.show()

    y_values = [i[1] for i in result_word_sort[:word_num]]
    x_values = [i[0] for i in result_word_sort[:word_num]]
    plt.bar(range(word_num), y_values, color='rgb', tick_label=x_values, label='词频分布最高的词')
    plt.legend()
    plt.title('词频分布')
    plt.xlabel('个数')
    plt.ylabel('词语')
    plt.savefig('{0}.{1}'.format(file_name, 'words.jpg'))
    plt.show()

    wc = WordCloud(background_color='white',
                    collocations=False,
                    width=2000,
                    height=1400,
                    font_path="C:\\Windows\\Fonts\\msyhbd.ttf",
                    scale=2,
                    max_words=2000)
    wc.fit_words({x[0]:x[1] for x in result_word_sort})

    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file('{0}.{1}'.format(file_name, 'wordcloud.jpg'))

if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "weiboData.csv")
    #情感为正的最低概率
    pos_probability = 0.6
    #显示词频的前10个词
    words_show_num = 10
    sentiment_analysis(file_name, pos_probability, words_show_num)
