## ML - GBDT VS Adaboost
- **概述：**
>       背景：
>           Adaboost
>               英文"Adaptive Boosting"（自适应增强）的缩写，1995提出
>           GB：
>               在AdaBoost发表后不久，Breiman等人发表了<i>Formulate AdaBoost as gradient descent with a special loss function</i>。
>               随后Friedman等人发表了<i>Generalize AdaBoost to Gradient Boosting in order to handle a variety of loss functions</i>。
>               可以说AdaBoost是Gradient Boosting的一个特例或者Gradient Boosting是对AdaBoost进行推广
>
>       GBDT和Adaboost区别：
>           相同：
>               重复选择一个表现一般的模型并且每次基于先前模型表现进行调整
>           不同：
>               Adaboost是通过提升错分数据点的权重来定位模型的不足
>                   AdaBoost用错分数据点来识别问题，通过调整错分数据点的权重来改进模型
>               Gradient Boosting是通过计算梯度来定位模型的不足，因此相比Adaboost，Gradient Boosting可以使用更多种类的目标函数
>                   Gradient Boosting通过负梯度来识别问题，通过计算负梯度来改进模型
>
>       GBDT：
>           模型的训练过程是对一任意可导目标函数的优化过程。通过反复地选择一个指向负梯度方向的函数，该算法可被看做在函数空间里对目标函数进行优化。
>           因此可以认为：
>               Gradient Boosting = Gradient Descent + Boosting
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
>
>
>
>
>

- **待续：**
>       参考：https://www.zhihu.com/question/54626685      机器学习算法中GBDT与Adaboost的区别与联系
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
>
>
