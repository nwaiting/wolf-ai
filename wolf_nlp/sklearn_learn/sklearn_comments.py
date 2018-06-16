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


# panda 处理 csv 和 excel文件
import pandas as pd

#plt中文显示的问题
from matplotlib import pyplot as plt
plt.style.use('ggplot') #设置图片显示的主题样式
plt.rcParams['font-sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题















#
