#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from trietree import TrieTree
from model_handler import ModelHandler
from syllable_handler import SyllableHandler
from lexi_handler import LexiHandler

class Input(object):
    def __init__(self, model_file, syllable_file, syl2chinese):
        self.modelhandler = ModelHandler(model_file)
        self.syllablehandler = SyllableHandler(syllable_file)
        self.lexihandler = LexiHandler(syl2chinese)
        self.Init()

    def Init(self):
        self.syllablehandler.Init()
        self.lexihandler.Init()
        self.modelhandler.Init()

    def SpellSplit(self, pinyin):
        return self.syllablehandler.SpellSplit(pinyin)

    def SpellToChi(self, spells):
        """
        改进字典树 拼音转汉字
        """
        results = list()
        ch = self.lexihandler.GetChineseFromSpells(spells)
        if ch:
            results.append(ch)
        else:
            #没找到 需要在单个字符查找
            for i in spells:
                res = self.lexihandler.GetChineseFromSpells([i,])
                if res:
                    results.append(res)
        return results


    def GetChineseFromPinyin(self, pinyin):
        spelllist = self.SpellSplit(pinyin)
        return self.SpellToChi(spelllist)

    def GetProba(self, f, s):
        return self.modelhandler.GetChineseProb(f,s)

class Node(object):
    def __init__(self,v=None,_pre=None,_next=None,_prob=None):
        self.value_=v
        self.pre_=_pre
        self.next_=_next
        self.prob_=_prob;

def calTopPath(l, k):
    pass


if __name__ == '__main__':
    """
    r=[['你','拟','尼'],['好','豪'],['妈','吗']]
    c = sum(len(i) for i in r)
    d = [[0 for colu in xrange(c)] for row in xrange(c)]
    for i in xrange(len(r[0]),len(d)):
        for j in xrange(i):
            x0 = 0
            x1 = 0
            y0 = 0
            y1 = 0
            t = 0
            index = 0
            indey = 0
            for x in r:
                tmp = len(x)
                t += len(x)
                index += 1
                if t >= j:
                    x0 = index - 1
                    if j >= t:
                        x0 = index
                    x1 = (j - (t - tmp))%tmp
                    break

            t = 0
            index = 0
            indey = 0
            for x in r:
                tmp = len(x)
                t += len(x)
                indey += 1
                if t >= i:
                    y0 = indey - 1
                    if i >= t:
                        y0 = indey
                    y1 = (i - (t - tmp))%tmp
                    break
            if y0 - x0 > 1 or y0 == x0:
                continue
            if x1 < len(r[x0]) and y1 < len(r[y0]):
                print j,i,x0,x1,y0,y1,r[x0][x1], r[y0][y1]
    import sys
    sys.exit(0)
    """

    inf=-999999999.00
    input = Input("text.train", "syllable.bdt", "lexicon.bdt")
    res = input.GetChineseFromPinyin('zhendebuhaowan')
    """
    计算出 res[][] 的二维数组 求最大概率组合， 求前n个
    res:
    [57, 11, 26, 33, 45]
    駗 斟 缜 碪 诊 稹 枕 侦 振 砧 朕 瑱 姫 鸩 榛 圳 溱 鍼 鎭 薽 畛 贞 紾 眹 填 蓁 臻 揕 葴 禛 镇 疹 鬒 桭 桢 甄 袗 祯 甽 浈 阵 珍 帧 獉 鸩毒 遉 胗 眞 真 赈 眕 针 震 黰 轸 箴 椹
    悳 徳 㥁 得 底 地 德 锝 惪 㝵 的
    怖 蔀 堡 誧 醭 补 不 簿 歩 逋 卟 步 篰 钸 部 埗 布 埔 哺 卜 钚 晡 捗 捕 埠 鯆
    皋 薃 薅 皞 皜 号 嚆 皓 鄗 壕 薧 澔 耗 毫 蒿 呺 濠 嗥 灏 恏 暠 好 颢 嚎 諕 豪 郝 昊 蚝 貉 秏 茠 浩
    挽 纨 丸 完 芄 蔓 弯 皖 畹 宛 輓 玩 抏 卍 惌 剜 脘 顽 夗 万 夘 涴 莞 琬 槾 汍 蜿 碗 掔 豌 烷 绾 晚 卐 捥 湾 腕 刓 菀 晥 晩 翫 絻 惋 婉
    d:
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    """

    c = sum(len(i) for i in res)
    d = [[0 for row in xrange(c)] for colu in xrange(c)]
    dist = [0 for i in xrange(c)]
    l = list()
    for i in xrange(len(res[0]),len(d)):
        min_va = inf
        tmp_list = None
        for j in xrange(i):
            x0 = 0
            x1 = 0
            y0 = 0
            y1 = 0
            t = 0
            index = 0
            for x in xrange(len(res)):
                tmp = len(res[x])
                t += tmp
                index += 1
                if t >= j:
                    x0 = index-1
                    if j >= t:
                        x0 = index
                    x1 = (j - (t - tmp))%tmp
                    break

            t = 0
            indey = 0
            for x in xrange(len(res)):
                tmp = len(res[x])
                t += tmp
                indey += 1
                if t >= i:
                    y0 = indey-1
                    if i >= t:
                        y0 = indey
                    y1 = (i - (t - tmp))%tmp
                    break
            if y0 - x0 > 1 or y0 == x0:
                continue
            if x1 < len(res[x0]) and y1 < len(res[y0]):
                prob = input.GetProba(res[x0][x1], res[y0][y1])
                #with open("aaaaa.log", "ab") as f:
                #    f.write("{} {} {} {} {} {} {}{}\n".format(j,i,x0,x1,y0,y1,res[x0][x1], res[y0][y1]));
                if prob:
                    print j,i,x0,x1,y0,y1,prob,res[x0][x1],res[y0][y1],dist[j],min_va
                    if dist[j] + float(prob) > min_va:
                        min_va = dist[j] + float(prob)
                        tmp_list = res[x0][x1] + res[y0][y1]
            """
            if d[j][i] > 0:
                if dist[j] + d[j][i] < min_va:
                    min_va = dist[j] + d[j][i]
            """
        if min_va != inf:
            dist[i] = min_va
            l.append(tmp_list)
            print "tmp_list=", tmp_list,min_va
    print "dist=", dist
    for k in l:
        print k,

    #cal path##########
    j = len(res) - 1
    st = [j]
    flag = True
    while j > 0 and flag:
        flag = False
        for i in xrange(j):
            if res[i][j] > 0:
                #res[i][j] 需要转换为概率 input.GetProba(res[x0][x1], res[y0][y1]) !!!!
                if dist[j] == dist[i] + res[i][j]:
                    st.append(i)
                    flag = True
        j = st[len(st)-1]
    print st
    ###################

    """
    d = {}
    for i in xrange(len(res)):
        for j in xrange(len(res[i])):
            v = res[i][j]
            if i != len(res) - 1:
                d[v] = res[i+1][:]
    print d
    """
