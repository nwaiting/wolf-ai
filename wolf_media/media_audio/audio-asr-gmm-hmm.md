## media-audio asr gmm hmm
- **概述：**
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

- **一段语音是怎么切割音素？**
>       如’我‘的拼音是wo，我们按声韵母分开是：w o？
>       答案：
>           如果要训练w和o的分界点在哪我们不知道，所以HMM模型的训练就是问题。
>           这里使用EM算法，开始随机对语音分帧，例如平均分割语音，使用EM算法和前向后向算法
>           E步是求出每一帧位于哪个音素，M步是对于每个音素，找到它对应的所有帧，从这些帧的特征中估计音素模型的参数。
>           对齐之后就可以对每个状态进行GMM训练，之后循环E步M步。其中E步只要判断相邻音素的那一帧属于左边音素还是右边音素就可以了。
>
>

- **孤立词识别中的GMM-HMM和连续词识别中的GMM-HMM有什么不一样？**
>       孤立词识别中每个词都有自己的GMM-HMM，也就是说虽然有的词包括有相同的音素，但是数据不共享。
>       大词汇量的训练中，是对音素建立GMM-HMM模型，所以数据共享。
>
>

- **待续：**
>       参考：https://blog.csdn.net/abcjennifer/article/details/27346787   GMM-HMM语音识别模型 原理篇
>           https://blog.csdn.net/wbgxx333/article/details/18516053     语音识别系统原理介绍---从gmm-hmm到dnn-hmm
>           https://www.xuebuyuan.com/2100302.html  语音识别系统原理介绍—-gmm-hmm
>           https://blog.csdn.net/wbgxx333/article/details/10020449     语音信号处理之（四）梅尔频率倒谱系数（MFCC）
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
