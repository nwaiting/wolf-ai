#coding=utf-8
from gensim.models.keyedvectors import KeyedVectors
import os
bin_file = 'vectors.bin'
text_file = 'vectors.txt'
bin_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), bin_file)
text_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), text_file)
model = KeyedVectors.load_word2vec_format(bin_file, binary=True)
model.save_word2vec_format(text_file, binary=False)
