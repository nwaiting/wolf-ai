#coding=utf-8

import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
from wordcloud import WordCloud,STOPWORDS, ImageColorGenerator
from scipy.misc import imread

def func1():
    rd = pd.read_csv()
    rd = rd.dropna() #删除空行
    rd.content.values.tolist()

    stopwords = pd.read_csv('stopwords.csv')
    stopword = stopwords['stopword'].values

    #设置背景图片
    bimsg = imread('image/entertainment.jpeg')

    wc = WordCloud(background_color='white',
                    stopwords=stopwords,
                    collocations=False,
                    width=1800,
                    height=1400,
                    font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",
                    scale=2,
                    mask=bimsg,
                    max_words=2000).generate(text=text)
    #图像颜色生成器 生成背景
    bimagColors = ImageColorGenerator(bimsg)
    plt.imshow(wc.recolor(color_func=bimagColors))



if __name__ == '__main__':
    func1()
