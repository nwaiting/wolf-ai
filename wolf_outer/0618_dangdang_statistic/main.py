import pandas as pd
import matplotlib.pyplot as plt
import jieba
from pylab import mpl

# 图中显示乱码
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 保存词的变量
all_words_dict = {}
show_words_max = 10

# 保存出版社的变量
all_publisher_dict = {}
show_publisher_max = 15

# 保存作者的变量
all_author_dict = {}
show_author_max = 15


author_stop_words = {"译", "出品", "著", "绘", "策划", "等", "图", '', '.', '的', '未读', '博士', '等编绘',
                     '编', '编著', '等译', '[英]', '等著', '文', '(美)', '[日]', '(日)', ';'}
#去除标点符号
pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃']


def main():
    pd_data = pd.read_csv('dangdang.csv', header=None,)
    for row in pd_data.values:
        row = list(row)
        res = jieba.cut(row[0].strip('\r\n '))
        for word in res:
            if word in pointwords or not word:
                continue
            all_words_dict[word] = all_words_dict.get(word, 0) + 1

        publisher = row[2].strip('\r\n ')
        if publisher and publisher != 'NAN':
            all_publisher_dict[publisher] = all_publisher_dict.get(publisher, 0) + 1
        authors_items = row[3].strip('\r\n ').split(',')
        for author in authors_items:
            author = author.strip('\r\n ').split()
            for i in range(len(author)):
                add_author = author[i].strip('\r\n , ')
                if add_author in author_stop_words:
                    continue
                if add_author.find(',') != -1:
                    for inner_item in add_author.split(','):
                        inner_item = inner_item.strip('\r\n ')
                        if inner_item in author_stop_words:
                            continue
                        all_author_dict[inner_item] = all_author_dict.get(inner_item, 0) + 1
                elif add_author.find('，') != -1:
                    for inner_item in add_author.split('，'):
                        inner_item = inner_item.strip('\r\n ')
                        if inner_item in author_stop_words:
                            continue
                        all_author_dict[inner_item] = all_author_dict.get(inner_item, 0) + 1
                else:
                    all_author_dict[add_author] = all_author_dict.get(add_author, 0) + 1

    sd = sorted(all_publisher_dict.items(), key=lambda x:x[1], reverse=True)
    print(sd)
    sd = sd[:show_publisher_max]
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title('出版社分布图')
    plt.savefig('出版社分布图.png')
    plt.show()

    sd = sorted(all_author_dict.items(), key=lambda x:x[1], reverse=True)
    print(sd)
    sd = sd[:show_author_max]
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title('作者分布图')
    plt.savefig('作者分布图.png')
    plt.show()

    sd = sorted(all_words_dict.items(), key=lambda x:x[1], reverse=True)
    print(sd)
    sd = sd[:show_words_max]
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title('词频分布图')
    plt.savefig('词频分布图.png')
    plt.show()


main()













