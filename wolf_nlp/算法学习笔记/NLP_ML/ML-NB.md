## NLP_ML - NB
- **概述：**
>       NB是一种生成算法，是对特征X的联合特征X进行建模。
>
>
>
>

- **NB算法详解：**
>
>       1、cost函数
>           如下图，NB是一个生成模型
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/pgm_nb_cost_function1.png)
>
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/pgm_nb_cost_function2.png)
>
>       2、优化方法
>
>

- **算法过程：**
>       1、从样本中可以统计出先验分布
>       2、学习条件概率分布
>       3、利用贝叶斯公式得到联合分布
>       4、预测，计算K个类别的条件概率，概率最大的即为对应的类别
>
>
>
>
>
>
>
>

- **NB的优点：**
>       1、NB是一类比较简单的算法，相对于其他算法，NB的参数比较少
>
>
>
>
>

- **NB的缺点：**
>       1、假定特征之间相互独立
>
>
>
>
>
>

- **NB的应用：**
>       在实际应用中，如在sklearn中有3个NB的分类算法类，分别为：
>           1、GaussianNB
>               先验为高斯分布的NB
>               应用在样本特征值大部分是连续值
>           2、MultinormialNB
>               先验为多项式分布的NB
>               应用在样本特征的大部分是多元离散值
>           3、BernoulliNB
>               先验为伯努利的NB
>               应用在样本特征是二元离散值或很稀疏的多元离散值
>


- **待续：**
>       参考：http://www.ruanyifeng.com/blog/2012/10/spelling_corrector.html   贝叶斯推断及其互联网应用（三）：拼写检查
>               这就叫做"拼写检查"（spelling corrector）。有好几种方法可以实现这个功能，谷歌使用的是基于贝叶斯推断的统计学方法。
>               这种方法的特点就是快，很短的时间内处理大量文本，并且有很高的精确度（90%以上）。
>               谷歌的研发总监 Peter Norvig，写过一篇著名的文章，解释这种方法的原理（http://norvig.com/spell-correct.html）
>            https://github.com/hlk-1135/Dictionary     基于贝叶斯算法的拼写检查器
>            http://mindhacks.cn/2008/09/21/the-magical-bayesian-method/   数学之美番外篇：平凡而又神奇的贝叶斯方法
>            https://mp.weixin.qq.com/s/Oxfa6Xvqx5BCO46CMGZB-w  朴素贝叶斯算法的优缺点
>            http://www.cnblogs.com/pinard/p/6069267.html   朴素贝叶斯算法原理小结
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
