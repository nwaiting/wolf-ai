#coding=utf-8

import os
import jieba
import numpy as np
from lxml import etree
from sklearn.naive_bayes import MultinomialNB,GaussianNB
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.word2vec import Word2Vec

pointwords = ['，', '、', '[', ']', '（', '）', '：',
    '、', '。', '@', '’', '%', '《', '》', '“', '”', '.', '；',
    '′', '°', '″', '-', ',', '！', '？','～', '\'', '\"', ':',
    '(', ')', '【', '】', '~', '/', ';', '→', '\\', '·', '℃','#']
pt = set(pointwords)
pointWordsFilter = lambda s: ''.join(filter(lambda x: x not in pt,s))

stop_words = ['方舟子','舟子','方舟','韩寒','洗碗','洗碗工','韩','寒','之','争','留','剩菜','被','开除']
stop_words = []
sw = set(stop_words)
stopWordsFilter = lambda s:filter(lambda x:x not in sw,s)

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
sent_value_map = {'NEG':-1,'OTHER':0,'POS':1}
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
    #print(train_classes)
    classifier.fit(train_features, train_classes)

    cuts = jieba.cut(sent_w, cut_all=True)
    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
    res = classifier.predict([[1 if it in ite[1] else 0 for it in sent_words_set]])
    print(res)

sentiment_contents_all = []
sentiment_classes_all = []
def func4():
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
                    sentiment_contents_all.append(cuts_contents)
                    sentiment_classes_all.append([sent_value_map[sent.get('polarity')]])
        print('contents number ', contents_num)

    vectorizer = TfidfVectorizer()
    vectorizer.fit(sentiment_contents_all)
    train_features = vectorizer.transform(sentiment_contents_all)

    classifier = MultinomialNB()
    #print(train_classes)
    classifier.fit(train_features, sentiment_classes_all)

    cuts = jieba.cut(sent_w, cut_all=True)
    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
    res = classifier.predict([[1 if it in ite[1] else 0 for it in sent_words_set]])
    print(res)

all_split_words = []
word_vec_size = 300
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
                #print(sent.get('polarity'))
                contents_num += 1
                cuts = jieba.cut(sent.text, cut_all=True)
                res_cuts = stopWordsFilter(cuts)
                cuts_points = pointWordsFilter(' '.join(res_cuts))
                #print('cuts_points ', cuts_points)
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
    #classifier = MultinomialNB()
    classifier = GaussianNB()
    #data_pca = PCA(n_components=2).fit_transform(train_features)
    #data_pca = TSNE(n_components=128).fit_transform(train_features)
    classifier.fit(train_features, train_classes)

    cuts = jieba.cut(sent_w, cut_all=True)
    cuts_contents = pointWordsFilter(' '.join(cuts)).split()
    word_arr = np.zeros(word_vec_size)
    for w in cuts_contents:
        try:
            word_arr += np.array(model[w])
        except:
            pass
    res = classifier.predict([word_arr/len(cuts_contents)])
    print(res)

if __name__ == '__main__':
    flag = 3
    if flag == 0:
        file_name= os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AFINN','AFINN-111.txt')
        print(func1(file_name, 'i like it'))
        print(func1(file_name, 'i very love it'))
        print(func1(file_name, 'it\'s so terrible'))
    elif flag == 1:
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weibodata', 'xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml')
        ss = ["这个洗碗工是善良的，盼望看到她再次被酒店回聘",
                "首先洗碗工并没有做错，相反这样的做法是勤俭节约",
                "洗碗工留剩菜被开除#悲哀.社会的悲哀.也反映出了很严重的社会现实.首先是贫富差距太大"]
        for s in ss:
            print('predict ', s)
            func2(file_name, s)
    elif flag == 2:
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weibodata', 'xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml')
        ss = ['这个洗碗工是善良的，盼望看到她再次被酒店回聘',
                "洗碗工留剩菜被开除#悲哀.社会的悲哀.也反映出了很严重的社会现实.首先是贫富差距太大",
                "洗碗工留剩菜被开除#这酒店太没人情味了",
                "首先洗碗工并没有做错，相反这样的做法是勤俭节约",
                "洗碗工留剩菜被开除#对混乱不堪的中国，就别报以任何希望了",
                "酒店需要制度维持，窘迫需要关怀温暖",
                "韩寒方舟子之争#从某种程度上来说，方舟子已经天下无敌了——人不要脸，天下无敌！"]
        for s in ss:
            print('predict ', s)
            func3(file_name, s)
    elif flag == 3:
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weibodata', 'xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml')
        ss = ["这个洗碗工是善良的，盼望看到她再次被酒店回聘",
                "首先洗碗工并没有做错，相反这样的做法是勤俭节约",
                "洗碗工留剩菜被开除#悲哀.社会的悲哀.也反映出了很严重的社会现实.首先是贫富差距太大",
                "洗碗工留剩菜被开除#这位母亲很伟大，酒店不应该",
                "奋斗洗碗工人做的对，全国人民要支持她"]
        for s in ss:
            print('predict ', s)
            func3(file_name, s)
    elif flag == 4:
        s = ['hello',',','word','方舟子']
        ss = stopWordsFilter(s)
        res = list(ss)
        print(res)
        print(' '.join(res))
        print(pointWordsFilter(' '.join(res)))
















#
