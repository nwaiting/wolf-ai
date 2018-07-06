#coding=utf-8

import random

"""
    平均感知器：
        平均感知器实现分词、词性标注、命名实体识别

    训练总结：
        使用特征去预测，然后根据预测的结果，如果对的话，将正确的标注的属性权重加1，错误的标注的权重属性减1
"""

class PerceptronTagger(object):
    def __init__(self):
        self.weights_ = None
        self.i_ = None
        self.timestramp_ = None
        self.totals_ = None
        self.model_ = None
        self.classes_ = None
        self.tagdict = None

    def train1(self, nr_iter, examples):
        """
            词性标注训练步骤：
                1、输入一个（特征、词性）键值对
                2、通过当前的特征权重预测词性
                3、如果预测错误，那么（特征、正确词性）对应的特征权重+1，并且将（特征，错误词性）对应的权重-1

            注：如果直接按照上面的方法训练的话，很容易出现过拟合的情况，
        """
        for i in range(nr_iter):
            for features,true_tag in examples:
                maybe_tag = self.predict(features=features)
                if maybe_tag != true_tag:
                    for fitem in features:
                        self.weights_[fitem][true_tag] += 1
                        self.weights_[fitem][maybe_tag] -= 1
                random.shuffle(examples)

    def train2(self, sentences, save_loc=None, nr_iter=5, quiet=False):
        """
            搜索：
                推荐的模型直接输出当前词语的词性，然后处理下一个。这些预测词性之后作为下一个词语的特征。这么做有潜在问题，但是问题不大，具体原因看下面。
                潜在的问题是这样：
                    当前位置假设为3，上个词语和下个词语是2和4，在当前位置决定词性的最佳因素可能是词语本身，单次之就是2和4的词性。
                    于是就导致了一个"鸡生蛋"的问题：我们想要预测3的词性，可是它会用到未确定的2或4的词性
                根据上面的算法，会发现从左到右处理句子，和从右到左会得到完全不同的结果
                只有当你会犯错的时候才需要用到搜索。它可以防止错误的传播，或者说你将来的决策会改正这个错误。这就是为什么对词性标注来说，搜索非常重要！！！。
                当你的模型非常棒的时候，你过去做的决策总是对的，你就不需要搜索了

                当我们改进标注器后，搜索的重要性就会下降。相较于搜索，我们更应关注多标签。如果我们让模型不那么确定，应允许单个单词有1.05个词性的时候，我们可以得到99%的准确率。
        """
        self.make_tagdict(sentences=sentences, quiet=quiet)
        self.model_.classes = self.classes_
        prev,prev2 = START
        for iter_ in range(nr_iter):
            c = 0
            n = 0
            for words,tags in sentences:
                context = START + [self.normalize(w) for w in words] + END
                for i,word in enumerate(words):
                    maybe_tag = self.tagdict.get(word)
                    if not maybe_tag:
                        feats = self.get_features(i, word, context, prev, prev2)
                        maybe_tag = self.model_.predict(feats)
                        self.model_.update(tags[i], maybe_tag, feats)
                    prev2 = prev
                    prev = maybe_tag
                    c += maybe_tag == tags[i]
                    n += 1
            random.shuffle(sentences)
            if not quiet:
                print('Iter {0} : {1}/{2}={4}'.format(iter_, c, n, _pc(c,n)))
        self.model_.average_weights()


    def make_tagdict(self, sentences, quiet=False):
        pass

    def normalize(self, word):
        pass

    def get_features(self, i, word, context, prev, prev2):
        """
            获取特征
            提取特征之前进行预处理：
                所有词语都转小写
                1800-2100数字转为year
                其他数字转为digits
                专门识别日期、电话号码、邮箱等模块
            优化：
                比如还可以加入词频等外部特征
            Map tokens-in-contexts into a feature representation, implemented as a set.
            If the features change, a new model must be trained.
        """
        def add(name, *args):
            features.add('+'.join((name,), tuple(args)))
        features = set()
        add('bias')
        add('i suffix', word[-3:])
        add('i pref1', word[0])
        add('i-1 tag', prev)
        add('i-2 tag', prev2)
        add('i tag+i-2 tag', prev, prev2)
        add('i word', context[i])
        add('i-1 tag+i word', prev, context[i])
        add('i-1 word', context[i-1])
        add('i-1 suffix', context[i-1][-3:])
        add('i-2 word', context[i-2])
        add('i+1 word', context[i+1])
        add('i+1 suffix', context[i+1][-3:])
        add('i+2 word', context[i+2])
        return features

    def update(self, truth, guess, features):
        """
            记录每个权重的累加值，然后除以最终的迭代次数，就平均了
            如何累积权重也是个技术活儿，对于大部分训练实例，都只会引起特定的几个权重变化，其他特征函数的权重不会变化。
            步骤：
                记录每个权重上次变化的时间，当我们改变一个特征权重的时候，更新这个值
        """
        def update_feature(c,f,v):
            nr_iters_at_this_weight = self.i_ - self.timestramp_[f][c]
            self.totals_[f][c] += nr_iters_at_this_weight * self.weights_[f][c]
            self.weights_[f][c] += v
            self.timestramp_[f][c] = self.i_

        self.i_ += 1
        for f in features:
            update_feature(truth, f, 1.0)
            update_feature(guess, f, -1.0)


    def predict(self, features):
        """
            预测
        """
        scores = {}
        for f,v in features.items():
            if f not in self.weights_ or v == 0:
                continue
            weights = self.weights_[f]
            for label,w in weights.items():
                scores[label] += v * w
        return max(self.classes, key=lambda label:(scores[label], label))


def main():
    pass








if __name__ == '__main__':
    main()
