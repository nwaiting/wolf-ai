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

#降维算法 t-SNE
from sklearn.manifold import TSNE
ts=TSNE(2)
reduced_vec=ts.fit_transform()
plt.show(reduced_vec)

#构建词袋模型
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer,TfidfTransformer
vectorizer = CountVectorizer(max_features=1000)
train_data_features = vectorizer.fit_transform().toarray()  #转成词袋模型进行编码

#随机森林
#基于树的模型 不适合用one-hot编码、bag-of-words编码
#用one-hot编码、bag-of-words编码 的数据更适合用LR模型
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators=100)
forest.fit()

#英文中去除标点符号等，re.sub(r'[~a-zA-Z]','',text) 将除了a到z和A到Z以外的词替换成空

#分离训练和测试数据
from sklearn.cross_validation import train_test_split

# 用于保存模型
from sklearn.externals import joblib
joblib.dump()

#svm分类
from sklearn.svm import SVC, SVR
clf = SVC(kernel='rbf', verbose=True)
clf.fit()

from sklearn.feature_selection


# panda 处理 csv 和 excel文件
import pandas as pd
