## NLP_ML - 性能评估
- **概述：**
>       模型评估分两类：
>           分类模型评估，常用方法有
>               Accurary
>               Precision
>               Recall
>               F1 score
>               ROC Curve：（Receiver Operating Characteristic）
>                   ROC曲线是基于样本的真实类别和预测概率来画的
>                   ROC曲线如何画出来？
>                       真阳性率和假阳性率
>                       可以设置不同的阈值，对所有阈值计算真阳性率和假阳性率，然后就可以做出ROC曲线
>                       都是对同一信号刺激的反应，只不过是在几种不同的判定标准下所得的结果而已
>               PR Curve
>               AUC：（Area Under the Curve）
>                   AUC即ROC曲线下的面积
>                   AUC是一个模型评价指标，只能用于二分类模型的评价。
>                   AUC和logloss比accuracy更常用，因为很多ML对分类问题的结果都是概率，如果预测概率高于阈值则为正类，AUC或者logloss可以避免吧概率转换成类别
>                   注：
>                       AUC对样本类别是否均衡并不敏感，这也是不均衡样本通常用AUC评价分类器性能的一个原因
>
>           回归模型评估，常用方法有
>               MAE：（Mean Absolute Error）
>                   平均绝对误差，又称为l1范数损失
>               MSE：（Mean Squared Error）
>                   平均平方误差，又称为l2范数损失
>
>
>
>

- **性能评估：**
>       常用方法：
>           1、精确率、召回率、F值等
>           2、ROC曲线
>           3、AUC曲线
>               AUC曲线定义为ROC曲线下的面积，这个面积不大于1，越大模型预测越好
>           4、平均绝对误差MAE和平均平方误差MSE
>
>
>

- **性能评估经验：**
>       对于分类器，主要的评价指标有precision，recall，F-score，以及ROC曲线等。
>       在二分类问题中，我们主要关注的是测试集的正样本能否正确分类。当样本不均衡时，比如样本中负样本数量远远多于正样本，
>           此时如果负样本能够全部正确分类，而正样本只能部分正确分类，那么(TP+TN)可以得到很高的值，也就是Accuracy是个较大的值，但是正样本并没有取得良好的分类效果
>
>
>
>
>
>

- **待续：**
>       参考：http://dingby.site/2018/03/07/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E6%80%A7%E8%83%BD%E8%AF%84%E4%BC%B0%E6%8C%87%E6%A0%87/    机器学习性能评估指标
>           https://zhuanlan.zhihu.com/p/25982866   了解ROC曲线下面积，有这篇文章就够了
>           https://www.plob.org/article/12476.html     全面了解ROC曲线（含有PR曲线）
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
