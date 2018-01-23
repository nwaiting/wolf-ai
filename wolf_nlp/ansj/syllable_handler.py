#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from trietree import TrieTree

class SyllableHandler(object):
    def __init__(self, syllable_file):
        self.syllablefile_ = syllable_file
        self.sylllist = TrieTree()

    def Init(self):
        with open(self.syllablefile_, "rb") as f:
            for line in f.xreadlines():
                line = line.strip()
                self.sylllist.Insert(line)
    def SpellSplit(self, pinyin):
        t = str()
        i = 0
        node = self.sylllist.root_
        while i < len(pinyin):
            if pinyin[i] in node.childrens_:
                t += pinyin[i]
                node = node.childrens_[pinyin[i]]
            else:
                node = self.sylllist.root_
                t += ' '
                i -= 1
            i += 1
        return t.split(' ')
