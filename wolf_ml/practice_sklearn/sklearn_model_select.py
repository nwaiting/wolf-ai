#coding=utf-8


"""
sklearn 模型选择和评估：
    模型验证方法如下：
        通过交叉验证得分：model_sleection.cross_val_score(estimator,X)
        对每个输入数据点产生交叉验证估计：model_selection.cross_val_predict(estimator,X)
        计算并绘制模型的学习率曲线：model_selection.learning_curve(estimator,X,y)
        计算并绘制模型的验证曲线：model_selection.validation(estimator,...)
        通过排序评估交叉验证的得分在重要性：model_selection.permutation_test_score(...)

    模型评估方法：
        Estimator对象的score方法
        在交叉验证中使用的scoring参数

    sklearn分类器评估指标总体概况：
        使用sklearn.metric包中的性能度量函数有：
            分类器性能指标
            回归器性能指标
            聚类其性能指标
            两两距离测度

    分类器评估标准：
        准确率：返回被正确分类的样本比例（default）或者数量（normalize=False）
        二元分类问题：
            F值
        多类别多标签分类问题：
            把其中的一类看成是正类，其他所有类看成是负类，每一类都可以看作是正类是都可以产生P，R，F，
            此时，可以按照5中方式来组合每一个类的结果，这5种方式是：macro，weighted，micro，samples，average=None
        Roc曲线:
            TPR\FPR
"""



if __name__ == '__main__':
    main()
