#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from trietree import TrieTree

class LexiHandler(object):
    def __init__(self, syl2chinese):
        self.syl2chinese_ = syl2chinese
        self.syl2ch_TrieTree = TrieTree()

    def Init(self):
        with open(self.syl2chinese_, "rb") as f:
            for line in f.xreadlines():
                line = line.strip()
                resutlt = re.split("'|\t", line)
                self.syl2ch_TrieTree.Insert(resutlt[:-1], resutlt[-1])

    def GetChineseFromSpells(self, spells):
        node = self.syl2ch_TrieTree.SearchNode(spells)
        if node:
            s = node.GetContents()
            if s:
                return list(s)

if __name__ == '__main__':
    s = ['zhen', 'de', 'bu', 'hao', 'wan']
    lexi = LexiHandler("lexicon.bdt")
    lexi.Init()
    for k in s:
        res = lexi.GetChineseFromSpells([k,])
        if res:
            for j in res:
                print k,j
