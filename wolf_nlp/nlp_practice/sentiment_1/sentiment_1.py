#coding=utf-8

import os
import jieba
import numpy as np
from lxml import etree
from sklearn.naive_bayes import MultinomialNB
from gensim.models.word2vec import Word2Vec

pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃','#','韩寒','方舟子','方舟','舟子','洗碗','洗碗工']
pt = set(pointwords)
pointWordsFilter = lambda s: ''.join(filter(lambda x: x not in pt,s))

sentiment_words = {}
def func1(file, sent_w):
    '''
        like 1
        good 2
        bad -2
        terrible -3
        类似于基于关键词打分机制
        www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
    '''
    if len(sentiment_words) <= 0:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                res = line.split('\t')
                if len(res) == 2:
                    sentiment_words[res[0]] = int(res[1])

    total_sentiment_score = 0
    for w in sent_w.split():
        total_sentiment_score += sentiment_words.get(w, 0)
    return total_sentiment_score

sentiment_contents = []
sentiment_contents_features = []
sent_value_map = {'NEG':10,'OTHER':20,'POS':30}
sent_words_set = set()
def func2(file, sent_w):
    """
        基于词袋模型的ml训练打分
    """
    if len(sentiment_contents) <= 0:
        xml_file = etree.parse(file)
        root_node = xml_file.getroot()
        contents_num = 0
        for sents in root_node:
            for sent in sents:
                # print(sent.text)
                # NEG(-1) OTHER(0) POS(1)
                if sent.get('polarity'):
                    contents_num += 1
                    cuts = jieba.cut(sent.text, cut_all=True)
                    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
                    for ite in cuts_contents:
                        sent_words_set.add(ite)
                    sentiment_contents.append((sent_value_map[sent.get('polarity')], cuts_contents))
        print('contents number ', contents_num)

    for ite in sentiment_contents:
        sentiment_contents_features.append((ite[0], [1 if it in ite[1] else 0 for it in sent_words_set]))

    classifier = MultinomialNB()
    train_features = []
    train_classes = []
    for ite in sentiment_contents_features:
        train_features.append(ite[1])
        train_classes.append(ite[0])
    print(train_classes)
    classifier.fit(train_features, train_classes)

    cuts = jieba.cut(sent_w, cut_all=True)
    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
    res = classifier.predict([[1 if it in ite[1] else 0 for it in sent_words_set]])
    print(res)

all_split_words = []
word_vec_size = 500
def func3(file, sent_w):
    """
        基于word2vec的ml训练打分
    """
    sentences = []
    xml_file = etree.parse(file)
    root_node = xml_file.getroot()
    contents_num = 0
    for sents in root_node:
        for sent in sents:
            if sent.get('polarity'):
                contents_num += 1
                cuts = jieba.cut(sent.text, cut_all=True)
                cuts_points = pointWordsFilter(' '.join(cuts))
                print('cuts_points ', cuts_points)
                cuts_contents = cuts_points.split()
                sentiment_contents.append((sent_value_map[sent.get('polarity')], cuts_contents))
                all_split_words.append(cuts_contents)
    print('sentences number ', contents_num)

    model = Word2Vec(size=word_vec_size, min_count=1)
    model.build_vocab(all_split_words)
    model.train(all_split_words, total_examples= model.corpus_count, epochs=model.iter)

    train_features = []
    train_classes = []
    for ite in sentiment_contents:
        word_arr = np.zeros(word_vec_size)
        for word in ite[1]:
            #print('model ', model[word])
            word_arr += np.array(model[word])
        #print(word_arr/len(ite[1]))
        train_features.append(word_arr/len(ite[1]))
        train_classes.append([ite[0]])
    classifier = MultinomialNB()
    classifier.fit(train_features, train_classes)

    cuts = jieba.cut(sent_w, cut_all=True)
    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
    word_arr = np.zeros(word_vec_size)
    for w in cuts_contents:
        word_arr += np.array(model[w])
    res = classifier.predict(word_arr/len(cuts_contents))
    print(res)

if __name__ == '__main__':
    """
    file_name= os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AFINN','AFINN-111.txt')
    print(func1(file_name, 'i like it'))
    print(func1(file_name, 'i very love it'))
    print(func1(file_name, 'it\'s so terrible'))
    """

    """
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weibodata', 'xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml')
    func2(file_name, "这个洗碗工是善良的，盼望看到她再次被酒店回聘")
    func2(file_name, "首先洗碗工并没有做错，相反这样的做法是勤俭节约")
    """

    """
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weibodata', 'xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml')
    func3(file_name, '这个洗碗工是善良的，盼望看到她再次被酒店回聘')
    """
    s = ['hello',',','word','方舟子']
    print(pointWordsFilter(' '.join(s)))
