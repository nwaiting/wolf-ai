#coding=utf8

"""
ngram中文分词：
    参考：http://www.52nlp.cn/%E5%88%9D%E5%AD%A6%E8%80%85%E6%8A%A5%E9%81%93%EF%BC%882%EF%BC%89%EF%BC%9A%E5%AE%9E%E7%8E%B0-1-gram%E5%88%86%E8%AF%8D%E7%AE%97%E6%B3%95

    ngram是求一整条链路的概率，根据马尔科夫假设，当前词仅跟前面有限的几个词有关
    利用最大似然算出一组参数，使得训练样本的概率取得最大值

    数据平滑：
        由于数据稀疏的存在，极大似然不是一种很好的参数估计的方法
        主要策略：把训练样本中出现过的事件的概率适当减小，然后把减小得到的概率密度分配给训练语料中没有出现过的事件
        平滑算法：
            Laplacian (add-one) smoothing
            Additive smoothing
            Good-Turing estimate
            Jelinek-Mercer smoothing (interpolation)  差值
            Katz smoothing (backoff)  回退
            Witten-Bell smoothing
            Absolute discounting
            Kneser-Ney smoothing
            Add-k Smoothing（Lidstone’s law）

            各种算法概述：
                差值：就是把不同阶的模型结合起来
                    把不同级别的ngram模型线性加权组合后来使用
                    简单线性插值可以使用：P(wn|wn-2, wn-1) = λ1P(wn) + λ2P(wn|wn-1) + λ3P(wn|wn-2,wn-1)
                    其中∑iλi=1，λi可以凭经验设定，也可以通过EM算法确定
                回退：就是说如果没有3gram，就是用bigram，如果没有bigram，就用unigram
                    通常我们认为高阶模型更加可靠，当能够获知更多历史信息时，其实就获得了当前推测的更多约束，这样就更容易得出正确的结论。
                    所以在高阶模型可靠时，尽可能的使用高阶模型，但是有时候高阶模型的计数结果可能为0，这是我们就转而使用低阶模型来避免稀疏数据的问题
                    比如3gram中的"like chinese food"语料中没有出现，计数为0，在回退策略中，会选择使用"chinese food"来替代
            差值和回退的区别：
                相同：都涉及到较高和较低阶模型的信息，在决定没有出现过的ngram时，两个都使用了低阶模型信息
                不同：在决定非零计数的ngram概率时，差值模型使用了低阶模型，而回退模型不使用
                      与差值算法相比，回退算法需要参数较少，可以直接确定，无需通过迭代反复训练，更加方便

                add-one：将规定没有出现过的N-Gram在训练语料中出现了一次
                    公式：
                        Padd1(wi|wi-n+1,...,w1) = (C(wi-n+1,...,wi) + 1) / (C(wi-n+1,...,wi-1) + V)
                add-k：既然我们认为加1有点过了，不然选择一个小于1的正数k
                    公式：
                        Paddk(wi|wi-n+1,...,w1) = (C(wi-n+1,...,wi) + k) / (C(wi-n+1,...,wi-1) + kV)
                        有一个缺点是k必须是人为确定，所以没有一个统一的标准
                Kneser-Ney Smoothing：
                    概述：这种算法目前是一种标准的，而且是非常先进的平滑算法，它其实相当于是前面讲过的几种算法的综合



ngram判断两个句子或者单词的距离：
    参考：https://blog.csdn.net/baimafujinji/article/details/51281816
    两个单词的编辑距离：
        求字符串s和字符串t的距离
        公式：L = Gn(s) + Gn(t) - 2 * (Gn(s) ∩ Gn(t))
        Gn(s)表示单词s的切分结果数
        Gn(t)表示单词t的切分结果数
        Gn(s) ∩ Gn(t) 表示s和t相同的单词数
        比如求字符串Gorbachev和Gorbechyov的距离：
        先进行切分，当ngram的n为2时，切分结果：
            Go,or,rb,ba,ac,ch,he,ev
            Go,or,rb,be,ec,ch,hy,yo,ov
            距离计算：L = 8 + 9 - 2 * (4)

"""

"""
    缺少一个ngram中文分词的实现
"""
class Ngram(object):
    def __init__(self, n=None):
        self.n_ = n if n else 2

    def splitStr(self, s):
        res = list()
        i = 0
        while i < len(s):
            if i + self.n_ <= len(s):
                res.append(s[i:i+self.n_])
            else:
                break
            i += 1
        return res

    def editLen(self, s, t):
        s_list = self.splitStr(s)
        t_list = self.splitStr(t)
        sec_list = [i for i in s_list if i in t_list]
        L = len(s_list) + len(t_list) - 2 * len(sec_list)
        return L

if __name__ == '__main__':
    ngram = Ngram()
    s = 'Gorbachev'
    t = 'Gorbechyov'
    print(ngram.editLen(s, t))
