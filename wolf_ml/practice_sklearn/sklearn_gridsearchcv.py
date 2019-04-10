#coding=utf-8


"""
    GridSearchCV：
        返回值：
            clf.best_params_   返回最好的参数
            clf.best_score_  返回最好的测试分数，它的值和 clf.cv_results_['mean_test_score'][dt_grid.best_index_] 是相同的。
            clf.best_index_  返回列表中分数最好的下表
            clf.best_estimator_  返回最好的模型
            grid_scores_     在sklearn 0.18中已经不赞成使用了，用下面的cv_results_来代替
            clf.cv_results_     返回使用交叉验证进行搜索的结果，它本身又是一个字典，里面又有很多内容，我们来看一下上面的clf.cv_results_.keys()里面有什么：
                dict_keys(
                        ['mean_fit_time', 'std_fit_time', 'mean_score_time', 'std_score_time',
                        'param_C', 'param_gamma', 'param_kernel', 'params',
                        'split0_test_score', 'split1_test_score', 'split2_test_score', 'split3_test_score', 'split4_test_score',
                        'mean_test_score', 'std_test_score', 'rank_test_score',
                        'split0_train_score', 'split1_train_score', 'split2_train_score', 'split3_train_score', 'split4_train_score',
                        'mean_train_score', 'std_train_score'] )
                第一类是时间， 第二类是参数， 第三类是测试分数，其中又分为每次交叉验证的参数和统计的参数，第四类是训练分数，其中也分为每次交叉验证的参数和统计的参数
"""

import os
import pandas as pd
import numpy as np
from operator import itemgetter
from sklearn.datasets import load_iris
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC


def main():
    iris = load_iris()
    svc = SVC()
    params = {"C":[1,1.5,2,2.5,3,4], "gamma":[0.125,0.25,0.75,1,2,4]}
    grid = GridSearchCV(svc, param_grid=params, n_jobs=-1, scoring="accuracy", return_train_score=True)
    grid.fit(iris.data, iris.target)

    #得到最好的带参数的模型
    print(grid.best_estimator_)

    print(grid.best_score_)
    print(grid.best_params_)
    #print(grid.cv_results_)

    def report(gscores, n_top=3):
        top_scores = sorted(gscores, key=itemgetter(1), reverse=True)[:n_top]
        for i, score in enumerate(top_scores):
            print("Model with rank: {0}".format(i + 1))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  score.mean_validation_score,
                  np.std(score.cv_validation_scores)))
            print("Parameters: {0}".format(score.parameters))
            print("")
    # The grid_scores_ attribute was deprecated in version 0.18 in favor of the more elaborate cv_results_ attribute
    #print(grid.grid_scores_)
    report(grid.grid_scores_)
    print("=="*64)

    # 输出超参数交叉验证所有结果 !!!!!!

    print(grid.best_index_)
    print(grid.cv_results_["params"][grid.best_index_])
    print("=="*64)
    print(grid.cv_results_["params"])
    #print(grid.cv_results_["mean_test_score"])
    #print(grid.cv_results_["std_test_score"])


    cv_results = pd.DataFrame.from_dict(grid.cv_results_)
    results_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cv_results.csv")
    cv_results.to_csv(results_file, index=0)





if __name__ == '__main__':
    main()
