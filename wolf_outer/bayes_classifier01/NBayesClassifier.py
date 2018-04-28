#coding=utf-8
import os
import json
import re
import jieba
from sklearn.naive_bayes import MultinomialNB

def genLocalPath(file_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)

def filter_tags(html_str):
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
    re_br=re.compile('<br\s*?/?>')
    re_h=re.compile('</?\w+[^>]*>')
    re_comment=re.compile('<!--[^>]*-->')
    s=re_cdata.sub('',html_str)
    s=re_script.sub('',s)
    s=re_style.sub('',s)
    s=re_br.sub('\n',s)
    s=re_h.sub('',s)
    s=re_comment.sub('',s)
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    return s

def genFeature(train_data_file, train_class_file, test_data_file):
    dict_id_pre = {}
    train_data_list = []
    test_data_list = []
    contents_words = {}
    title_words = {}
    train_data_feature_list = []
    train_data_class_list = []
    test_data_feature_list = []
    test_data_id_list = []

    with open(train_class_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\r\n ')
            if line:
                if line.startswith('id'):
                    continue
                line_arr = line.split(',')
                if len(line_arr) == 2:
                    dict_id_pre[line_arr[0]] = line_arr[1]

    with open(train_data_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\r\n ')
            if line:
                json_str = None
                try:
                    json_str = json.loads(line)
                except Exception as e:
                    print('except {0}'.format(e))
                else:
                    tmp_dict = {}
                    try:
                        tmp_line = filter_tags(json_str['content'])
                        seglist = jieba.cut(tmp_line,cut_all=False)
                        tmp_dict['content'] = list(seglist)
                        for i in tmp_dict['content']:
                            contents_words[i] = contents_words.get(i, 0) + 1
                        tmp_dict['id'] = json_str['id']
                        tmp_dict['title'] = list(jieba.cut(json_str['title'], cut_all=False))
                        for i in tmp_dict['title']:
                            title_words[i] = title_words.get(i, 0) + 1
                        tmp_dict['pre'] = dict_id_pre[tmp_dict['id']]
                    except Exception as e:
                        print('except {0}'.format(e))
                    else:
                        #print('tmp_dict ', tmp_dict)
                        train_data_list.append(tmp_dict)

    with open(test_data_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\r\n ')
            if line:
                json_str = None
                try:
                    json_str = json.loads(line)
                except Exception as e:
                    print('except load json {0}'.format(e))
                else:
                    tmp_dict = {}
                    try:
                        tmp_line = filter_tags(json_str['content'])
                        seglist = jieba.cut(tmp_line,cut_all=False)
                        tmp_dict['content'] = list(seglist)
                        tmp_dict['id'] = json_str['id']
                        tmp_dict['title'] = list(jieba.cut(json_str['title'], cut_all=False))
                    except Exception as e:
                        print('except parse json {0} {1}'.format(e, json_str))
                    else:
                        #print('tmp_dict ', tmp_dict)
                        test_data_list.append(tmp_dict)

    for item in train_data_list:
        feature_arr = []
        feature_arr += [1 if word in item['title'] else 0 for word in title_words]
        feature_arr += [1 if word in item['content'] else 0 for word in contents_words]
        train_data_feature_list.append(feature_arr[:])
        train_data_class_list.append(item['pre'])

    for item in test_data_list:
        feature_arr = []
        feature_arr += [1 if word in item['title'] else 0 for word in title_words]
        feature_arr += [1 if word in item['content'] else 0 for word in contents_words]
        test_data_feature_list.append(feature_arr[:])
        test_data_id_list.append(item['id'])

    return train_data_feature_list,train_data_class_list,test_data_feature_list,test_data_id_list

def textClassifier(train_feature_list,train_class_list,test_feature_list,test_ids,result_file):
    classifier = MultinomialNB()
    print('start train')
    classifier.fit(train_feature_list,train_class_list)
    print('start predict')
    predicts_prob = classifier.predict_proba(test_feature_list)
    print('predicts_prob ', predicts_prob)
    with open(result_file, 'wb') as fp:
        fp.write(('id,pred\n').encode('utf-8'))
        res = zip(test_ids,predicts_prob)
        for item in res:
            fp.write(('{0},{1}\n'.format(item[0],item[1][0])).encode('utf-8'))

if __name__ == '__main__':
    train_file = 'train_mini.json'
    train_class_file = 'train.csv'
    test_file = 'test_mini.json'
    result_file = 'test_pre_prob.txt'
    train_file = genLocalPath(train_file)
    train_class_file = genLocalPath(train_class_file)
    test_file = genLocalPath(test_file)
    result_file = genLocalPath(result_file)
    train_feature,train_class,test_feature,test_ids = genFeature(train_file, train_class_file, test_file)
    textClassifier(train_feature,train_class,test_feature,test_ids,result_file)
