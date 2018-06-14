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

#英文中去除标点符号等，re.sub(r'[~a-zA-Z]','',text) 将除了a到z和A到Z以外的词替换成空

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


# panda 处理 csv 和 excel文件
import pandas as pd

#plt中文显示的问题
from matplotlib import pyplot as plt
plt.style.use('ggplot') #设置图片显示的主题样式
plt.rcParams['font-sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题















#
