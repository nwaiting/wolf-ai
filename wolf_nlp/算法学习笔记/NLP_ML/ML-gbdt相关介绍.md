## NLP_ML - GBDT介绍
- **概述：**
>       本文主要讲解 lightgbm、xgboost、GBDT、Adaboost相关介绍
>
>       boosting：
>           是一族可将弱学习器提升为强学习器的算法。
>           工作机制：
>               先从初始训练集训练处一个基分类器，在根据基分类器的表现对训练样本分布进行调整，使得先前基学习器做错的训练样本在后续会得到更多关注。
>               然后基于调整后的样本分类来训练下一个基学习器。直到基学习器数目达到预先指定的值T，然后将这T个基学习器进行加权结合。
>
>

- **boosting和bagging：**
>       bagging主要关注降低方差，因此它在不剪枝的决策树、神经网络等学习器上效用更为明显
>       boosting主要关注降低偏差，因此boosting能基于泛化性能相对弱的学习器构建出很强的集成
>
>
>
>       注：
>           泛化误差：
>               可以分解为两部分，偏差（bias）和方差（variance）
>               偏差：
>                   指算法的期望预测与真实预测之间的偏差程度，反应了模型本身的拟合能力
>               方差：
>                   度量了同等大小的训练集的变动导致学习性能的变化，刻画了数据扰动所导致的影响
>
>           偏差和方差对模型的影响：
>               当模型越复杂时，拟合的程度就越高，模型的训练偏差就越小。但此时如果换一组数据可能模型的变化就会很大，即模型的方差很大。所以模型过于复杂的时候会导致过拟合。!!!
>               当模型越简单时，即使我们再换一组数据，最后得出的学习器和之前的学习器的差别就不那么大，模型的方差很小。还是因为模型简单，所以偏差会很大。
>
>           泛化误差对模型的影响：
>               也就是说，当我们训练一个模型时，偏差和方差都得照顾到，漏掉一个都不行。
>               对于Bagging算法来说，由于我们会并行地训练很多不同的分类器的目的就是降低这个方差(variance) ,因为采用了相互独立的基分类器多了以后，h的值自然就会靠近.
>                   所以对于每个基分类器来说，目标就是如何降低这个偏差（bias),所以我们会采用深度很深甚至不剪枝的决策树。
>               对于Boosting来说，每一步我们都会在上一轮的基础上更加拟合原数据，所以可以保证偏差（bias）,所以对于每个基分类器来说，问题就在于如何选择variance更小的分类器，即更简单的分类器，
>                   所以我们选择了深度很浅的决策树。
>
>
>
>

- **GBDT在rank的原理：**
>       GBDT用在rank中，主要是如何进行pair-wise的训练？
>       比如应用在搜索中：
>           learning to rank需要解决的问题是给定一个query，如何选择最相关的document。**gbrank核心为将排序问题转化为一组回归问题。**
>           例如，
>           对于所有的query-document pair，从pair抽取出一系列特征对其进行表示。如query1-document1记为x,query1-document2记为y。x>y表示用户发起查询query1时，x比y更合适，更加满足query1的需求，
>           给定排序函数空间H，希望得到一个排序函数h(h∈H)，当x>y时，有h(x)>h(y)，损失函数为：
>           R(h) = 1/2 * ∑(max(0, h(y)-h(x)+τ))^2 - λ*τ^2
>           可以理解为：
>               如果h学到了这种排序关系，则h(x)>h(y)，h对于损失函数贡献为0，否则为(h(y)-h(x))^2。直接优化loss比较困难，可以通过改变h(y)或者h(x)来达到减少lass的目的
>               为了避免优化函数h是一个常量，在loss fuction上增加一个平滑项τ，0<τ≤1。在实际应用中τ为固定常数。
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

- **Adaboost：**
>       https://blog.csdn.net/v_JULY_v/article/details/40718799   Adaboost 算法的原理与推导
>
>

- **GBDT：**
>       GBDT（Gradient Boosting Decision Tree）
>       http://www.cnblogs.com/LeftNotEasy/archive/2011/03/07/1976562.html  （算法的流程详解）
>       https://blog.csdn.net/google19890102/article/details/51746402/  （GBDT源码解释）
>
>

- **xgboost：**
>       https://blog.csdn.net/v_JULY_v/article/details/81410574     july的xgboost
>
>
>

- **lightgbm：**
>       lightgbm详解：
>           https://blog.csdn.net/anshuai_aw1/article/details/83040541  Lightgbm 直方图优化算法深入理解
>           https://www.deeplearn.me/2315.html  LightGbm之直方图优化理解
>           http://izhaoyi.top/2017/09/23/sklearn-xgboost/#%E6%95%88%E7%8E%87%E5%92%8C%E5%86%85%E5%AD%98%E4%B8%8A%E7%9A%84%E6%8F%90%E5%8D%87    sklearn、XGBoost、LightGBM的文档阅读小记
>           https://www.msra.cn/zh-cn/news/features/lightgbm-20170105   开源 | LightGBM：三天内收获GitHub 1000  星
>       lightgbm主要做了工程优化，满足工业海量数据要求
>       优化点：
>           基于Histogram的决策树算法
>           带深度限制的Leaf-wise的叶子生长策略
>           直方图做差加速
>
>
>
>
>

- **待续：**
>       参考：https://blog.csdn.net/a819825294/article/details/51206410    xgboost原理
>           https://blog.csdn.net/weixin_42587745/article/details/82423410      xgboost 实战以及源代码分析
>           https://blog.csdn.net/Cdd2xd/article/details/77426622   GBM 与 GBDT 与 XgBoost
>           https://homes.cs.washington.edu/~tqchen/data/pdf/BoostedTree.pdf    Introduction to Boosted Trees[Tianqi Chen]
>           https://blog.csdn.net/yinyu19950811/article/details/81079192    XGBoost原理介绍(介绍比较全)
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
