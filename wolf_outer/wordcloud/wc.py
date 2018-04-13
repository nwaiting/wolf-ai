#coding=utf8

from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
from matplotlib import font_manager
from pylab import mpl
from scipy.misc import imread
from snownlp import SnowNLP
import os
import json

"""
颜色柱状图
配置柱状图
销售数量和评论数据和时间关系
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


def emotionAnalysis(e_value_l, e_value_r, r_file, s_file, file_pic, file_stop=None, show_size=5):
    """
        根据情绪值范围过滤 句子
    """
    color_dict = {}
    size_dict = {}
    time_dict = {}
    text = ""

    with open(s_file, 'r', encoding='utf8') as fp:
        for line in fp.readlines():
            json_str = None
            try:
                json_str = json.loads(line.strip('\r\n '))
            except Exception as e:
                print('json error {0}'.format(e))
                continue

            color_dict[json_str['productColor']] = color_dict.get(json_str['productColor'], 0) + 1
            size_dict[json_str['productSize']] = size_dict.get(json_str['productSize'], 0) + 1
            jtime = json_str['referenceTime'].strip().split()
            if len(jtime) == 2:
                jtime = jtime[0]
                rfind_index = jtime.rfind('-')
                if rfind_index != -1:
                    jtime = jtime[:rfind_index]
                    jtime = jtime.replace('-', '')
                    jtime = int(jtime)
                    time_dict[jtime] = time_dict.get(jtime, 0) + 1
            s = SnowNLP(json_str['comments'])
            if s.sentiments >= e_value_l and s.sentiments <= e_value_r:
                text += ' '.join(s.words)

        # 颜色比例柱状图
        color_list = sorted(color_dict.items(), key= lambda x: x[1], reverse=True)[:show_size]
        color_list_first = [i[0] for i in color_list]
        color_list_second = [i[1] for i in color_list]
        mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.bar(range(len(color_list_second)), color_list_second, color='rgb', tick_label=color_list_first)
        plt.savefig('{0}.{1}'.format(file_pic, 'color.jpg'))
        plt.show()

        #配置比例柱状图
        size_list = sorted(size_dict.items(), key=lambda x:x[1], reverse=True)[:show_size]
        size_list_first = [i[0] for i in size_list]
        size_list_second = [i[1] for i in size_list]
        plt.bar(range(len(size_list_second)), size_list_second, color='rgb', tick_label=size_list_first)
        plt.savefig('{0}.{1}'.format(file_pic, 'size.jpg'))
        plt.show()

        #评论和时间关系
        time_list = sorted(time_dict.items(), key=lambda x:x[0])
        time_list_first = [i[0] for i in time_list]
        time_list_second = [i[1] for i in time_list]
        plt.bar(range(len(time_list_second)), time_list_second, color='rgb', tick_label=time_list_first)
        plt.savefig('{0}.{1}'.format(file_pic, 'comments.jpg'))
        plt.show()

        #词图
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

if __name__ == '__main__':
    for item in ('v10','r15','x21','mix2'):
        #情绪值范围
        emotion_value_l = 0.7
        emotion_value_r = 1.0
        file_path_parent = os.path.dirname(os.path.realpath(__file__))
        #过滤后的情绪分词
        result_file_data = os.path.join(file_path_parent, 'high.data')
        result_file_pic = os.path.join(file_path_parent, 'high.{0}.jpg'.format(item))
        #原始数据文件
        source_file = os.path.join(file_path_parent, 'jd.allwords.data.{0}.txt'.format(item))
        #屏蔽词
        stop_words_file = os.path.join(file_path_parent, 'stop_words.data.{0}.txt'.format(item))
        if not os.path.exists(source_file):
            print('error !!!!!!!!!!! {0} not exists'.format(source_file))
        emotionAnalysis(emotion_value_l, emotion_value_r, result_file_data, source_file, result_file_pic, stop_words_file)
        #buildWordCloud(result_file_data, result_file_pic, stop_words_file)
