#coding=utf-8

from gensim.models import word2vec

def train_word2vec(train_f, model_f):
    words = word2vec.Text8Corpus(train_f)
    words_mod = word2vec.Word2Vec(words, size=100)
    words_mod.wv.save_word2vec_format(model_file, binary=False)
    #words_mod.save_word2vec_format(model_file, binary=False)

if __name__ == '__main__':
    train_file = 'Result_Country.txt'
    model_file = 'word2vec.txt'
    train_word2vec(train_file, model_file)
