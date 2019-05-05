#coding=utf-8

"""
    NB-朴素贝叶斯：
        partial_fit方法：
            GaussianNB一个重要的功能是有partial_fit方法，这个方法的一般用在如果训练集数据量非常大，一次不能全部载入内存的时候。这时我们可以把训练集分成若干等分，
                重复调用partial_fit来一步步的学习训练集，非常方便。
"""

from sklearn.naive_bayes import GaussianNB,BernoulliNB,MultinomialNB


def main():
    """
        GaussianNB类的主要参数仅有一个，即先验概率priors ，对应Y的各个类别的先验概率P(Y=Ck)。
        这个值默认不给出，如果不给出此时P(Y=Ck)=mk/m。其中m为训练集样本总数量，mk为输出为第k类别的训练集样本数。如果给出的话就以priors为准
    """
    nb = GaussianNB(priors=None)

    # 多次循环fit
    nb.partial_fit()

    """
        binarize：
            BernoulliNB一共有4个参数，其中3个参数的名字和意义和MultinomialNB完全相同。
            唯一增加的一个参数是binarize。这个参数主要是用来帮BernoulliNB处理二项分布的，可以是数值或者不输入。
            如果不输入，则BernoulliNB认为每个数据特征都已经是二元的。否则的话，小于binarize的会归为一类，大于binarize的会归为另外一类
    """
    nb = BernoulliNB(alpha=1.0, fit_prior=True, class_prior=None, binarize=.0)


    """
        alpha：
            λ为一个大于0的常数，常常取为1，即拉普拉斯平滑。也可以取其他值
            参数alpha即为上面的常数λ，如果你没有特别的需要，用默认的1即可。如果发现拟合的不好，需要调优时，可以选择稍大于1或者稍小于1的数
        fit_prior:
            布尔参数fit_prior表示是否要考虑先验概率，如果是false,则所有的样本类别输出都有相同的类别先验概率。
            否则可以自己用第三个参数class_prior输入先验概率，或者不输入第三个参数class_prior让MultinomialNB自己从训练集样本来计算先验概率，
                此时的先验概率为P(Y=Ck)=mk/m。其中m为训练集样本总数量，mk为输出为第k类别的训练集样本数
            fit_prior	class_prior	  最终先验概率
                false	  填或者不填没有意义	P(Y=Ck)=1/k
                true	   不填	    P(Y=Ck)=mk/m
                true	   填	     P(Y=Ck)=class_prior
    """
    nb = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)



if __name__ == '__main__':
    main()
