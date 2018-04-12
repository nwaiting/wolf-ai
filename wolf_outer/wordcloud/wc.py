#coding=utf8

from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
from scipy.misc import imread
from snownlp import SnowNLP
import os

"""
生成词图
"""

def buildWordCloud(file_data, file_pic, file_stop=None):
    with open(file_data, 'r', encoding='utf8') as fp:
        text = fp.read()
        stopwords = None
        if file_stop:
            stopwords = STOPWORDS.copy()
            with open(file_stop, 'r', encoding='utf8') as sfp:
                for i in sfp.readlines():
                    stopwords.add(i.strip('\r\n '))
        wc = WordCloud(background_color='white',
                        stopwords=stopwords,
                        collocations=False,
                        width=1800,
                        height=1400,
                        font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",
                        scale=2,
                        max_words=2000).generate(text=text)

        plt.imshow(wc)
        plt.axis('off')
        plt.show()
        wc.to_file(file_pic)


def emotionAnalysis(e_value_l, e_value_r, r_file, s_file):
    """
        根据情绪值范围过滤 句子
    """
    with open(r_file, 'w', encoding='utf8') as rfp:
        with open(s_file, 'r', encoding='utf8') as fp:
            for line in fp.readlines():
                s = SnowNLP(line)
                if s.sentiments >= e_value_l and s.sentiments <= e_value_r:

                    rfp.write(' '.join(s.words))


if __name__ == '__main__':
    #情绪值范围
    emotion_value_l = 0.8
    emotion_value_r = 1.0
    file_path_parent = os.path.dirname(os.path.realpath(__file__))
    #过滤后的情绪分词
    result_file_data = os.path.join(file_path_parent, 'high.data')
    result_file_pic = os.path.join(file_path_parent, 'high.jpg')
    #原始数据文件
    source_file = os.path.join(file_path_parent, 'jd.allwords.data')
    #屏蔽词
    stop_words_file = os.path.join(file_path_parent, 'stop_words.data')
    if not os.path.exists(source_file):
        print('error !!!!!!!!!!! {0} not exists'.format(source_file))
    #emotionAnalysis(emotion_value_l, emotion_value_r, result_file_data, source_file)
    buildWordCloud(result_file_data, result_file_pic, stop_words_file)













# end
