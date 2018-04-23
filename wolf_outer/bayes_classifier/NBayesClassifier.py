#coding: utf-8
import os
import time
import random
import snownlp
from sklearn.naive_bayes import MultinomialNB

def MakeWordsSet(words_file):
    words_set = set()
    with open(words_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            word = line.strip('\r\n ')
            if word and word not in words_set:
                words_set.add(word)
    return words_set

def TextProcessing(file_path, test_size=0.2):
    data_list = []
    class_list = []
    with open(file_path, encoding='utf-8') as fp:
        tag_flag = None
        for line in fp.readlines():
            line = line.strip('\r\n ')
            if line:
                if line.startswith('tag-'):
                    tag_flag = line
                else:
                    if tag_flag:
                        find_index = line.find('?——?')
                        if find_index != -1:
                            line = line[:find_index]
                            snow = snownlp.SnowNLP(line)
                            word_list = snow.words
                            data_list.append(word_list)
                            class_list.append(tag_flag)

    # 随机取测试机和训练集
    data_class_list = list(zip(data_list, class_list))
    random.shuffle(data_class_list)
    index = int(len(data_class_list)*test_size)+1
    train_list = data_class_list[index:]
    test_list = data_class_list[:index]
    train_data_list, train_class_list = zip(*train_list)
    test_data_list, test_class_list = zip(*test_list)

    # 统计词频
    all_words_dict = {}
    for word_list in train_data_list:
        for word in word_list:
            all_words_dict[word] = all_words_dict.get(word, 1) + 1

    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f:f[1], reverse=True)
    all_words_list = list(list(zip(*all_words_tuple_list))[0])

    return all_words_list, train_data_list, test_data_list, train_class_list, test_class_list

def words_dict(all_words_list, deleteN, stopwords_set=set()):
    feature_words = []
    n = 1
    for t in range(0, len(all_words_list), 1):
        if n > 1000: # feature_words的维度1000
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


def TextClassifier(train_feature_list, test_data_list, test_feature_list, train_class_list, test_class_list, result_file=None):
    # sklearn分类器
    classifier = MultinomialNB().fit(train_feature_list, train_class_list)
    predicts = classifier.predict(test_feature_list)
    if result_file:
        with open(result_file, 'wb') as fp:
            res = zip(test_data_list,test_class_list,test_feature_list,predicts)
            for item in res:
                fp.write(('test data： {0}\n'.format(item[0])).encode('utf-8'))
                fp.write(('feature： {0}\n'.format(item[2])).encode('utf-8'))
                fp.write(('test class： {0}\n'.format(item[1])).encode('utf-8'))
                fp.write(('predict： {0}\n\n'.format(item[3])).encode('utf-8'))
    test_accuracy = classifier.score(test_feature_list, test_class_list)
    return test_accuracy


if __name__ == '__main__':
    print('start bayes classifier')
    # 读取数据
    file_path = 'poems.txt'
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
    all_words_list, train_data_list, test_data_list, train_class_list, test_class_list = TextProcessing(file_path, test_size=0.2)

    # 生成stopwords_set
    stop_file_path = 'stopwords.txt'
    stop_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), stop_file_path)
    stopwords_set = MakeWordsSet(stop_file_path)

    # 文本特征提取和分类
    result_file = 'poems_results.txt'
    result_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), result_file)
    deleteNs = range(0, len(all_words_list), 20)
    test_accuracy_list = []
    for deleteN in deleteNs:
        feature_words = words_dict(all_words_list, deleteN, stopwords_set)
        if feature_words:
            train_feature_list, test_feature_list = TextFeatures(train_data_list, test_data_list, feature_words)
            test_accuracy = TextClassifier(train_feature_list, test_data_list, test_feature_list, train_class_list, test_class_list, result_file=result_file)
            test_accuracy_list.append(test_accuracy)

    print("end bayes classifier")
