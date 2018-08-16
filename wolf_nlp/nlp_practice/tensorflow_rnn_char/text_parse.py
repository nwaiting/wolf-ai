#coding=utf-8

import os
import pickle
import numpy as np
import copy

class TextHandler(object):
    def __init__(self, file=None,
                        max_vocab=5000,
                        vocab_load_file=None,
                        time_inputs=None,
                        time_steps=None,
                        vocab_save_file=None):
        self.vocab_ = None

        if vocab_load_file:
            with open(vocab_load_file, 'r') as f:
                self.vocab_ = pickle.load(f)

        char_map = {}
        vocab_all_words = ''
        if file and os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if line:
                        line = line.strip('\r\n ')
                        for item in line:
                            char_map[item] = char_map.get(item, 0) + 1
                            vocab_all_words += item
            sorted_list = sorted(char_map.items(), key=lambda x:(x[1],x[0]), reverse=True)
            if len(sorted_list) > max_vocab:
                sorted_list = sorted_list[:max_vocab]
            self.vocab_ = [i[0] for i in sorted_list]

        self.word_to_int_table_ = {j:i for i,j in enumerate(self.vocab_)}
        self.int_to_word_table_ = {i:j for i,j in enumerate(self.vocab_)}
        self.text_arrays_ = self.text_to_arr(vocab_all_words)
        self.time_steps_ = time_steps
        self.time_inputs_ = time_inputs

        if vocab_save_file:
            self.save_to_file(vocab_save_file)

    @property
    def vocab_size(self):
        return len(self.vocab_) + 1

    @property
    def text_arrays(self):
        return self.text_arrays_

    def get_batch(self):
        batch_size = self.time_steps_ * self.time_inputs_
        n_batches = int(len(self.text_arrays_) / batch_size)
        #需要转换的话先保证整除
        self.text_arrays_ = self.text_arrays_[:n_batches*batch_size]
        self.text_arrays_ = self.text_arrays_.reshape((-1, self.time_inputs_))
        #self.text_arrays_ = self.text_arrays_.reshape((self.time_steps_, -1))
        while True:
            np.random.shuffle(self.text_arrays_)
            for i in range(n_batches):
                x = self.text_arrays_[i*self.time_steps_:(i+1)*self.time_steps_, :]
                y = np.zeros_like(x)
                y[:,:-1],y[:,-1] = x[:,1:],x[:,0]
                yield x,y


    def word_to_int(self, word):
        return self.word_to_int_table_.get(word, len(self.vocab_))

    def int_to_word(self, i):
        return self.int_to_word_table_.get(i, '<unk>')

    def text_to_arr(self, texts):
        arr = []
        for item in texts:
            arr.append(self.word_to_int(item))
        return np.array(arr)

    def arr_to_text(self, arrs):
        texts = ''
        for i in arrs:
            texts += self.int_to_word(i)
        return texts

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.vocab_, f)
