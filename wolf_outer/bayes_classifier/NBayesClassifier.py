#coding: utf-8
import os
import time
import random
import snownlp
from sklearn.naive_bayes import MultinomialNB
from matplotlib import pyplot as plt
from pylab import mpl
from collections import Counter

#去除标点符号
pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃']
pt = set(pointwords)
pointWordsFilter = lambda s: ''.join(filter(lambda x: x not in pt, s))

def MakeWordsSet(words_file):
    words_set = set()
    with open(words_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            word = line.strip('\r\n ')
            if word and word not in words_set:
                words_set.add(word)
    return words_set

def TextPro(file_path):
    test_data_list = []
    test_sentiments_list = []
    handle_count = 0
    with open(file_path, encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\r\n ')
            find_index = line.find('?——?')
            if find_index == -1:
                find_index = line.find('——')
            if find_index != -1:
                line = line[:find_index]
                line = pointWordsFilter(line)
                try:
                    snow = snownlp.SnowNLP(line)
                    test_data_list.append(snow.words)
                    test_sentiments_list.append(snow.sentiments)
                    handle_count += 1
                except Exception as e:
                    #print('except {0} -- line {1}'.format(e, line))
                    pass
            if handle_count%10000 == 0:
                print('have done {0}'.format(handle_count))
        return test_data_list, test_sentiments_list

def TextProcessing(file_path, test_size=0.2):
    data_list = []
    class_list = []
    sentiments_list = []
    with open(file_path, 'r', encoding='utf-8') as fp:
        tag_flag = None
        for line in fp.readlines():
            line = line.strip('\r\n ')
            if line:
                if line.startswith('tag-'):
                    tag_flag = line
                else:
                    if tag_flag:
                        find_index = line.find('?——?')
                        if find_index == -1:
                            find_index = line.find('——')
                        if find_index != -1:
                            line = line[:find_index]
                            line = pointWordsFilter(line)
                            snow = snownlp.SnowNLP(line)
                            word_list = snow.words
                            data_list.append(word_list)
                            class_list.append(tag_flag)
                            sentiments_list.append(snow.sentiments)

    # 随机取测试机和训练集
    data_class_list = list(zip(data_list, class_list, sentiments_list))
    random.shuffle(data_class_list)
    index = int(len(data_class_list)*test_size)+1
    train_list = data_class_list[index:]
    test_list = data_class_list[:index]
    train_data_list, train_class_list, train_sentiments_list = zip(*train_list)
    test_data_list, test_class_list, test_sentiments_list = zip(*test_list)

    # 统计词频
    all_words_dict = {}
    for word_list in train_data_list:
        for word in word_list:
            all_words_dict[word] = all_words_dict.get(word, 1) + 1

    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f:f[1], reverse=True)
    all_words_list = list(list(zip(*all_words_tuple_list))[0])

    return all_words_list, train_data_list, test_data_list, train_class_list, test_class_list, test_sentiments_list

def WordsDict(all_words_list, stopwords_set=set()):
    feature_words = []
    n = 1
    for t in range(0, len(all_words_list), 1):
        if n > 1000:
            break
        if not all_words_list[t].isdigit() and all_words_list[t] not in stopwords_set and 1<len(all_words_list[t])<5:
            feature_words.append(all_words_list[t])
            n += 1
    return feature_words


def TextFeatures(train_data_list, test_data_list, feature_words):
    def text_features(text, feature_words):
        text_words = set(text)
        # sklearn特征 list
        features = [1 if word in text_words else 0 for word in feature_words]
        return features
    train_feature_list = [text_features(text, feature_words) for text in train_data_list]
    test_feature_list = [text_features(text, feature_words) for text in test_data_list]
    return train_feature_list, test_feature_list

def SplitSentiment(sent):
    flag_sent = 0.0
    if sent > 0.5:
        if sent > 0.4 and sent <= 0.6:
            flag_sent = 0.6
        elif sent > 0.6 and sent <= 0.8:
            flag_sent = 0.8
        else:
            flag_sent = 1.0
    elif sent < 0.5:
        if sent > 0.4 and sent <= 0.6:
            flag_sent = 0.6
        elif sent > 0.2 and sent <= 0.4:
            flag_sent = 0.4
        else:
            flag_sent = 0.2
    return flag_sent

def TextTrain(train_feature_list, train_class_list):
    classifier = MultinomialNB()
    classifier.fit(train_feature_list, train_class_list)
    return classifier

def TextClassifier(classifier, test_data_list, test_feature_list, test_class_list, test_sentiments_list, predict_prob=None, result_file=None):
    # sklearn分类器
    predicts = classifier.predict(test_feature_list)
    predicts_prob = classifier.predict_proba(test_feature_list)
    test_class_results = {}
    test_sentiments_results = {}
    if result_file:
        with open(result_file, 'wb') as fp:
            res = zip(test_data_list,test_class_list,test_feature_list,predicts,test_sentiments_list,predicts_prob)
            for item in res:
                #if predict_prob and max(item[5]) > predict_prob:
                if predict_prob and item[5][1] > predict_prob:
                    fp.write(('test data： {0}\n'.format(item[0])).encode('utf-8'))
                    #fp.write(('feature： {0}\n'.format(item[2])).encode('utf-8'))
                    fp.write(('sentiment {0}\n'.format(item[4])).encode('utf-8'))
                    fp.write(('test class： {0}\n'.format(item[1])).encode('utf-8'))
                    fp.write(('predict： {0}\n'.format(item[3])).encode('utf-8'))
                    fp.write(('predict prob :{0}\n\n'.format(item[5])).encode('utf-8'))
                    test_class_results[item[3]] = test_class_results.get(item[3], 0) + 1
                    s_split = SplitSentiment(item[4])
                    test_sentiments_results[s_split] = test_sentiments_results.get(s_split, 0) + 1
            for k,v in test_class_results.items():
                fp.write(('{0} {1}'.format(k,v)).encode('utf-8'))
    return test_class_results,test_sentiments_results

def show(test_sentiments_results, test_class_results):
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    sd = sorted(test_sentiments_results.items(), key=lambda x:x[0])
    plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb',tick_label=[i[0] for i in sd])
    plt.title(u'唐诗宋词情感分布图')
    plt.savefig('{0}.{1}'.format(result_file, 'sentiments.jpg'))
    plt.show()

    print('test_class_results ', test_class_results)
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    tick_l = test_class_results.keys()
    tick_l = [i.replace('tag-', '') for i in tick_l if i]
    print('tick_l ', tick_l)
    plt.bar(range(len(test_class_results)), test_class_results.values(), color='rgb', tick_label=tick_l)
    plt.title(u'唐诗宋词建筑分类分布图')
    plt.savefig('{0}.{1}'.format(result_file, 'classes.jpg'))
    plt.show()


if __name__ == '__main__':
    print('start bayes classifier')
    # 读取训练数据 每一个类别前面加上 tag- 前缀
    file_path = 'poems.txt'
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
    all_words_list, train_data_list, test_data_list, train_class_list, test_class_list, test_sentiments_list = TextProcessing(file_path, test_size=0.1)

    #测试数据
    file_path = 'poems_test.txt'
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
    if os.path.exists(file_path):
        t_test_data_list, t_test_sentiments_list = TextPro(file_path)
        if len(t_test_data_list) > 0 and len(t_test_sentiments_list) > 0:
            test_data_list = t_test_data_list[:]
            test_class_list = [0.0 for _ in range(len(t_test_data_list))]
            test_sentiments_list = t_test_sentiments_list[:]

    # 生成stopwords_set
    stop_file_path = 'stopwords.txt'
    stop_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), stop_file_path)
    stopwords_set = MakeWordsSet(stop_file_path)

    # 文本特征提取和分类
    result_file = 'poems_results.txt'
    # 分类概率值  如果低于这个值那么分类为其他类
    predict_prob = 0.1
    result_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), result_file)
    feature_words = WordsDict(all_words_list, stopwords_set)
    test_class_results_all = {}
    test_sentiments_results_all = {}

    if feature_words:
        train_feature_list, test_feature_list = TextFeatures(train_data_list, test_data_list, feature_words)
        range_big = len(test_data_list)
        num_per = 10000
        range_end = int(range_big/num_per)
        classifiers = TextTrain(train_feature_list, train_class_list)
        for i in range(range_end + 1):
            print('classifier {0} ~ {1}'.format(num_per*i, num_per*(i+1)))
            test_data_list_t = []
            test_feature_list_t = []
            test_class_list_t = []
            test_sentiments_list_t = []
            if i == range_end:
                test_data_list_t = test_data_list[num_per*i:]
                test_feature_list_t = test_feature_list[num_per*i:]
                test_class_list_t = test_class_list[num_per*i:]
                test_sentiments_list_t = test_sentiments_list[num_per*i:]
            else:
                test_data_list_t = test_data_list[num_per*i:num_per*(i+1)]
                test_feature_list_t = test_feature_list[num_per*i:num_per*(i+1)]
                test_class_list_t = test_class_list[num_per*i:num_per*(i+1)]
                test_sentiments_list_t = test_sentiments_list[num_per*i:num_per*(i+1)]

            test_class_results_tmp,test_sentiments_results_tmp = TextClassifier(classifiers, test_data_list_t, test_feature_list_t, test_class_list_t, test_sentiments_list_t, predict_prob=predict_prob, result_file=result_file)
            test_class_results_all = dict(Counter(test_class_results_tmp)+Counter(test_class_results_all))
            test_sentiments_results_all = dict(Counter(test_sentiments_results_tmp)+Counter(test_sentiments_results_all))

    show(test_sentiments_results_all,test_class_results_all)

    print("end bayes classifier")
