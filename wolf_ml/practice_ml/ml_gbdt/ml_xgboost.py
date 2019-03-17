# coding=utf-8

"""
参考：
    https://blog.csdn.net/han_xiaoyang/article/details/52665396     机器学习系列(12)_XGBoost参数调优完全指南（附Python代码）
        https://blog.csdn.net/sb19931201/article/details/52557382   xgboost入门与实战（原理篇）
        https://blog.csdn.net/sb19931201/article/details/65445514   XGBoost Plotting API以及GBDT组合特征实践
"""

import xgboost as xgb
# from sklearn import cross_validation
# 新的模块sklearn.model_selection，将以前的sklearn.cross_validation, sklearn.grid_search 和 sklearn.learning_curve模块组合到一起
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

x_train = []
y_train = []
x_train,x_test,y_train,y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=10)
dtrain = xgb.DMatrix(x_train, label=y_train)
dtest = xgb.DMatrix(x_test, label=y_test)
params = {'max_depth':2, 'eta':1, 'silent':0, 'objective':'binary:logistic'}
max_round = 10
save_model_path = ""

best_model = xgb.train(params,dtrain,max_round)
best_model.best_iterator
best_model.best_score
joblib.dump(best_model, save_model_path)