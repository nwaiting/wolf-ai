## ML - 排序
- **概述：**
>       排序学习是推荐、搜索、广告的核心方法。排序结果的好坏很大程度影响用户体验、广告收入等。
>
>
>       Ranking 模型可以粗略分为基于相关度和基于重要性进行排序的两大类
>       早期基于相关度的模型：
>           通常利用 query 和 doc 之间的词共现特性（如布尔模型）、VSM（如 TFIDF、LSI 等）、概率排序思想（BM25、LMIR 等）等方式
>       基于重要性的模型：
>           利用的是 doc 本身的重要性，如 PageRank、TrustRank 等
>

- **learning to rank介绍：**
>       参考：https://blog.csdn.net/lipengcn/article/details/80373744
>       L2R可以分为三大类：
>           三大类方法主要区别在于损失函数。不同的损失函数导致不同的模型学习过程和输入输出空间
>           (1)、pointwise 类
>               基本框架：
>                   1、输入空间中样本是单个 doc（和对应 query）构成的特征向量
>                   2、输出空间中样本是单个 doc（和对应 query）的相关度
>                   3、假设空间中样本是打分函数
>                   4、损失函数评估单个 doc 的预测得分和真实得分之间差异
>               根据使用的 ML 方法不同，pointwise 类可以进一步分成三类：
>                   基于回归的算法、基于分类的算法，基于有序回归的算法
>               缺点：
>                   1、pointwise 类方法并没有考虑同一个 query 对应的 docs 间的内部依赖性。一方面，导致输入空间内的样本不是 IID 的，违反了 ML 的基本假设，另一方面，没有充分利用这种样本间的结构性。其次，当不同 query 对应不同数量的 docs 时，整体 loss 将会被对应 docs 数量大的 query 组所支配，前面说过应该每组 query 都是等价的
>                   2、损失函数也没有 model 到预测排序中的位置信息。因此，损失函数可能无意的过多强调那些不重要的 docs，即那些排序在后面对用户体验影响小的 doc
>               改进：
>                   Pointwise 类算法也可以再改进，比如在 loss 中引入基于 query 的正则化因子的 RankCosine 方法
>           (2)、pairwise 类
>               基本框架：
>                   1、输入空间中样本是（同一 query 对应的）两个 doc（和对应 query）构成的两个特征向量
>                   2、输出空间中样本是 pairwise preference
>                   3、假设空间中样本是二变量函数
>                   4、损失函数评估 doc pair 的预测 preference 和真实 preference 之间差异
>               pairwise 类方法基本就是使用二分类算法即可
>               使用算法：
>                   经典的算法有 基于 NN 的 SortNet，基于 NN 的 RankNet，基于 fidelity loss 的 FRank，基于 AdaBoost 的 RankBoost，基于 SVM 的 RankingSVM，基于提升树的 GBRank
>           (3)、listwise 类
>               基本框架：
>                   1、输入空间中样本是（同一 query 对应的）所有 doc（与对应的 query）构成的多个特征向量（列表）
>                   2、输出空间中样本是这些 doc（和对应 query）的相关度排序列表或者排列
>                   3、假设空间中样本是多变量函数，对于 docs 得到其排列，实践中，通常是一个打分函数，根据打分函数对所有 docs 的打分进行排序得到 docs 相关度的排列；
>                   4、损失函数分成两类，一类是直接和评价指标相关的，还有一类不是直接相关的。
>
>
>
>

- **Pairwise**
>       Pairwise算法没有聚焦于精确的预测每个文档之间的相关度，主要关心两个文档之间的顺序，相比pointwise的算法更加接近于排序的概念。
>       在Pairwise中，排序算法通常转化为对文档对的分类，分类的结果是哪个文章的相关度更好，学习的目的是较少错误分类的文档对，在完美的模型中，所有的文档对的顺序都被
>           正确的分类。不同于pointwise算法的是，输入的特征是两个文章的特征，这两个文章不是独立的。
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
>       参考：https://medium.com/@yaoyaowd/%E5%B0%8F%E8%B0%88learning-to-rank%E6%A8%A1%E5%9E%8B-21c81eb2c61e   小谈Learning to Rank模型
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
