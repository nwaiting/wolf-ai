#coding=utf8

from wordcloud import WordCloud
from matplotlib import pyplot as plt
from scipy.misc import imread
import os

def main():
    source_file = 'a.txt'
    to_jpg_file = 'a.jpg'
    to_jpg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), to_jpg_file)
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), source_file)

    with open(filename, 'r', encoding='utf8') as fp:
        text = fp.read()
        wc = WordCloud(background_color='white',
                        font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",
                        scale=1.5).generate(text=text)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

        wc.to_file(to_jpg_file)

if __name__ == '__main__':
    main()













# end
