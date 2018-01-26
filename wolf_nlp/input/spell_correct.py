#coding=utf-8

"""
拼写检查：
    有两个模型需要注意：
        1、语言模型
        2、误差模型

    http://www.omegaxyz.com/2017/12/26/python_check_word/
    http://norvig.com/spell-correct.html  原文
    http://python.jobbole.com/81675/  详解 怎样写一个拼写检查器（Python 版）

    给定一个词 w, 在所有正确的拼写词中, 我们想要找一个正确的词 c, 使得对于 w 的条件概率最大，即：
    argmaxc P(c|w)
    按照 贝叶斯理论：
    argmaxc P(w|c) P(c) / P(w)
    用户可以输错任何词, 因此对于任何 c 来讲, 出现 w 的概率 P(w) 都是一样的
    所以可以写成：
    argmaxc P(w|c) P(c)
    P(c)：称之为做语言模型c出现的概率，好比说, 英语中出现 the 的概率  P(‘the’) 就相对高, 而出现  P(‘zxzxzxzyy’) 的概率接近0
    P(w|c)：被称为误差模型，在用户想键入 c 的情况下敲成 w 的概率. 因为这个是代表用户会以多大的概率把 c 敲错成 w
    argmaxc：枚举所有可能的 c 并且选取概率最大的

    平滑化：
        从来没有过见过的新词一律假设出现过一次. 这个过程一般成为”平滑化”, 因为我们把概率分布为0的设置为一个小的概率值.

    编辑距离：
        拼写检查的文献宣称大约80-95%的拼写错误都是介于编译距离 1

    误差模型部分 P(w|c):
        1、把一个元音拼成另一个的概率要大于辅音 (因为人常常把 hello 打成 hallo 这样)
        2、把单词的第一个字母拼错的概率会相对小
        3、编辑距离  编辑距离为1的正确单词比编辑距离为2的优先级高, 而编辑距离为0的正确单词优先级比编辑距离为1的高.
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

    #编辑距离为1的
    def edits1(self, word):
        n = len(word)
        return set([word[0:i] + word[i+1:] for i in range(n)] +   #deletion
                [word[0:i] + word[i+1] + word[i] + word[i+2:] for i in range(n-1)] +    #transposition
                [word[0:i] + c + word[i+1:] for i in range(n) for c in self.alphabeta] +    #alteration
                [word[0:i] + c + word[i:] for i in range(n+1) for c in self.alphabeta]  #insertion
                )

    #编辑距离为2的正确词
    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.all_words)

    def correct(self, word):
        # 表达式中有优先级处理
        cand = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        #选取cond中概率最大的
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
