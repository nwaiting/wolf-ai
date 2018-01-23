#coding=utf-8

"""
拼写检查：
    http://www.omegaxyz.com/2017/12/26/python_check_word/
"""

import collections,re,os

class Spelling(object):
    def __init__(self, file_name=None):
        if file_name:
            self.file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
        self.all_words = collections.defaultdict(lambda:1)
        self.alphabeta = 'abcdefghijklmnopqrstuvwxyz'

    def train(self):
        if self.file_name:
            for i in self.words(open(self.file_name,'rb').read().decode()):
                self.all_words[i] += 1

    def words(self, words):
        return re.findall('[a-z]+', words)

    def known(self, word):
        return set(w for w in word if w in self.all_words)

    def edits1(self, word):
        n = len(word)
        return set([word[0:i] + word[i+1:] for i in range(n)] +   #deletion
                [word[0:i] + word[i+1] + word[i] + word[i+2:] for i in range(n-1)] +    #transposition
                [word[0:i] + c + word[i+1:] for i in range(n) for c in self.alphabeta] +    #alteration
                [word[0:i] + c + word[i:] for i in range(n+1) for c in self.alphabeta]  #insertion
                )

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.all_words)

    def correct(self, word):
        cand = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return max(cand, key=lambda w:self.all_words[w])

    def show(self):
        limit = 0
        for k,v in self.all_words.items():
            print(k,v)
            if limit > 100:
                break
            limit += 1

if __name__ == '__main__':
    spell = Spelling('big.txt')
    spell.train()
    #spell.show()
    print(spell.correct('speling'))
    print(spell.correct('korrecter'))
