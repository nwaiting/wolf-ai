## ML - XGboost论文及源码导读
- **概述：**
>
>
>
>
>

- **XGBoost：**
>       XGBoost的基学习器是CART回归树，，但与李航的《统计学习方法》等教材里介绍的CART回归树不同，XGBoost使用的是模型树。
>       简要的说，模型树的叶节点的输出值，不是分到该叶节点的所有样本点的均值（回归树），而是由一个函数生成的值。
>
>       该如何确定树的结构呢？我们该用什么特征分割节点、分割节点的特征值又是多少呢？
>           XGBoost用贪心算法遍历特征，用损失函数增益值判断该在哪个特征的何处分裂。
>           损失增益函数是分裂后树的损失函数值和分裂前树的损失函数值之差
>
>       注意：
>           在XGBoost中如果使用分类算法并且分为多类，最终形成的树的数目是类个数 * estimator个数
>           如果输入的n_estimators参数是100，目标变量分了3类，最后会有300棵树。
>
>
>
>

- **稀疏矩阵存储：**
>       稀疏矩阵存储格式总结+存储效率对比:COO,CSR,DIA,ELL,HYB
>           COO：
>               这是最简单的一种格式，每一个元素需要用一个三元组来表示，分别是（行号，列号，数值），对应上图右边的一列。这种方式简单，但是记录单信息多（行列），每个三元组自己可以定位，因此空间不是最优
>           CSR：
>               （CSR是按行压缩，CSC是和CSR相对应的一种方式，即按列压缩的意思）
>               CSR是比较标准的一种，也需要三类数据来表达：数值，列号，以及行偏移。
>               CSR不是三元组，而是整体的编码方式。
>           ELL：
>               用两个和原始矩阵相同行数的矩阵来存：第一个矩阵存的是列号，第二个矩阵存的是数值，行号就不存了，用自身所在的行来表示；这两个矩阵每一行都是从头开始放，如果没有元素了就用个标志比如*结束。
>           DIA：
>               对角线存储法，按对角线方式存，列代表对角线，行代表行
>           Hybrid (HYB) ELL + COO：
>               ELL中提到的，如果某一行特别多，造成其他行的浪费，那么把这些多出来的元素用COO单独存储。
>
>       经验：（网上经验仅供参数）
>           1、DIA和ELL格式在进行稀疏矩阵-矢量乘积(sparse matrix-vector products)时效率最高，所以它们是应用迭代法(如共轭梯度法)解稀疏线性系统最快的格式
>           2、COO和CSR格式比起DIA和ELL来，更加灵活，易于操作
>           3、ELL的优点是快速，而COO优点是灵活，二者结合后的HYB格式是一种不错的稀疏矩阵表示格式
>           4、根据Nathan Bell的工作，CSR格式在存储稀疏矩阵时非零元素平均使用的字节数(Bytes per Nonzero Entry)最为稳定（float类型约为8.5，double类型约为12.5），而DIA格式存储数据的非零元素平均使用的字节数与矩阵类型有较大关系，适合于StructuredMesh结构的稀疏矩阵（float类型约为4.05，double类型约为8.10），对于Unstructured Mesh以及Random Matrix,DIA格式使用的字节数是CSR格式的十几倍；
>           5、从我使用过的一些线性代数计算库来说，COO格式常用于从文件中进行稀疏矩阵的读写，如matrix market即采用COO格式，而CSR格式常用于读入数据后进行稀疏矩阵计算
>
>
>

- **XGBoost相关知识点：**
>       分布式支持：
>           提供了两种支持，一种基于RABIT，另一种则基于Spark
>           1、RABIT：
>               RABIT里提供了native MPI/Sun Grid Engine/YARN这三种方式
>                   (1) native MPI
>                       native MPI这种方式，实际上除了计算任务的调度管理以外，也提供了相应的通信原语，所以更像一个纯粹的MPI计算任务
>                   (2) Sun Grid Engine
>                       略
>                   (3) YARN
>                       这里有很多实现细节，包括YARN ApplicationMaster/Client的开发、Tracker脚本的开发、RABIT容错通信原语的开发以及基于RABIT原语的XGBoost算法分布式实现
>           2、Spark：
>               略
>       多线程并行优化：
>           使用OpenMP
>

- **YARN简介：**
>       YARN 是“ Yet Another Resource Negotiator”的简称
>       在进一步了解 YARN 框架之前我们需要知道，相比较而言， MapReduce 则是 YARN 的一个特例。 YARN 则是 MapReduce 的一个更加通用和高级的框架形式，并在其上增加了更多的功能。
>       云计算包括以下几个层次的服务: IaaS、PaaS和SaaS。
>           这里所谓的层次，是分层体系架构意义上的“层次”。laas. Paas、 Saas分别实现在基础设施层、软件开放运行平台层、应用软件层。
>
>       参考：https://www.ibm.com/developerworks/cn/data/library/bd-yarn-intro/index.html      YARN 简介
>           https://www.imooc.com/article/32462     Hadoop 之分布式资源管理框架YARN
>           https://www.jianshu.com/p/9228767f13a3  分布式资源管理系统：YARN
>
>

- **注意：**
>        Classification with more than 2 classes requires the induction of n_classes regression trees at each at each iteration,thus, the total number of induced trees equals n_classes * n_estimators.
>           For datasets with a large number of classes we strongly recommend to use RandomForestClassifier as an alternative to GradientBoostingClassifier .
>
>

- **待续：**
>       参考：http://mlnote.com/2016/10/29/xgboost-code-review-with-paper/
>           http://mlnote.com/2016/10/05/a-guide-to-xgboost-A-Scalable-Tree-Boosting-System/    XGboost: A Scalable Tree Boosting System论文及源码导读
>           https://www.cnblogs.com/xbinworld/p/4273506.html?utm_source=tuicool&utm_medium=referral     稀疏矩阵存储格式总结+存储效率对比:COO,CSR,DIA,ELL,HYB
>           https://jepsonwong.github.io/2018/05/21/xgboost/#%E8%A1%8C%E9%87%87%E6%A0%B7%E5%88%97%E9%87%87%E6%A0%B7     XGBoost
>           https://zxth93.github.io/2017/09/29/XGBoost%E7%AE%97%E6%B3%95%E5%8E%9F%E7%90%86/index.html      XGBoost算法原理
>           https://wepon.me/2016/05/07/XGBoost%E6%B5%85%E5%85%A5%E6%B5%85%E5%87%BA/    XGBoost浅入浅出
>           https://www.zhihu.com/question/41354392/answer/98658997     机器学习算法中 GBDT 和 XGBOOST 的区别有哪些？
>           https://blog.csdn.net/yinyu19950811/article/details/81079192
>               XGBoost原理介绍（介绍分布式加权直方图、稀疏感知分裂发现、System design(缓存感知访问(Cache-aware Access)、用于核外计算的块)）
>           https://zhuanlan.zhihu.com/p/41207969   说说XGBoost 算法中的CART模型树
>           https://lonepatient.top/2017/03/18/boosting.html    XGBoost、LightGBM和CatBoost的同与不同
>
>
>
>
>
>
>
