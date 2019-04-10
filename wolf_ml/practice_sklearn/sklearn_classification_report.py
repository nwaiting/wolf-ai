#coding=utf-8


"""
    sklearn.metrics.classification_report(y_true, y_pred, labels=None, target_names=None, sample_weight=None, digits=2, output_dict=False)
    参数：
        y_true：1维数组，或标签指示器数组/稀疏矩阵，目标值。
        y_pred：1维数组，或标签指示器数组/稀疏矩阵，分类器返回的估计值。
        labels：array，shape = [n_labels]，报表中包含的标签索引的可选列表。
        target_names：字符串列表，与标签匹配的可选显示名称（相同顺序）。（如果有值的时候，则报告的行索引则为target_names列表的值）
        sample_weight：类似于shape = [n_samples]的数组，可选项，样本权重。
        digits：int，输出浮点值的位数


    classification_report 输出训练报告
        >>> target_names = ['class 0', 'class 1', 'class 2']
        >>> print(classification_report(y_true, y_pred, target_names=target_names))
                      precision    recall  f1-score   support

             class 0       0.50      1.00      0.67         1
             class 1       0.00      0.00      0.00         1
             class 2       1.00      0.67      0.80         3

           micro avg       0.60      0.60      0.60         5
           macro avg       0.50      0.56      0.49         5
        weighted avg       0.70      0.60      0.61         5
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

    print(grid.cv_results_["mean_test_score"])
    print(grid.cv_results_["std_test_score"])
    #print(grid.cv_results_[""])

    cv_results = pd.DataFrame.from_dict(grid.cv_results_)
    results_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cv_results.csv")
    cv_results.to_csv(results_file, index=0)


    """
        得到预测报告：
                     precision    recall  f1-score   support
              0       1.00      1.00      1.00        50
              1       1.00      0.98      0.99        50
              2       0.98      1.00      0.99        50

    avg / total       0.99      0.99      0.99       150

    """
    y_predictions = grid.predict(iris.data)
    reports = classification_report(y_true=iris.target, y_pred=y_predictions)
    print(reports)




if __name__ == '__main__':
    main()
