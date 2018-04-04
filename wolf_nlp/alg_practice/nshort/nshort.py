#coding=utf8

"""
NShort算法：
    参考：http://www.cnblogs.com/Finley/p/6619187.html
    最短路径算法最好使用Floyd或者Dijsktra算法，但是耗时太长，大多数情况下使用贪心算法求得次优解就可以达到所需精度
    词典法本身就是一种不精确的方法，最短路径的最优解和次优解在分词效果上相差不大
    但是求得最优解的时间复杂度由O(n2)到O(n3)

"""

text = """
罗辑 离开 墓碑 ， 站 到 他 为 自己 挖掘 的 墓穴 旁 ， 将 手枪 顶到 自己 的 心脏 位置 ，
说 ： “ 现在 ， 我 将 让 自己 的 心脏 停止 跳动 ， 与此同时 我 也 将 成为 两个 世界 有史以来 最大 的 罪犯 。
对于 所 犯下 的 罪行 ， 我 对 两个 文明 表示 深深 的 歉意 ，
但 不会 忏悔 ， 因为 这是 唯一 的 选择 。 我 知道 智子 就 在 身边 ， 但 你们 对 人类 的 呼唤 从不 理睬 ，
无言 是 最大 的 轻蔑 ， 我们 忍受 这种 轻蔑 已经 两个 世纪 了 ， 现在 ， 如果 你们 愿意 ，
可以 继续 保持 沉默 ， 我 只 给 你们 三十 秒钟 时间 ，
传授 传授 传授 一点 一点 一点 一点 人事 人生 人生 人生
"""

class NShort(object):
    def __init__(self, filename=None):
        self.word_dict = {}
        self.debug_show = False
        self.filename_ = filename if filename else None
        self.buildWordDict(text)

    def buildWordDict(self, s):
        if self.filename_:
            with open(self.filename_, 'r', encoding='utf-8') as fp:
                for line in fp.readlines():
                    line = line.strip('\r\n ')
                    line_list = line.split('\t')
                    if len(line_list) > 0:
                        self.word_dict[line_list[0]] = self.word_dict.get(line_list[0], 0) + 1
                        if self.debug_show:
                            print(line_list[0], self.word_dict[line_list[0]])
        else:
            s = s.strip('\r\n ')
            for sitem in s.split(' '):
                sitem = sitem.strip('\r\n  ')
                self.word_dict[sitem] = self.word_dict.get(sitem, 0) + 1
                if self.debug_show:
                    print(sitem, self.word_dict[sitem])

    def buildTag(self, sentence):
        dag = {}
        # (i,(stop,num))
        for i in range(len(sentence)):
            uni = [i+1]
            tmp = [(i+1,1)]
            for j in range(i+1,len(sentence)+1):
                fra = sentence[i:j]
                num = self.word_dict.get(fra, 0)
                if num > 0 and j not in uni:
                    tmp.append((j,num))
                    uni.append(j)
            dag[i] = tmp
        return dag


    def cut(self, sentence):
        route = self.predict(sentence)
        next = 0
        i = 0
        word_list = list()
        while i < len(sentence):
            next = route[i]
            word_list.append(sentence[i:next])
            i = next
        return word_list

    def predict(self, sentence):
        dag = self.buildTag(sentence)
        slen = len(sentence)
        route = [0] * slen
        for i in range(slen):
            # 多个字段比较 先比较x[1] 然后比较x[0]
            route[i] = max(dag[i], key=lambda x:(x[1],x[0]))[0]
        return route


if __name__ == "__main__":
    import os
    f = os.path.join(os.path.dirname(__file__), '../data/CoreNatureDictionary.txt')
    nshort = NShort(f)
    cases = [
        "给你们传授一点人生的经验",
        "我来到北京清华大学",
        "长春市长春节讲话",
        "我们在野生动物园玩",
        "我只是做了一些微小的工作",
        "国庆节我在研究中文分词",
        "比起生存还是死亡来忠诚与背叛可能更是一个问题"
    ]
    for case in cases:
        print(nshort.cut(case))
