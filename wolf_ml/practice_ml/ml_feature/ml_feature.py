# coding=utf-8


"""
    参考：https://github.com/HanXiaoyang/Kaggle_Titanic
        https://blog.csdn.net/han_xiaoyang/article/details/49797143
        http://www.cnblogs.com/jasonfreak/p/5448385.html

    总结的一些经验：
        baseline model：
            Andrew Ng老师似乎在coursera上说过，应用机器学习，千万不要一上来就试图做到完美，先撸一个baseline的model出来，
            再进行后续的分析步骤，一步步提高，所谓后续步骤可能包括『分析model现在的状态(欠/过拟合)，分析我们使用的feature的作用大小，
            进行feature selection，以及我们模型下的bad case和产生的原因』等等

        特征处理：
            Kaggle上的大神们，也分享过一些experience，说几条我记得的哈：
            『对数据的认识太重要了！』
            『数据中的特殊点/离群点的分析和处理太重要了！』
            『特征工程(feature engineering)太重要了！在很多Kaggle的场景下，甚至比model本身还要重要』
            『要做模型融合(model ensemble)啊啊啊！』


"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler,Binarizer,OneHotEncoder,Normalizer,Imputer,PolynomialFeatures,MinMaxScaler,FunctionTransformer,RobustScaler
from sklearn.feature_selection import SelectKBest, chi2, RFE, SelectFromModel
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from scipy.stats import pearsonr, pearson3

"""
    数据预处理：
        标准化，返回值为标准化后的数据
        StandardScaler().fit_transform(iris.data)

        区间缩放法
        区间缩放，返回值为缩放到[0, 1]区间的数据
        MinMaxScaler().fit_transform(iris.data)

        二值化，阈值设置为3（大于3为1，小于3为0），返回值为二值化后的数据
        Binarizer(threshold=3).fit_transform(iris.data)

        哑编码，对IRIS数据集的目标值，返回值为哑编码后的数据，只能对数值型数据进行处理
        OneHotEncoder().fit_transform(iris.target.reshape((-1,1)))

        归一化，返回值为归一化后的数据
        归一化是依照特征矩阵的行处理数据，其目的在于样本向量在点乘运算或其他核函数计算相似性时，拥有统一的标准，也就是说都转化为“单位向量”
        Normalizer().fit_transform(iris.data)

        如果你的数据有许多异常值，那么使用数据的均值与方差去做标准化就不行了
        你可以使用robust_scale 和 RobustScaler这两个方法。它会根据中位数或者四分位数去中心化数据
        RobustScaler()

        缺失值计算
        由于IRIS数据集没有缺失值，故对数据集新增一个样本，4个特征均赋值为NaN，表示数据缺失
        缺失值计算，返回值为计算缺失值后的数据
        参数missing_value为缺失值的表示形式，默认为NaN
        参数strategy为缺失值填充方式，默认为mean（均值）
        Imputer().fit_transform(vstack((array([nan, nan, nan, nan]), iris.data)))

        数据变换
        常见的数据变换有基于多项式的、基于指数函数的、基于对数函数的
        多项式转换,参数degree为度，默认值为2
        PolynomialFeatures().fit_transform(iris.data)

        自定义转换函数为对数函数的数据变换
        基于单变元函数的数据变换可以使用一个统一的方式完成，使用preproccessing库的FunctionTransformer对数据进行对数函数转换
        第一个参数是单变元函数
        FunctionTransformer(log1p).fit_transform(iris.data)

    特征选择：
        当数据预处理完成后，我们需要选择有意义的特征输入机器学习的算法和模型进行训练。
        从两个方面来选择特征：
            特征是否发散：如果一个特征不发散，例如方差接近于0，也就是说样本在这个特征上基本上没有差异，这个特征对于样本的区分并没有什么用。
            特征与目标的相关性：这点比较显见，与目标相关性高的特征，应当优选选择。除方差法外，本文介绍的其他方法均从相关性考虑。
        根据特征选择的形式，可以分为三种：
            1、过滤法（filter）
                按照发散性或相关性对各个特征进行评分，设定阈值或者待选择阈值的个数，进行选择特征
                计算每一个特征与响应变量的相关性：工程上常用的手段有计算皮尔逊系数和互信息系数，皮尔逊系数只能衡量线性相关性而互信息系数能够很好地度量各种相关性，但是计算相对复杂一些
            2、包装法（wrapper）
                根据目标函数（通常是效果评分），每次选择若干特征或者排除若干特征）
            3、嵌入法（embedded）
                先使用某些机器学习算法进行模型训练，得到各个特征的权值系数，根据系数大小选择特征。类似于filter方法

        常见方法：
            过滤法：
                1 方差选择
                    使用方差选择法，先要计算各个特征的方差，然后根据阈值，选择方差大于阈值的特征
                    使用feature_selection库的VarianceThreshold类来选择特征的代码如下，
                    # 方差选择法，返回值为特征选择后的数据，参数threshold为方差的阈值
                    VarianceThreshold(threshold=3).fit_transform(iris.data)
                2、相关系数法
                    使用相关系数法，先要计算各个特征对目标值的相关系数以及相关系数的P值
                    用feature_selection库的SelectKBest类结合相关系数来选择特征的代码如下，
                    # 选择K个最好的特征，返回选择特征后的数据
                    # 第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。在此定义为计算相关系数
                    # 参数k为选择的特征个数
                    SelectKBest(lambda X, Y: array(map(lambda x:pearsonr(x, Y), X.T)).T, k=2).fit_transform(iris.data, iris.target)
                3、卡方检验
                    经典的卡方检验是检验定性自变量对定性因变量的相关性。假设自变量有N种取值，因变量有M种取值，
                        考虑自变量等于i且因变量等于j的样本频数的观察值与期望的差距，构建统计量，这个统计量的含义简而言之就是自变量对因变量的相关性。
                    用feature_selection库的SelectKBest类结合卡方检验来选择特征的代码如下，
                    #选择K个最好的特征，返回选择特征后的数据
                    SelectKBest(chi2, k=2).fit_transform(iris.data, iris.target)
                4、互信息法
                    经典的互信息也是评价定性自变量对定性因变量的相关性的
                    为了处理定量数据，最大信息系数法被提出，使用feature_selection库的SelectKBest类结合最大信息系数法来选择特征的代码如下，
                    from sklearn.feature_selection import SelectKBest
                    from minepy import MINE

                    #由于MINE的设计不是函数式的，定义mic方法将其为函数式的，返回一个二元组，二元组的第2项设置成固定的P值0.5
                    def mic(x, y):
                        m = MINE()
                        m.compute_score(x, y)
                        return (m.mic(), 0.5)

                    #选择K个最好的特征，返回特征选择后的数据
                    SelectKBest(lambda X, Y: array(map(lambda x:mic(x, Y), X.T)).T, k=2).fit_transform(iris.data, iris.target)

            包装法 Wrapper：
                递归特征消除法
                递归消除特征法使用一个基模型来进行多轮训练，每轮训练后，消除若干权值系数的特征，再基于新的特征集进行下一轮训练
                使用feature_selection库的RFE类来选择特征的代码如下，
                #递归特征消除法，返回特征选择后的数据
                #参数estimator为基模型
                #参数n_features_to_select为选择的特征个数
                RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(iris.data, iris.target)

            嵌入法 Embedded：
                1、基于惩罚项的特征选择法
                    使用带惩罚项的基模型，除了筛选出特征外，同时也进行了降维
                    使用feature_selection库的SelectFromModel类结合带L1惩罚项的逻辑回归模型，来选择特征的代码如下
                    #带L1惩罚项的逻辑回归作为基模型的特征选择
                    SelectFromModel(LogisticRegression(penalty="l1", C=0.1)).fit_transform(iris.data, iris.target)

                    L1惩罚项降维的原理在于保留多个对目标值具有同等相关性的特征中的一个，所以没选到的特征不代表不重要。故，可结合L2惩罚项来优化。
                    具体操作为：若一个特征在L1中的权值为1，选择在L2中权值差别不大且在L1中权值为0的特征构成同类集合，将这一集合中的特征平分L1中的权值，故需要构建一个新的逻辑回归模型
                    使用feature_selection库的SelectFromModel类结合带L1以及L2惩罚项的逻辑回归模型，来选择特征的代码如下，
                    # 带L1和L2惩罚项的逻辑回归作为基模型的特征选择，参数threshold为权值系数之差的阈值
                    SelectFromModel(LR(threshold=0.5, C=0.1)).fit_transform(iris.data, iris.target) #LR是自定义的函数，即上面的优化方案

                2、基于树模型的特征选择法
                    树模型中GBDT也可用来作为基模型进行特征选择
                    使用feature_selection库的SelectFromModel类结合GBDT模型，来选择特征的代码如下，
                    # GBDT作为基模型的特征选择
                    SelectFromModel(GradientBoostingClassifier()).fit_transform(iris.data, iris.target)

            类	                所属方式	    说明
            VarianceThreshold	Filter	    方差选择法
            SelectKBest	        Filter	    可选关联系数、卡方校验、最大信息系数作为得分计算的方法
            RFE	                Wrapper	    递归地训练基模型，将权值系数较小的特征从特征集合中消除
            SelectFromModel	    Embedded	训练基模型，选择权值系数较高的特征

    降维：
        当特征选择完成后，可以直接训练模型了，但是可能由于特征矩阵过大，导致计算量大，训练时间长的问题，因此降低特征矩阵维度也是必不可少的
        常见的降维方法除了以上提到的基于L1惩罚项的模型以外，另外还有主成分分析法（PCA）和线性判别分析（LDA），线性判别分析本身也是一个分类模型
        PCA和LDA比较：
            相同：
                PCA和LDA有很多的相似点，其本质是要将原始的样本映射到维度更低的样本空间中
            区别：
                PCA和LDA的映射目标不一样：PCA是为了让映射后的样本具有最大的发散性；而LDA是为了让映射后的样本有最好的分类性能。
                所以说PCA是一种无监督的降维方法，而LDA是一种有监督的降维方法。
        1、PCA
            使用decomposition库的PCA类选择特征的代码如下，
            #主成分分析法，返回降维后的数据
            #参数n_components为主成分数目
            PCA(n_components=2).fit_transform(iris.data)
        2、LDA 线性判别分析
            使用lda库的LDA类选择特征的代码如下，
            #线性判别分析法，返回降维后的数据
            #参数n_components为降维后的维数
            LDA(n_components=2).fit_transform(iris.data, iris.target)
"""


def f1():
    """
        主要是实现上面介绍的一些方法
    """
    iris = load_iris()
    print(StandardScaler().fit_transform(iris.data))
    print("=="*64)

    print(MinMaxScaler().fit_transform(iris.data))
    print("=="*64)

    print(Binarizer(threshold=3.0).fit_transform(iris.data))
    print("=="*64)

    # sparse=False 不产生稀疏矩阵，
    print(OneHotEncoder(sparse=False).fit_transform(iris.target.reshape((-1, 1))))
    print("=="*64)

    """
    归一化，对行进行处理
    若为l1时，样本各个特征值除以各个特征值的绝对值之和
    若为l2时，样本各个特征值除以各个特征值的平方之和
    若为max时，样本各个特征值除以样本中特征值最大的值
    """
    print(Normalizer(norm='l1').fit_transform(iris.data))
    print("=="*64)


def f2():
    iris = load_iris()

    print(np.vstack((np.array([np.nan, np.nan, np.nan, np.nan]), iris.data)))
    print("=="*64)

    # 空值填充
    # missing_values : integer or "NaN", optional (default="NaN")
    # 参数strategy为缺失值填充方式，默认为mean（均值）
    print(Imputer().fit_transform(np.vstack((np.array([np.nan, np.nan, np.nan, np.nan]), iris.data))))
    print("=="*64)

    # 常见的数据变换有基于多项式的、基于指数函数的、基于对数函数的，也可以自定义函数
    print(FunctionTransformer(np.log1p).fit_transform(iris.data))
    print("=="*64)










if __name__ == '__main__':
    #f1()
    f2()
