#coding=utf-8

from gensim.models import word2vec

def train_word2vec(train_f, model_f, word2vec_size):
    words = word2vec.Text8Corpus(train_f)
    words_mod = word2vec.Word2Vec(words, size=word2vec_size)
    words_mod.wv.save_word2vec_format(model_file, binary=False)
    #words_mod.save_word2vec_format(model_file, binary=False)

if __name__ == '__main__':
    w_size = 300
    train_file = 'Result_Country.txt'
    model_file = 'word2vec_{0}.txt'.format(w_size)
    train_word2vec(train_file, model_file, w_size)
