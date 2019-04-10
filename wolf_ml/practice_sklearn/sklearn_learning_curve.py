#coding=utf-8

"""
    sklearn模型调优（判断是否过过拟合及选择参数）
        learning_curve()：这个函数主要是用来判断（可视化）模型是否过拟合的
            主要作用：
                要判定一下当前模型所处状态(欠拟合or过拟合)!!!

            有一个很可能发生的问题是，我们不断地做feature engineering，产生的特征越来越多，用这些特征去训练模型，会对我们的训练集拟合得越来越好，同时也可能在逐步丧失泛化能力，从而在待预测的数据上，表现不佳，也就是发生过拟合问题
            优化方法：
                过拟合：
                    对过拟合而言，通常以下策略对结果优化是有用的：
                        做一下feature selection，挑出较好的feature的subset来做training
                        提供更多的数据，从而弥补原始数据的bias问题，学习到的model也会更准确
                欠拟合：
                    而对于欠拟合而言，我们通常需要更多的feature，更复杂的模型来提高准确度。

                著名的learning curve可以帮我们判定我们的模型现在所处的状态。我们以样本数为横坐标，训练和交叉验证集上的错误率作为纵坐标，两种状态分别如下两张图所示：过拟合(overfitting/high variace)，欠拟合(underfitting/high bias)

            主要通过交叉验证，获取在训练集和测试集上的预测能力
            learning_curve(estimator, X, y, train_sizes=array([0.1, 0.325, 0.55, 0.775, 1. ]), cv=None, scoring=None, exploit_incremental_learning=False, n_jobs=1, pre_dispatch='all', verbose=0)
                参数：
                    estimator：分类器
                    X：训练向量
                    y：目标相对于X分类或者回归
                    train_sizes：训练样本相对的或绝对的数字，这些量的样本将会生成learning curve。
                    cv：确定交叉验证的分离策略（None：使用默认的3-fold cross-validation；integer：确定几折交叉验证）
                    verbose：整型，可选择的。控制冗余：越高，有越多的信息。
                返回值：
                    train_sizes_abs：生成learning curve的训练集的样本数。重复的输入会被删除。
                    train_scores：在训练集上的分数
                    test_scores：在测试集上的分数

        validation_curve()：这个函数主要是用来查看在参数不同的取值下模型的性能，模型的准确率
            validation_curve(estimator, X, y, param_name, param_range, groups=None, cv=’warn’, scoring=None, n_jobs=None, pre_dispatch=’all’, verbose=0, error_score=’raise-deprecating’)
                参数：
                    param_name	要改变的参数的名字，如果当model为SVC时，改变gamma的值，求最好的那个gamma值
                    param_range	给定的参数范围
                返回值：
                    train_scores : array, shape (n_ticks, n_cv_folds)
                        Scores on training sets.
                    test_scores : array, shape (n_ticks, n_cv_folds)
                        Scores on test set.

    使用Cross-Validation时常犯的错误：
        由于实验室许多研究都有用到 evolutionary algorithms（EA）与 classifiers，所使用的 fitness function 中通常都有用到 classifier 的辨识率，然而把cross-validation 用错的案例还不少。
            前面说过，只有 training data 才可以用于 model 的建构，所以只有 training data 的辨识率才可以用在 fitness function 中。
            而 EA 是训练过程用来调整 model 最佳参数的方法，所以只有在 EA结束演化后，model 参数已经固定了，这时候才可以使用 test data。
            那 EA 跟 cross-validation 要如何搭配呢？Cross-validation 的本质是用来估测(estimate)某个 classification method 对一组 dataset 的 generalization error，不是用来设计 classifier 的方法，
            所以 cross-validation 不能用在 EA的 fitness function 中，因为与 fitness function 有关的样本都属于 training set，那试问哪些样本才是 test set 呢？
            如果某个 fitness function 中用了cross-validation 的 training 或 test 辨识率，那么这样的实验方法已经不能称为 cross-validation 了。

        EA 与 k-CV 正确的搭配方法，是将 dataset 分成 k 等份的 subsets 后，每次取 1份 subset 作为 test set，其余 k-1 份作为 training set，
            并且将该组 training set 套用到 EA 的 fitness function 计算中(至于该 training set 如何进一步利用则没有限制)。因此，正确的 k-CV 会进行共 k 次的 EA 演化，
            建立 k 个classifiers。而 k-CV 的 test 辨识率，则是 k 组 test sets 对应到 EA 训练所得的 k 个 classifiers 辨识率之平均值。


    scikit-learn 中的 learning_curve() 函数来生成一个回归模型的学习曲线。不需要我们自己设置验证集，learning_curve() 函数会自己完成这个任务。
        每个特定大小的训练集都会训练一个新的模型。如果你使用了交叉验证，也就是我们在本文中使用的方法，那么每个训练集大小会训练出 k 个不同的模型（k 是交叉验证的次数）。
        为了节省代码的运行时间，将交叉验证设置到 5-10 是比较现实的。

    模型的最好状态：
        为了达到偏差和方差的平衡
        参考：http://studyai.site/2016/10/24/%E6%96%AF%E5%9D%A6%E7%A6%8F%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%20%E7%AC%AC%E5%85%AD%E5%91%A8%20%282%29%E5%81%8F%E5%B7%AEVS%E6%96%B9%E5%B7%AE/
        http://www.idataskys.com/2017/08/15/%E5%88%A9%E7%94%A8scikit-learn%E6%9D%A5%E5%88%86%E6%9E%90%E6%A8%A1%E5%9E%8B%E6%AC%A0%E6%8B%9F%E5%90%88%E5%92%8C%E8%BF%87%E6%8B%9F%E5%90%88%E9%97%AE%E9%A2%98/

    模型验证的五种方法：
        一、通过交叉验证计算得分（model_selection.cross_val_score(estimator,x)）
        二、对每一个输入数据点产生交叉验证估计（model_selection.cross_val_predict(estimator,x)）
        三、计算绘制模型的学习率曲线（model_selection.learning_curve(estimator,x,y)）
        四、计算并绘制模型验证曲线（model_selection.validation_curve(estimator…)）
        五、通过排序评估交叉验证得分的重要性（model_selection.permatation_test_score()）
        参考：http://studyai.com/article/c8a5e7dd
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve, validation_curve, cross_val_score


def f1():
    X,y = datasets.load_digits(return_X_y=True)
    train_size,train_score,test_score = learning_curve(RandomForestClassifier(), X, y, train_sizes=[0.1,0.2,0.4,0.6,0.8,1], cv=10, scoring="accuracy")
    print(train_size)
    print("=="*64)
    print(train_score)
    print("=="*64)
    print(test_score)
    print("=="*64)
    train_error = 1 - np.mean(train_score, axis=1)
    test_error = 1 - np.mean(test_score, axis=1)
    plt.plot(train_size, train_error, "o-", color="r", label="training")
    plt.plot(train_size, test_error, "o-", color='g', label="test")
    plt.xlabel("train size")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def f2():
    X,y = datasets.load_digits(return_X_y=True)
    param_list = [10,20,40,80,120,160]
    train_score,test_score = validation_curve(RandomForestClassifier(), X, y, param_name="n_estimators", param_range=param_list, cv=10, scoring="accuracy")
    train_score = np.mean(train_score, axis=1)
    test_score = np.mean(test_score, axis=1)
    plt.plot(param_list, train_score, 'o-', color='r', label="training")
    plt.plot(param_list, test_score, 'o-', color='g', label="testing")
    plt.legend(loc="best")
    plt.xlabel("number of tree")
    plt.ylabel("accuracy")
    plt.show()


def f3():
    rfc = RandomForestClassifier()
    X,y = datasets.load_digits(return_X_y=True)
    res = cross_val_score(rfc, X, y, cv=5)
    print(res)

if __name__ == '__main__':
    #f1()
    #f2()
    f3()
