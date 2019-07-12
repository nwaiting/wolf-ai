## ML-hmm  hmm-gmm
- **概述：**
>       马尔可夫过程（Markov process）是一类随机过程。它的原始模型马尔可夫链，由俄国数学家A.A.马尔可夫于1907年提出
>       马尔可夫过程是研究离散事件动态系统状态空间的重要方法，它的数学基础是随机过程理论
>
>       常见的马尔科夫过程：
>           1、独立随机过程为马尔可夫过程
>           2、泊松过程为马尔可夫过程
>           3、维纳过程为马尔可夫过程
>           4、质点随机游动过程为马尔可夫过程
>

- **声学模型：**
>       声学模型的目的是将经MFCC提取的所有帧的特征向量转化为有序的音素输出
>
>       现在大多数识别都采用三音素模型
>       聚类算法来对所有的上下文相关的三音素做聚类，得到绑定状态聚类的一个集合
>
>       GMM：
>           GMM主要是为了得到HMM求解过程的发射概率
>       HMM：
>           就是根据各个概率得到最优的音素
>           聚类算法来对所有的上下文相关的三音素做聚类，得到绑定状态聚类的一个集合
>           现在大多数识别都采用三音素模型，为了压缩建模单元数量，状态绑定的技术被大量使用，它使得发音类似的状态用一个模型表表示，从而减少了参数量。！！！
>               状态绑定的技术可以使用专家手工编撰的规则，也可以使用数据驱动的方式。
>
>

- **识别的三步：**
>       1、第一步，把帧识别成状态（gmm）
>       2、第二步，把状态组合成音素（hmm）
>       3、第三步，把音素组合成单词（hmm）
>
>

- **hmm：**
>       前向概率、后向概率：
>           前向概率：
>               2、中括号意思就是当前层的所有N个隐状态与下一层的第i个状态的连接，里面的 α 是到时刻t部分观测序列为，
>                   且在 t 时刻处于状态 j 的概率（前向计算给出，第一层用的是过程①），a是 t 时刻第 j 个状态到 t+1 时刻第 i 个状态的转移情况（转移矩阵给出）；
>                   中括号外面乘以的b是当前状态下，对应观测情况发生的概率，比如当前是晴天，那么晴天对应海藻湿润的概率是什么呢?就是b，由混淆矩阵给出。
>               3、其实就是求解在时刻t，所有状态的概率求和
>           后向概率：
>               2、对于t=T-1,T-2,...1递推计算，时刻 t 状态为条件下时刻t+1之后的观测序列为的后向概率，
>                   其实就是第t+1 时刻的N个状态到t 时刻状态的转移概率乘以t+1时刻每个隐状态对应的观察情况为o(t+1)的概率，再乘以状态j之后的观测序列的后向概率
>               3、计算一种加和，但是与前向算法的加和还不一样，它的含义是与步骤②一样的，只不过初始概率 π 代替了转移概率a
>
>

- **gmm和hmm参数估计：**
>       gmm参数估计：
>           E（estimate）-step: 根据当前参数 (means, variances, mixing parameters)估计P(j|x)
>           M（maximization）-step: 根据当前P(j|x) 计算GMM参数
>
>       HMM参数估计：
>           E（estimate）-step: 给定observation序列，估计时刻t处于状态sj的概率γt(j)
>           M（maximization）-step: 根据γt(j)重新估计HMM参数aij
>
>       gmmhmm结合：
>           假设状态->observation服从单核高斯概率分布
>
>       gmm-hmm结合识别：
>           一是把当前frame的特征识别为这个state的概率(也就是GMM中的mean vector 和covariance matrix )
>           二是上个state转化为这个state的概率也就是状态转移概率Transition probabilities。
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
>       参考：https://blog.csdn.net/xmu_jupiter/article/details/50965039   HMM的Baum-Welch算法和Viterbi算法公式推导细节
>           https://blog.csdn.net/abcjennifer/article/details/27346787      GMM-HMM语音识别模型 原理篇
>           https://www.cnblogs.com/pinard/p/6972299.html   隐马尔科夫模型HMM（三）鲍姆-韦尔奇算法求解HMM参数
>           https://blog.csdn.net/fandaoerji/article/details/44853853   HMM+GMM语音识别技术详解级PMTK3中的实例
>           https://blog.csdn.net/quheDiegooo/article/details/55520775  语音识别中声学模型训练过程-GMM（一）
>           https://blog.csdn.net/wbgxx333/article/details/39006885     语音识别基本原理介绍--gmm-hmm中训练的完整版
>           https://blog.csdn.net/wbgxx333/article/details/38962623     语音识别基本原理介绍之gmm-hmm续
>           https://blog.csdn.net/nsh119/article/details/79496409       语音识别-声学模型（GMM-HMM）
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
