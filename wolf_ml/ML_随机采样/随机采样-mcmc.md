## ML-随机采样 - mcmc
- **概述：**
>       推断：
>           1、精确推断
>           2、近似推断
>               (1)、确定性近似（Variation Inference）
>               (2)、随机性近似（MCMC）
>
>
>       蒙特卡洛采样方法：
>           1、基于概率分布采样
>           2、拒绝采样
>           3、重要性采样（对每个采样点进行加权）
>
>
>       马氏链：
>           时间和状态都是离散的随机过程
>           研究对象是一个随机变量序列
>
>       马尔可夫性：
>           无后效性，未来只依赖于当前
>
>       MH：
>           根据细致平稳分布得到的因子，构造采样率α关于转移概率的表达式，然后通过随机采样，
>           得到的概率在采样率α内的则接收样本，否则取前一次的样本
>
>       Gibbs：
>           一维一维的进行采样
>           相对于MH采样，接受率为1，采样效率高，是一种特殊的MH采样
>
>
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/xbinworld/p/4266146.html     随机采样方法整理与讲解（MCMC、Gibbs Sampling等）
>           https://zhuanlan.zhihu.com/p/37121528   马尔可夫链蒙特卡罗算法（MCMC）
>           https://cosx.org/2013/01/lda-math-mcmc-and-gibbs-sampling/  LDA-math-MCMC 和 Gibbs Sampling
>
>
>           https://www.cnblogs.com/pinard/p/6625739.html   MCMC(一)蒙特卡罗方法
>           https://blog.csdn.net/chenshulong/article/details/78906129  MCMC
>           https://blog.csdn.net/G090909/article/details/50878066  马尔科夫蒙特卡洛算法(MCMC)
>           https://www.jianshu.com/p/28d32aa7cc45  MCMC方法小记
>           https://blog.csdn.net/google19890102/article/details/51755242   简单易学的机器学习算法——马尔可夫链蒙特卡罗方法MCMC
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
