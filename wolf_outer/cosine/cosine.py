#coding=utf8

import os
import math

def cal_cosine(vec_1, vec_2):
    d1 = 0.0
    na = 0.0
    nb = 0.0
    #公式 cos = (d1) / (na**(1/2) * nb**(1/2))
    for ia,ib in zip(vec_1, vec_2):
        ia = float(ia)
        ib = float(ib)
        d1 += ia * ib
        na += math.pow(ia, 2)
        nb += math.pow(ib, 2)
    if na == 0.0 or nb == 0.0:
        return None
    # cos公式 (d1) / ()
    return float(d1)/(math.sqrt(na) * math.sqrt(nb))


def parse_file(f):
    t_vec = set()
    with open(f, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            #去除行首和行尾的空格、\r、\n等字符，然后以空格分开
            line = line.strip('\r\n ').split(' ')
            t_vec |= set(line)
    return t_vec

def load_word2vec_model(model_f):
    d = {}
    with open(model_f, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\r\n ')
            if line:
                lines = line.split()
                if len(lines) > 0:
                    d[lines[0]] = lines[1:]
    return d

def cal_texts(text_1, text_2, model_vecs_map):
    text_1_set = parse_file(text_1)
    text_2_set = parse_file(text_2)
    text_all = text_1_set | text_2_set
    text_1_vec = []
    text_2_vec = []
    if model_vecs_map:
        for i in text_1_set:
            if i in model_vecs_map:
                text_1_vec += model_vecs_map[i]
        for i in text_2_set:
            if i in model_vecs_map:
                text_2_vec += model_vecs_map[i]
        max_len = max(len(text_1_vec), len(text_2_vec))
        if max_len == len(text_1_vec):
            text_2_vec += [0] * (max_len-len(text_1_vec))
        else:
            text_1_vec += [0] * (max_len-len(text_2_vec))
    else:
        text_1_vec = [1 if i in text_1_set else 0 for i in text_all]
        text_2_vec = [1 if i in text_2_set else 0 for i in text_all]
    return cal_cosine(text_1_vec, text_2_vec)

if __name__ == '__main__':
    file_1 = '0001.txt'
    file_2 = '0002.txt'
    model_file = 'word2vec.txt'
    """
    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    file_1 = os.path.join(file_dir_path, file_1)
    file_2 = os.path.join(file_dir_path, file_2)
    """
    if not os.path.exists(file_1):
        print('error file {0} not exists'.format(file_1))
    if not os.path.exists(file_2):
        print('error file {0} not exists'.format(file_2))
    if not os.path.exists(model_file):
        print('error file {0} not exists'.format(model_file))

    print(cal_texts(file_1, file_2, load_word2vec_model(model_file)))
