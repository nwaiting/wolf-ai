#coding=utf8

#线性回归
from sklearn.linear_model import LinearRegression

#logistic回归
from sklearn.linear_model.logistic import LogisticRegression, LogisticRegressionCV

# naive_bayes
# 见 D:\opensource\scrapy-work\wolf_nlp\算法学习笔记\NLP汉语自然语言处理原理与实践-读书笔记/20180424-bayes.md
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

#降维算法 t-SNE
from sklearn.manifold import TSNE
ts=TSNE(2)
reduced_vec=ts.fit_transform()
plt.show(reduced_vec)
