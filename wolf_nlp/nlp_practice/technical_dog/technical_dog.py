#coding=utf-8
import os
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

"""
    plt.rcParams
    主要作用是设置画的图的分辨率，大小等信息
    plt.rcParams['figure.figsize'] = (8.0, 4.0) # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest' # 设置 interpolation style
    plt.rcParams['image.cmap'] = 'gray' # 设置 颜色 style
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  #设置字体

    #figsize(12.5, 4) # 设置 figsize
    plt.rcParams['savefig.dpi'] = 300 #图片像素
    plt.rcParams['figure.dpi'] = 300 #分辨率
    # 默认的像素：[6.0,4.0]，分辨率为100，图片尺寸为 600&400
    # 指定dpi=200，图片尺寸为 1200*800
    # 指定dpi=300，图片尺寸为 1800*1200
    # 设置figsize可以在不改变分辨率情况下改变比例
"""


def func1():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', '大话西游.txt')
    segment = []
    with open(file, encoding='utf-8') as fd:
        for line in fd.readlines():
            line = line.strip('\r\n ')
            segs = jieba.cut(line)
            for seg in segs:
                if seg:
                    segment.append(seg)
    words_df = pd.DataFrame({'segment':segment})
    #print(words_df.head())

    #去除停用词
    stop_word_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'stopwords.txt')
    stopwords = pd.read_csv(stop_word_file, index_col=False, quoting=3, sep='\t', names=['stopword'], encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    #统计词频
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({'计数':np.size})
    words_stat = words_stat.reset_index().sort_values(by='计数', ascending=False)
    #print(words_stat.head())

    #词云
    fig = plt.figure(figsize=(10, 5))
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    #设置显示字体大小
    plt.rcParams['font.size'] = 15
    ttf_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'msyh.ttf')
    wordcloud = WordCloud(background_color='black', font_path=ttf_file, scale=10)
    #wordcloud = wordcloud.fit_words(words_stat.head(1000).itertuples(index=False))
    print( words_stat.head(5).values)
    #这里需要一个字典
    wordcloud = wordcloud.fit_words({x[0]:x[1] for x in words_stat.head(1000).values})
    plt.imshow(wordcloud)
    #plt.show()

    #自定义图形显示
    from scipy.misc import imread
    fig = plt.figure(figsize=(20,10))
    plt.rcParams['font.size'] = 20
    img_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', 'heart.jpeg')
    bimg = imread(img_file)
    wordcloud = WordCloud(font_path=ttf_file, background_color='black', mask=bimg, scale=10)
    wordcloud = wordcloud.fit_words({x[0]:x[1] for x in words_stat.head(4000).values})
    bimgColor = ImageColorGenerator(bimg)
    plt.axis('off')
    plt.imshow(wordcloud.recolor(color_func=bimgColor))
    plt.show()


if __name__ == '__main__':
    func1()
