import os
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from pylab import mpl
from sklearn.linear_model import LinearRegression

# 图中显示乱码
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 保存词的变量
all_words_dict = {}
show_words_max = 10

# 保存出版社的变量
all_publisher_dict = {}
show_publisher_max = 5
all_publisher_score_dict = {}
all_publisher_score_max = 5
all_publisher_score_average_max = 5
all_publisher_price_dict = {}

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

stopwords = set()

def main():
    stop_words_file_name = 'stopword.txt'
    if os.path.exists(stop_words_file_name):
        with open(stop_words_file_name, 'rb') as f:
            for line in f.readlines():
                line = line.decode('utf-8').strip('\r\n ')
                stopwords.add(line)
    pd_data = pd.read_csv('dangdang.csv', header=None,)
    for row in pd_data.values:
        row = list(row)
        res = jieba.cut(row[0].strip('\r\n '))
        for word in res:
            word = word.strip('\r\n ')
            if word in pointwords or not word or word in stopwords:
                continue
            all_words_dict[word] = all_words_dict.get(word, 0) + 1

        publisher = row[2].strip('\r\n ')
        if publisher and publisher != 'NAN':
            all_publisher_dict[publisher] = all_publisher_dict.get(publisher, 0) + 1
            all_publisher_score_dict[publisher] = all_publisher_score_dict.get(publisher, 0.0) + float(row[-1])
            all_publisher_price_dict[publisher] = all_publisher_price_dict.get(publisher, 0.0) + float(row[1].strip('\r\n ')[1:])
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

    sd = sorted(all_publisher_score_dict.items(), key=lambda x:x[1], reverse=True)
    print(sd)
    sd = sd[:all_publisher_score_max]
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title('出版社总分分布图')
    plt.savefig('出版社总分分布图.png')
    plt.show()

    average_publisher_socre_dict = {}
    for k,v in all_publisher_score_dict.items():
        average_publisher_socre_dict[k] = round(v / all_publisher_dict[k], 2)
    sd = sorted(average_publisher_socre_dict.items(), key=lambda x:x[1], reverse=True)
    print(sd)
    sd = sd[:all_publisher_score_average_max]
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title('出版社平均分分布图')
    plt.savefig('出版社平均分分布图.png')
    plt.show()

    # 先行回归得出评分和价格的关系
    price_score_tupe = []
    x = []
    y = []
    for k,v in all_publisher_price_dict.items():
        x.append([v])
        y.append(average_publisher_socre_dict[k])
        price_score_tupe.append((v, average_publisher_socre_dict[k]))
    model = LinearRegression()
    model.fit(x, y)
    print(model.coef_)

    # 出版社与价格的分布图 分数倒序
    sd = sorted(price_score_tupe, key=lambda x:x[1], reverse=True)
    print(sd)
    sd = sd[:all_publisher_score_average_max]
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title('出版社与价格的分布图')
    plt.savefig('出版社与价格的分布图.png')
    plt.show()


main()












