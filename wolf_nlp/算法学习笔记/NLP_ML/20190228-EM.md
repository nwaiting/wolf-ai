## NLP_ML - ML算法之EM
- **概述：**
>       Hinton（深度学习的缔造者）,Jordan（当世概率图模型的集大成者），他们碰撞的领域EM算法。这个是PCA外，另一个无监督学习的经典。
>       EM算法是一种迭代算法，用于含有隐变量的概率模型参数的极大似然估计，或极大后验概率估计。
>       EM是一种从不完全数据或有数据丢失的数据集(含隐变量)中求解概率模型参数最大似然估计的方法。
>
>       EM应用功能：
>           EM算法可以用于生成模型的非监督学习，生成模型由联合概率分布P(x,y)表示，可以认为非监督学习训练数据是联合概率分布产生的数据。
>           EM算法提供一种近似计算含有隐变量概率模型的极大似然估计的方法。EM算法的最大优点是简单性和普适性。
>
>

- **EM算法**
>
>
>
>
>
>
>
>

- **EM算法应用：**
>       EM算法有很多的应用，最广泛的就是GMM混合高斯模型的参数估计，聚类(K-means聚类)、HMM等。
>
>
>
>

- **GMM高斯混合模型：**
>       一般混合模型可以由任意概率分布密度代替式中的高斯分布密度。
>
>
>
>
>
>
>
>

- **应用经验：**
>       由于EM算法对初始值敏感，所以初始值的选择变得非常重要，常用的方法的选取不同的初值进行迭代，选择最好的
>
>
>
>

- **待续：**
>       参考：统计学习方法 [李航]
>           http://www.csuldw.com/2015/12/02/2015-12-02-EM-algorithms/  EM-最大期望算法
>           http://www.cnblogs.com/jerrylead/archive/2011/04/06/2006936.html    （EM算法）The EM Algorithm
>           https://www.cnblogs.com/jerrylead/archive/2011/04/06/2006924.html   混合高斯模型（Mixtures of Gaussians）和EM算法
>           http://www.sohu.com/a/210551059_473283  EM算法的九层境界：​Hinton和Jordan理解的EM算法
>           https://www.camcard.com/info/l5a32ab19f149bc416b89ba56  EM算法的九层境界：​Hinton和Jordan理解的EM算法
>           https://www.zybuluo.com/zhuanxu/note/988299     EM算法的9重境界之前两重
>           http://www.zfdeqnc.com/content/180731212714053.html
>           https://mp.weixin.qq.com/s?src=11&timestamp=1558944527&ver=1631&signature=CMnFbsI-4ZaKgmJrKjjWkDbPXrFxcUmQ0J2YOFu1BT4KDu3QsNG2*vkWDU8oiVQqg54J8HVUPMs3ytfWJ4dtjDU7t0*6SNKaPQB-5k5wfVr1PLkaHiJ*RrYDOXoX3QO*&new=1
>               EM算法的九层境界：​Hinton和Jordan理解的EM算法
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
