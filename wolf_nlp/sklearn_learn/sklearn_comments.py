#coding=utf8

#线性回归
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso

#logistic回归
from sklearn.linear_model.logistic import LogisticRegression, LogisticRegressionCV

# naive_bayes
# 见 D:\opensource\scrapy-work\wolf_nlp\算法学习笔记\NLP汉语自然语言处理原理与实践-读书笔记/20180424-bayes.md
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
# 会出现共线性问题
# 重复的词，多项式（出现多次），伯努利（出现1次），混合模型（计算句子概率时计算1次，统计时统计多次）

#降维算法 t-SNE PCA
# tsne保留下的属性信息，更具代表性，也即最能体现样本间的差异
# tsne运行极慢，PCA则相对较快
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
data_pca = PCA(n_components=50).fit_transform(data)
data_pca_tsne = TSNE(n_components=2).fit_transform(data_pca)

#构建词袋模型
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer,TfidfTransformer
vectorizer = CountVectorizer(max_features=1000, ngram_range=(1, 2, 3))  #单个词、2元词组、3元词组全部获取，生成词袋模型
train_data_features = vectorizer.fit_transform().toarray()  #转成词袋模型进行编码

#数据预处理
#数据的幅度缩放 标准化
from sklearn.preprocessing import MinMaxScaler,StandardScaler,scale
#独热向量编码
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import minmax_scale
minmax_scale.fit_transform()

#特征选择
#SelectKBest：选出k个， SelectPercentile：选出百分比
from sklearn.feature_selection import SelectKBest, SelectPercentile, GenericUnivariateSelect,RFE

#随机森林
#基于树的模型 不适合用one-hot编码、bag-of-words编码
#用one-hot编码、bag-of-words编码 的数据更适合用LR模型
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators=100)
forest.fit()

#分离训练和测试数据
from sklearn.cross_validation import train_test_split
train_test_split(X,y, test_size=0.33, random_state=1234) #random_state随机选取33%样本作为测试集合

#调节超参数的使用方法，会给出一组候选参数，然后进行交叉验证选择最好的一组参数进行建模
from sklearn.model_selection import GridSearchCV

# 用于保存模型
from sklearn.externals import joblib
joblib.dump()

#svm分类
from sklearn.svm import SVC, SVR
clf = SVC(kernel='rbf', verbose=True)
clf.fit()

from sklearn.svm import LinearSVC, SVR（regression）
#嵌入型特征选择
from sklearn.feature_selection import SelectFromModel
lsvc = LinearSVC(C=0.01, penalty='l1', dual=False).fit(X,y) #选择l1作为正则化
model = SelectFromModel(lsvc, prefit=True)
model.transform(X)

"""
数据归一化、标准化、正则化
    scale或者StandardScaler 两个方法进行标准化，去除均值和方差缩放
        公式为：(X-mean)/std  计算时对每个属性/每列分别进行
        将数据按期属性（按列进行）减去其均值，并处以其方差。得到的结果是，对于每个属性/每列来说所有数据都聚集在0附近，方差为1。

    MinMaxScaler缩放数据到指定区间内（通常在0-1区间）
        目的和作用：
            对于方差非常小的属性可以增强其稳定性
            维持稀疏矩阵中为0的条目

    Normalizer或者normalize，正则化的过程就是将每个样本缩放到单位范数（每个样本的范数为1），如果后面要使用如二次型（点积）或者其他核方法计算两个样本之间的相似度这个方法会很有用
    Normalizer主要思想：对每个样本计算其p范数，然后对给样本中每个元素除以该范数，这样处理的结果是使得每个处理后样本p范数等于1
    改方法主要应用于文本分类和聚类中。例如对于两个tf-idf向量的l2-norm进行点积，就可以得到这两个向量的余弦相似性

"""

from sklearn.preprocessing import scale, StandardScaler, MinMaxScaler, Normalizer, normalize


"""
    fit和fit_transform区别：
        fit只是数据拟合
        fit_transform特征化

        fit(X)：传一个参数是无监督的学习算法，如降维、特征提取、标准化
        fit(X,y)：传两个参数是有监督学习
"""

"""
    网格搜索参数详解：
        sklearn.model_selection.GridSearchCV(estimator, param_grid, scoring=None, fit_params=None,n_jobs=1, iid=True,
        refit=True, cv=None, verbose=0, pre_dispatch=‘2*n_jobs’, error_score=’raise’, return_train_score=’warn’)
        参数：
            estimator：分类器
            param_grid：需要最优化的参数的取值
                    pagram_grid = {
                            'learning_rate':[0.01,0.02,0.05,0.1],
                            'n_estimators':[1000,2000,3000,4000,5000], #树的数量
                            'num_leaves':[128,1024] #树的深度 7,10
                        }
            scoring：模型评价标准，默认为None，这时需要使用score函数，或者如scoring='roc_auc'，
                    根据所选模型不同，评价标准不同，字符串函数名，或者是可条用对象
                    需要其函数签名如：scorer(estimator,X,y)；如果是None，则使用estimator的误差估计函数
            verbose=0，scoring=None
                    verbose：日志冗长度，0：不输出训练过程，1：偶尔输出，>1：对每个子模型都输出
            pre_dispatch:
                    指定总共分发的并行任务数，当n_job大于1时，数据将在每个运行点进行复制，这可能导致OOM，而设置pre_dispatch参数，则可以预先划分总共的job数量
                    是数据最多被复制pre_dispatch次
            return_train_score:
                    如果为False，cv_results_属性将不包括训练分数
            refit：
                    默认为True，程序将会以交叉验证训练集得到的最佳参数，重新对所有可用的训练集和开发集进行，作为最终用于性能评估的最佳模型参数。即在搜索参数结束后，用最佳参数结果再次fit一遍全部数据集
            iid：
                    默认为True，为True时，默认为各个样本fold概率分布一直，误差估计为所有样本之和，而非各个fold的平均
            cv：
                    交叉验证参数，默认None，使用三折交叉验证，指定fold数量，默认为3，也可以是yield训练/测试数据的生成器


            gsearch1 = sklearn.model_selection.GridSearchCV()
            gsearch1.fit(X,y)
            gsearch1.grid_scores_,
            gsearch1.best_params_,
            gsearch1.best_score_

    如果有transform，使用Pipeline简化系统搭建流程，将transform与分类器串联起来
        pipeline= Pipeline([("features", combined_features), ("svm", svm)])
        param_grid= dict(features__pca__n_components=[1, 2, 3],
                          features__univ_select__k=[1,2],
                          svm__C=[0.1, 1, 10])

        grid_search= GridSearchCV(pipeline, param_grid=param_grid, verbose=10)
        grid_search.fit(X,y)
        print(grid_search.best_estimator_)

"""

"""
    patsy是一个Python包，用于描述统计模型（statistical models）（特别是，线性模型或者有线性成分的模型），同时也用于构建设计矩阵（design matrices）
        from patsy import dmatrices
        举例来说，如果我们有变量y和变量 x，a，b。我们想求出变量y与变量x,a,b之间的回归关系，其中变量a和b之间存在着交互作用，
        则公式可写为：patsy.dmatrices("y ~ x + a + b + a:b", data)
"""












# panda 处理 csv 和 excel文件
import pandas as pd

#plt中文显示的问题
from matplotlib import pyplot as plt
plt.style.use('ggplot') #设置图片显示的主题样式
plt.rcParams['font-sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

#用于显示图例，有多个axes图例时，把他们放在一起
#参数：best 自适应模式
plt.legend(loc='best')













#
