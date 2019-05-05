#coding=utf-8

"""
    SVC, LinearSVC, NuSVC区别：
        SVC：
            如果对数据分布没有什么经验，一般使用SVC去分类，这就需要我们选择核函数以及对核函数调参了
        LinearSVC：
            LinearSVC从名字就可以看出，他是线性分类，也就是不支持各种低维到高维的核函数，仅仅支持线性核函数，对线性不可分的数据不能使用
            如果有经验知道数据是线性可以拟合的，那么使用LinearSVC去分类，它们不需要我们去慢慢的调参去选择各种核函数以及对应参数， 速度也快
        NuSVC：
            如果对训练集训练的错误率或者说支持向量的百分比有要求的时候，可以选择NuSVC分类和NuSVR回归。它们有一个参数来控制这个百分比


    SVC参数详解：
        C=1.0,
            float参数 默认值为1.0
            错误项的惩罚系数。C越大，即对分错样本的惩罚程度越大，因此在训练样本中准确率越高，但是泛化能力降低，也就是对测试数据的分类准确率降低。
            相反，减小C的话，容许训练样本中有一些误分类错误样本，泛化能力强。对于训练样本带有噪声的情况，一般采用后者，把训练样本集中错误分类的样本作为噪声。
        kernel='rbf',
            str参数 默认为‘rbf’
                ‘linear’:线性核函数
                ‘poly’：多项式核函数
                ‘rbf’：径像核函数/高斯核
                ‘sigmod’:sigmod核函数
                ‘precomputed’:核矩阵
        degree=3,
            int型参数 默认为3
            这个参数只对多项式核函数有用，是指多项式核函数的阶数n，如果给的核函数参数是其他核函数，则会自动忽略该参数。
        gamma='auto',
            float参数 默认为auto
            核函数系数，只对‘rbf’,‘poly’,‘sigmod’有效
            如果gamma为auto，代表其值为样本特征数的倒数，即1/n_features
        coef0=0.0,
            float参数 默认为0.0
            核函数中的独立项，只有对‘poly’和‘sigmod’核函数有用，是指其中的参数c
        shrinking=True,
            bool参数 默认为True
            是否采用启发式收缩方式
        probability=False,
            bool参数 默认为False
            是否启用概率估计。这必须在调用fit()之前启用，并且会fit()方法速度变慢
        tol=1e-3,
            float参数 默认为1e^-3
            svm停止训练的误差精度
        cache_size=200,
            float参数 默认为200
            指定训练所需要的内存，以MB为单位，默认为200MB
        class_weight=None,
            字典类型或者‘balance’字符串。默认为None
            给每个类别分别设置不同的惩罚参数C，如果没有给，则会给所有类别都给C=1，即前面参数指出的参数C
            如果给定参数‘balance’，则使用y的值自动调整与输入数据中的类频率成反比的权重
        verbose=False,
            bool参数 默认为False
            是否启用详细输出。 此设置利用libsvm中的每个进程运行时设置，如果启用，可能无法在多线程上下文中正常工作。一般情况都设为False，不用管它。
        max_iter=-1,
            int参数 默认为-1
            最大迭代次数，如果为-1，表示不限制
        decision_function_shape='ovr',
            原始的SVM只适用于二分类问题，如果要将其扩展到多类分类，就要采取一定的融合策略，这里提供了三种选择。
            ‘ovo’ 一对一，决策所使用的返回的是（样本数，类别数*(类别数-1)/2）, 
            ‘ovr’ 一对多，返回的是(样本数，类别数)，或者None，就是不采用任何融合策略, 默认是ovr，因为此种效果要比oro略好一点
        random_state=None
            int型参数 默认为None
            伪随机数发生器的种子,在混洗数据时用于概率估计

    SVC的属性：
        svc.n_support_：各类各有多少个支持向量
        svc.support_：各类的支持向量在训练样本中的索引
        svc.support_vectors_：各类所有的支持向量

    参考：https://github.com/lc222/text_classification_AI100   要用于文本分类
        https://blog.csdn.net/qq_35273499/article/details/79163054  知乎多标签文本分类任务
        https://zhuanlan.zhihu.com/p/28923961   知乎看山杯夺冠记
        http://ruder.io/deep-learning-nlp-best-practices/index.html     Deep Learning for NLP Best Practices
        https://nbviewer.jupyter.org/github/SnailDove/github-blog/blob/master/Titanic-0.837.ipynb   Titanic特征处理
        https://nbviewer.jupyter.org/github/SnailDove/github-blog/blob/master/Titanic_with_name_sex_age_and_ticket_features-0.82275.ipynb   Titanic特征处理
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC, LinearSVC, NuSVC, OneClassSVM
from sklearn.metrics import accuracy_score,roc_auc_score
from sklearn.preprocessing import Normalizer,normalize,MinMaxScaler,StandardScaler,scale
from sklearn.datasets import load_svmlight_file
from sklearn import datasets

"""
    OneClassSVM：
        OneClassSVM两个功能：异常值检测、解决极度不平衡数据
        
"""


def load_data():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "train_modified.csv")
    df = pd.read_csv(file_path)
    print(df.ix[:,"Disbursed"].value_counts())
    columns = [x for x in df.columns if x not in ["Disbursed","ID"]]
    X = df.ix[:, columns].values
    y = df.ix[:, "Disbursed"]
    return X,y

def model_fit():
    X,y = load_data()
    svc_model = SVC()
    svc_model.fit(X, y)

    svc_model.predict()
    svc_model.predict_proba()

def model_svm():
    digits = datasets.load_digits()
    model = SVC(C=1.0, gamma='auto')
    model.fit(digits.data[:-1], digits.target)
    res = model.predict(digits.data[:-1])
    print(res)
    print(digits.target)
    print("accuracy=",np.mean(res==digits.target))

def grid_search_params():
    pass


if __name__ == '__main__':
    model_svm()
