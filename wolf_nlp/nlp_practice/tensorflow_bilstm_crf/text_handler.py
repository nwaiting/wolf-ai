#coding=utf-8

import random
import os
import sys
import pickle
import numpy as np

# tag-BIO
tag2label = {"O":0,
            "B-PER":1,"I-PER":2,
            "B-LOC":3,"I-LOC":4,
            "B-ORG":5,"I-ORG":6}

def sentence2id(sents, word2id):
    sentence_id = []
    for word in sents:
        word = str()
        if word.isdigit():
            word = '<NUM>'
        elif ('\u0041' <= word <= '\u005a') or ('\u0061' <= word <= '\u007a'):
            word = '<ENG>'
        if word not in word2id:
            word = '<UNK>'
        sentence_id.append(word2id[word])
    return sentence_id

def batch_generator(data, batch_size, vocab, tag2label, shuffle=False):
    if shuffle:
        random.shuffle(data)

    seqs = []
    lables = []
    for (st, tags) in data:
        sentence_lab = sentence2id(st, vocab)
        tag_lab = [tag2label[tag] for tag in tags]
        if len(seqs) == batch_size:
            yield seqs,lables
            seqs = []
            lables = []
        seqs.append(sentence_lab)
        lables.append(tag_lab)
    if len(seqs) != 0:
        yield seqs,lables

def pad_sequences(sequences, pad_mask=0):
    #补充对齐sequence, 填充seq_list，
    #return：句子的列表和长度的列表
    max_len = max(len(x) for x in sequences)
    seq_list = []
    seq_len_list = []
    for seq in sequences:
        seq = list(seq)
        seq_new = seq[:max_len] + [pad_mask] * max(max_len-len(seq), 0)
        seq_list.append(seq_new)
        seq_len_list.append(min(len(seq), max_len))
    return seq_list,seq_len_list

def conlleval(label_prediction, label_path, metric_path):
    """
    """
    eval_perl = './conlleval_rev.pl'
    with open(label_path, 'w') as fw:
        line = []
        for sent_result in label_prediction:
            for ch, tag, tag_ in sent_result:
                tag = '0' if tag == 'O' else tag
                ch = ch.encode('utf-8')
                line.append('{} {} {}\n'.format(ch, tag, tag_))
            line.append('\n')
        fw.write(line)
    #os.system("perl {} < {} > {}".format(eval_perl, label_path, metric_path))
    with open(metric_path) as fr:
        merics = [line.strip() for line in fr.readlines()]
    return merics

def read_dictionary(data_path):
    with open(data_path, 'rb') as f:
        word2id = pickle.load(f)
        print('data len {0}'.format(len(word2id)))
    return word2id

def random_embedding(vocab, embedding_dim):
    embedding_matri = np.random.uniform(-0.25, 0.25, (len(vocab), embedding_dim))
    return np.float32(embedding_matri)

def read_corpus(data_path):
    """
    return：[(sentence,tag)]
    """
    data = []
    with open(data_path, encoding='utf-8') as f:
        sents,tags = [], []
        for line in f.readlines():
            if line != '\n':
                [ch,tag] = line.strip('\r\n ').split()
                sents.append(ch)
                tags.append(tag)
            else:
                data.append((sents,tags))
                sents = []
                tags = []
    return data

def get_entiry(tag_seq, char_seq):
    loc = get_LOC_entity(tag_seq, char_seq)
    per = get_PER_entity(tag_seq, char_seq)
    org = get_ORG_entity(tag_seq, char_seq)
    return per, loc, org
def get_PER_entity(tag_seq, char_seq):
    char_seq_len = len(char_seq)
    PER = []
    for i,(char,tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-PER':
            if 'per' in locals().keys():
                PER.append(per)
                del per
            per = char
            if i+1 == char_seq_len:
                PER.append(per)
        if tag == 'I-PER':
            per += char
            if i+1 == char_seq_len:
                PER.append(per)
        if tag not in ['I-PER', 'B-PER']:
            if 'per' in locals().keys():
                PER.append(per)
                del per
            continue
    return PER

def get_LOC_entity(tag_seq, char_seq):
    char_seq_len = len(char_seq)
    LOC = []
    for i,(char,tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == char_seq_len:
                LOC.append(loc)
        if tag == 'I-LOC':
            loc += char
            if i+1 == char_seq_len:
                LOC.append(loc)
        if tag not in ['B-LOC','I-LOC']:
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue
    return LOC


def get_ORG_entity(tag_seq, char_seq):
    char_seq_len = len(char_seq)
    ORG = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-ORG':
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            org = char
            if i+1 == char_seq_len:
                ORG.append(org)
        if tag == 'I-ORG':
            org += char
            if i+1 == char_seq_len:
                ORG.append(org)
        if tag not in ['I-ORG', 'B-ORG']:
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            continue
    return ORG


class TextHandler(object):
    def __init__(self):
        pass
