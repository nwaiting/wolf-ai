# coding=utf-8

"""
参考：
    https://blog.csdn.net/han_xiaoyang/article/details/52665396     机器学习系列(12)_XGBoost参数调优完全指南（附Python代码）
        https://blog.csdn.net/sb19931201/article/details/52557382   xgboost入门与实战（原理篇）
        https://blog.csdn.net/sb19931201/article/details/65445514   XGBoost Plotting API以及GBDT组合特征实践
        https://snaildove.github.io/2018/10/02/get-started-XGBoost/     XGBoost原理和底层实现剖析（非常详细！！！）
"""
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from xgboost import plot_importance
import lightgbm as lgb
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

from sklearn.ensemble import RandomForestClassifier
# from sklearn import cross_validation
# 新的模块sklearn.model_selection，将以前的sklearn.cross_validation, sklearn.grid_search 和 sklearn.learning_curve模块组合到一起
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn import metrics

"""
    GridSearchCV参数
        cv
            交叉验证参数，默认None，使用三折交叉验证。指定fold数量，默认为3，也可以是yield训练/测试数据的生成器。
        iid
            默认True,为True时，默认为各个样本fold概率分布一致，误差估计为所有样本之和，而非各个fold的平均
        verbose
            日志冗长度，int：冗长度，0：不输出训练过程，1：偶尔输出，>1：对每个子模型都输出

    返回结果：
        grid_scores_：给出不同参数情况下的评价结果
        best_params_：描述了已取得最佳结果的参数的组合
        best_score_：成员提供优化过程期间观察到的最好的评分
"""

def load_data():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "train_modified.csv")
    df = pd.read_csv(file_path)
    print(df.ix[:,"Disbursed"].value_counts())
    columns = [x for x in df.columns if x not in ["Disbursed","ID"]]
    X = df.ix[:, columns].values
    y = df.ix[:, "Disbursed"]
    return X,y

def load_data_df():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "train_modified.csv")
    df = pd.read_csv(file_path)
    print(df.ix[:,"Disbursed"].value_counts())
    columns = [x for x in df.columns if x not in ["Disbursed","ID"]]
    X = df.ix[:, columns]
    y = df.ix[:, "Disbursed"]
    return X,y

def find_best_rf(n_estimators=60, min_samples_leaf=20, max_features="sqrt", random_state=10, oob_score=True,min_samples_split=100,max_depth=8):
    """
    最大特征数max_features
    再划分所需最小样本数min_samples_split
    叶子节点最少样本数min_samples_leaf
    决策树最大深度max_depth
    弱学习器迭代次数n_estimators
    """
    rf_model = RandomForestClassifier(oob_score=oob_score,
                                    n_estimators=n_estimators,
                                    min_samples_leaf=min_samples_leaf,
                                    min_samples_split = min_samples_split,
                                    max_features=max_features,
                                    random_state=random_state,
                                    max_depth=max_depth)
    X,y = load_data()
    rf_model.fit(X, y)
    y_prob = rf_model.predict_proba(X)[:,1]
    print("oob score={0},auc_score={1}".format(rf_model.oob_score_, metrics.roc_auc_score(y, y_prob)))
    print("=="*64)

def decision_tree_rf():
    find_best_rf(oob_score=True, random_state=10)

    X,y = load_data()
    # 得到最佳迭代次数
    params = {"n_estimators":list(range(10,71,10))}
    grid1 = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100, min_samples_leaf=20, max_depth=8, max_features="sqrt", random_state=10),
                        param_grid=params,
                        scoring="roc_auc",
                        cv=5,
                        n_jobs=-1)
    grid1.fit(X, y)
    #print(grid1.grid_scores_)
    print(grid1.cv_results_)
    print(grid1.best_params_)
    print(grid1.best_score_)
    print("=="*64)

    # 得到最优最大深度和划分所需最小样本数
    params2 = {"max_depth":list(range(3,14,2)), "min_samples_split":list(range(50,201, 20))}
    grid2 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=60, min_samples_leaf=20, max_features="sqrt", random_state=10, oob_score=True),
                        param_grid=params2,
                        scoring="roc_auc",
                        iid=False,
                        cv=5,
                        n_jobs=-1)
    grid2.fit(X, y)
    #print(grid2.grid_scores_)
    print(grid2.cv_results_)
    print(grid2.best_params_)
    print(grid2.best_score_)
    print("=="*64)


    find_best_rf(oob_score=True, random_state=10, n_estimators=60, max_depth=13, min_samples_split=110)
    print("=="*64)
    # 内部节点再划分所需最小样本数min_samples_split，我们暂时不能一起定下来，因为这个还和决策树其他的参数存在关联
    # 对内部节点再划分所需最小样本数min_samples_split和叶子节点最少样本数min_samples_leaf一起调参
    params3 = {"min_samples_split":list(range(80,150,20)), "min_samples_leaf":list(range(10,60,10))}
    grid3 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=60, max_depth=13, max_features="sqrt", oob_score=True, random_state=10),
                        param_grid=params3,
                        scoring="roc_auc",
                        iid=False,
                        cv=5,
                        n_jobs=-1)
    grid3.fit(X, y)
    #print(grid3.grid_scores_)
    print(grid3.cv_results_)
    print(grid3.best_params_)
    print(grid3.best_score_)
    print("=="*64)

    find_best_rf(oob_score=True, random_state=10, n_estimators=60, max_depth=13, min_samples_split=120, min_samples_leaf=20)


def decision_tree_xgb():
    """
    xgb参数：
        booster
            [default=gbtree](General Parameters)
            使用哪种助推器，可以是gbtree，gblinear或dart。gbtree和dart使用基于树的模型，而gblinear使用线性函数。
            tree booster的表现远远胜过linear booster，所以linear booster很少用到
        silent
            [默认0]
            当这个参数值为1时，静默模式开启，不会输出任何信息。一般这个参数就保持默认的0，因为这样能帮我们更好地理解模型。
        nthread
            [默认值为最大可能的线程数]
            这个参数用来进行多线程控制，应当输入系统的核数。如果你希望使用CPU全部的核，那就不要输入这个参数，算法会自动检测它。

    booster参数：
        max_depth
            [默认 6]
            最大深度。这个值也是用来避免过拟合的。max_depth 越大，模型会学到更具体更局部的样本。需要使用 CV 函数来进行调优。 典型值：3-10
        eta
            [默认 0.3]
            和 GBM 中的 learning rate 参数类似。 通过减少每一步的权重，可以提高模型的稳定性。 典型值为 0.01-0.2
            和 gradiant boosting 中的 learning rate 参数类似。通过减少每一步的权重，可以提高模型的稳定性。 典型值为 0.01-0.2
        min_child_weight
            [默认 1]
            决定最小叶子节点样本权重和。和 GBM 的 min_child_leaf 参数类似，但不完全一样。当它的值较大时，可以避免模型学习到局部的特殊样本。但是如果这个值过高，会导致欠拟合。
            这个参数需要使用 CV 来调整。
        max_leaf_nodes
            树上最大的节点或叶子的数量。 可以替代 max_depth 的作用。因为如果生成的是二叉树，一个深度为 n 的树最多生成 n2 个叶子。 如果定义了这个参数，GBM 会忽略 max_depth 参数
        gamma
            [默认 0]
            在节点分裂时，只有分裂后损失函数的值下降了，才会分裂这个节点。Gamma 指定了节点分裂所需的最小损失函数下降值。
            这个参数的值越大，算法越保守。这个参数的值和损失函数息息相关，所以是需要调整的
        max_delta_step
            [默认 0]
            这参数限制每棵树权重改变的最大步长。如果这个参数的值为 0，那就意味着没有约束。如果它被赋予了某个正值，那么它会让这个算法更加保守。
            通常，这个参数不需要设置。但是当各类别的样本十分不平衡时，它对逻辑回归是很有帮助的。 这个参数一般用不到，但是你可以挖掘出来它更多的用处。
        subsample
            [默认 1]
            这个参数控制对于每棵树，随机采样的比例。 减小这个参数的值，算法会更加保守，避免过拟合。但是，如果这个值设置得过小，它可能会导致欠拟合。 典型值：0.5-1
        colsample_bytree
            [默认 1]
            和 GBM 里面的 max_features 参数类似。用来控制每棵随机采样的列数的占比 (每一列是一个特征)。 典型值：0.5-1
        colsample_bylevel
            [默认 1]
            用来控制树的每一级的每一次分裂，对列数的采样的占比。 我个人一般不太用这个参数，因为 subsample 参数和 colsample_bytree 参数可以起到相同的作用。但是如果感兴趣，可以挖掘这个参数更多的用处。
        lambda
            [默认 1]
            权重的 L2 正则化项。(和 Ridge regression 类似)。 这个参数是用来控制 XGBoost 的正则化部分的。
            虽然大部分数据科学家很少用到这个参数，但是这个参数在减少过拟合上还是可以挖掘出更多用处的。
        alpha
            [默认 1]
            权重的 L1 正则化项。(和 Lasso regression 类似)。 可以应用在很高维度的情况下，使得算法的速度更快。
        scale_pos_weight
            [默认 1]
            在各类别样本十分不平衡时，把这个参数设定为一个正值，可以使算法更快收敛

    目标参数：
        objective
            [默认 reg:linear]
            这个参数定义需要被最小化的损失函数
            binary:logistic 二分类的逻辑回归，返回预测的概率 (不是类别)
            multi:softmax 使用 softmax 的多分类器，返回预测的类别 (不是概率)，在这种情况下，你还需要多设一个参数：num_class(类别数目)
            multi:softprob 和 multi:softmax 参数一样，但是返回的是每个数据属于各个类别的概率
        eval_metric
            [默认值取决于 objective 参数的取值]
            对于回归问题，默认值是 rmse，对于分类问题，默认值是 error
            rmse 均方根误差、
            mae 平均绝对误差、
            logloss 负对数似然函数值、
            error 二分类错误率 (阈值为 0.5)、
            merror 多分类错误率、
            mlogloss 多分类logloss损失函数、
            auc 曲线下面积
        seed
            随机数的种子设置它可以复现随机数据的结果，也可以用于调整参数
    """
    params = {"max_depth":6, "eta":0.05, "nthread":8, "learning_rate":0.05, "objective":"binary:logistic", "eval_metric":"auc"}
    cv_fold = None
    # 设置early_stopping_rounds=10，当logloss在10轮迭代之内，都没有提升的话，就stop。如果说eval_metric有很多个指标，那就以最后一个指标为准。经验上，选择early_stopping_rounds = 10%*(总迭代次数)
    early_stop_round = 200
    X,y = load_data()
    if cv_fold:
        dtrain = xgb.DMatrix(X, label=y)
        xgb_cvmodel = xgb.cv(params, dtrain, num_boost_round=5000,
                        nfold=cv_fold, seed=10, verbose_eval=True,
                        metrics="auc", early_stopping_rounds=early_stop_round,
                        show_stdv=False)
        print(xgb_cvmodel)
        #最优迭代次数
        best_round = xgb_cvmodel.shape[0]
        #最好的auc
        best_auc = xgb_cvmodel["test-auc-mean"].values[-1]
        best_model = xgb.train(params, dtrain, best_round)
        best_model.predict(dtest)
    else:
        X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)
        watchlist = [(dtrain, "train"),(dtest, "valid")]
        max_round = 200
        xgb_model = xgb.train(params, dtrain, max_round, evals=watchlist, early_stopping_rounds=early_stop_round)
        print("best iter={0}, best score={1}".format(xgb_model.best_iteration, xgb_model.best_score))
        dtrain_predictions = xgb_model.predict(dtrain)
        X_test = xgb.DMatrix(X_test)
        dtest_predictions = xgb_model.predict(X_test)
        # 这种计算分数会报错，因为一个是类别一个是概率
        #print("accuracy ", metrics.accuracy_score(y_test, dtest_predictions))
        print("accuracy ", metrics.accuracy_score(y_test, dtest_predictions.round()))

        # 获取特征重要性
        # model.get_score(importance_type='weight')
        # 或者 model.booster().get_score(importance_type='weight')
        importances = xgb_model.get_fscore()
        print(importances)
        importances = sorted(importances.items(), key=lambda x:x[1], reverse=True)
        print(importances[:30])
        #dtrain_predprob = xgb_model.predict_proba(dtrain)[:,1]
        #print("accuracy ", metrics.accuracy_score(y_train, dtrain_predictions))
        #print("auc score ", metrics.roc_auc_score(y, dtrain_predprob))

def model_fit(alg, xtrain,ytrain,xtest,ytest,user_traincv=True, cv_fold=5, early_stop_round=50):
    if user_traincv:
        xgb_param = alg.get_xgb_params()
        xgb_dtrain = xgb.DMatrix(xtrain, label=ytrain)
        xgb_dtest = xgb.DMatrix(xtest, label=ytest)
        cv_result = xgb.cv(xgb_param, xgb_dtrain, num_boost_round=alg.get_params()["n_estimators"], nfold=cv_fold,
                            metrics="auc", early_stopping_rounds=early_stop_round, show_stdv=False)
        alg.set_params(n_estimators=cv_result.shape[0])
    alg.fit(xtrain, ytrain, eval_metric="auc")
    train_predictions = alg.predict(xtrain)
    # predict_proba返回的是一个 n 行 k 列的数组， 第i行第j列上的数值是模型预测第i个预测样本为某个标签的概率，并且每一行的概率和为1
    train_predprob = alg.predict_proba(xtrain)[:,1]
    print("model reports:===============================")
    print("accuarcy:{0}".format(metrics.accuracy_score(ytrain, train_predictions)))
    print("auc score:{0}".format(metrics.roc_auc_score(ytrain, train_predprob)))

    test_predictions = alg.predict(xtest)
    test_predprob = alg.predict_proba(xtest)[:,1]
    print("predict test data result:==============================")
    print("accuracy:{0}".format(metrics.accuracy_score(ytest, test_predictions)))
    print("auc score:{0}".format(metrics.roc_auc_score(ytest, test_predprob)))

    #feat_imp = pd.Series(alg.booster().get_fscore()).sort_values(ascending=False)
    print(alg.feature_importances_)
    feat_imp = pd.Series(alg.feature_importances_).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title="Feature Important")
    plt.ylabel("Feature Important score")
    plt.show()


def decision_tree_xgb_sklearn():
    """
        方法1：
        xgb_model = xgb.train()
        xgb_model.get_fscore()

        方法2：
        model = XGBClassifier()
        model.fit(X, y)
        # feature importance
        print(model.feature_importances_)

        参考：https://github.com/aarshayj/Analytics_Vidhya/blob/master/Articles/Parameter_Tuning_XGBoost_with_Example/XGBoost%20models.ipynb
    """
    X,y = load_data_df()
    xtrain,xtest,ytrain,ytest = train_test_split(X, y, test_size=0.2, random_state=10, shuffle=True)
    flag = 9
    if flag == 1:
        params1 = {"max_depth":list(range(3,8,1)), "min_child_weight":list(range(1,6,2))}
        grid1 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=140, max_depth=5, min_child_weight=1, gamma=0, subsample=0.8,
                                                    colsample_bytree=0.8, objective="binary:logistic", scale_pos_weight=1, seed=10),
                            param_grid=params1,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5)
        grid1.fit(X,y)
        print(grid1.grid_scores_)
        print(grid1.best_params_)
        print(grid1.best_score_)
        # {'max_depth': 4, 'min_child_weight': 3} 0.82109573488313
    if flag == 2:
        params2 = {"min_child_weight":list(range(2,6,1))}
        grid2 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=140, max_depth=4, min_child_weight=1, gamma=0, subsample=0.8,
                                                    colsample_bytree=0.8, objective="binary:logistic", scale_pos_weight=1, seed=10),
                            param_grid=params2,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5)
        grid2.fit(X,y)
        print(grid2.grid_scores_)
        print(grid2.best_params_)
        print(grid2.best_score_)
        # {'min_child_weight': 3} 0.82109573488313
    if flag == 3:
        params3 = {"min_child_weight":list(range(3,10,1))}
        grid3 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=140, max_depth=4, min_child_weight=1, gamma=0, subsample=0.9,
                                                    colsample_bytree=0.9, objective="binary:logistic", scale_pos_weight=1, seed=10),
                            param_grid = params3,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5)
        grid3.fit(X, y)
        print(grid3.grid_scores_)
        print(grid3.best_params_)
        print(grid3.best_score_)
        # {'min_child_weight': 3} 0.81962890625
    if flag == 4:
        params4 = {"gamma":[i/10 for i in range(5)]}
        grid4 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=140, max_depth=4, min_child_weight=3, gamma=0, subsample=0.9,
                                                    colsample_bytree=0.9, objective="binary:logistic", scale_pos_weight=1, seed=10),
                            param_grid=params4,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5
                            )
        grid4.fit(X,y)
        print(grid4.grid_scores_)
        print(grid4.best_params_)
        print(grid4.best_score_)
        # {'gamma': 0.0} 0.81962890625
    if flag == 5:
        params5 = {"n_estimators":list(range(100, 150, 10))}
        grid5 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=140, max_depth=4, min_child_weight=3, gamma=0, subsample=0.9,
                                                    colsample_bytree=0.9, objective="binary:logistic", scale_pos_weight=1, seed=10),
                            param_grid=params5,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5
                            )
        grid5.fit(X, y)
        print(grid5.grid_scores_)
        print(grid5.best_params_)
        print(grid5.best_score_)
        # {'n_estimators': 130} 0.8196741615853659

    #alg = XGBClassifier(n_estimators=140, learning_rate=0.1, max_depth=4, min_child_weight=3, gamma=0, subsample=0.9, colsample_bytree=0.9, objective="binary:logistic",
    #                    scale_pos_weight=1, seed=10)
    #model_fit(alg, xtrain, ytrain, xtest, ytest)

    if flag == 6:
        params6 = {"subsample":[i/10.0 for i in list(range(6,10))],"colsample_bytree":[i/10.0 for i in list(range(6,10))]}
        grid6 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1,n_estimators=140,max_depth=4,min_child_weight=3,gamma=0,
                                                    subsample=1,colsample_bytree=1,objective="binary:logistic",scale_pos_weight=1,seed=10),
                            param_grid=params6,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5)
        grid6.fit(X,y)
        print(grid6.grid_scores_)
        print(grid6.best_params_)
        print(grid6.best_score_)
        # {'colsample_bytree': 0.8, 'subsample': 0.8} 0.82109573488313

    if flag == 7:
        params7 = {"subsample":[i/100.0 for i in list(range(75,90,5))], "colsample_bytree":[i/100.0 for i in list(range(75,90,5))]}
        grid7 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1,n_estimators=140, max_depth=4,min_child_weight=3,gamma=0,
                                                    subsample=1, colsample_bytree=1, objective="binary:logistic", scale_pos_weight=1,seed=10),
                            param_grid=params7,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5)
        grid7.fit(X, y)
        print(grid7.grid_scores_)
        print(grid7.best_params_)
        print(grid7.best_score_)
        # {'colsample_bytree': 0.8, 'subsample': 0.8} 0.82109573488313

    if flag == 8:
        params8 = {"reg_alpha":[i/10.0 for i in list(range(6))]+[0.001,0.005,0.05,0.01]}
        grid8 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1,n_estimators=140,max_depth=4,min_child_weight=3,gamma=0,
                                                    subsample=0.8,colsample_bytree=0.8,objective="binary:logistic",scale_pos_weight=1,seed=10),
                            param_grid=params8,
                            scoring="roc_auc",
                            n_jobs=-1,
                            iid=False,
                            cv=5)
        grid8.fit(X,y)
        print(grid8.grid_scores_)
        print(grid8.best_params_)
        print(grid8.best_score_)
        # {'reg_alpha': 0.1} 0.8236574250508131
    alg = XGBClassifier(n_estimators=140, learning_rate=0.1, max_depth=4, min_child_weight=3, gamma=0, subsample=0.9, colsample_bytree=0.9, objective="binary:logistic",
                        scale_pos_weight=1, seed=10, reg_alpha=0.1)
    model_fit(alg, xtrain, ytrain, xtest, ytest)


def test_xgboost():
    #iris = load_iris()
    #X,y = iris.data,iris.target
    X,y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234565) # 数据集分割

    # 算法参数
    params = {
        'booster': 'gbtree',
        'objective': 'multi:softmax',
        'num_class': 3,
        'gamma': 0.1,
        'max_depth': 6,
        'lambda': 2,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 3,
        'silent': 1,
        'eta': 0.1,
        'seed': 1000,
        'nthread': 4,
    }

    plst = params.items()
    dtrain = xgb.DMatrix(X_train, y_train) # 生成数据集格式
    num_rounds = 500
    model = xgb.train(plst, dtrain, num_rounds) # xgboost模型训练

    # 对测试集进行预测
    dtest = xgb.DMatrix(X_test)
    y_pred = model.predict(dtest)

    # 计算准确率
    print(y_pred)
    accuracy = accuracy_score(y_test,y_pred)
    print("accuarcy: %.2f%%" % (accuracy*100.0))

    # 显示重要特征
    plot_importance(model)
    plt.show()

if __name__ == '__main__':
    #test_xgboost()
    #decision_tree_xgb()
    decision_tree_xgb_sklearn()
    #decision_tree_rf()
