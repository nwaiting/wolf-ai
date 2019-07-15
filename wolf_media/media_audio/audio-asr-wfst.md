## media-audio asr wfst（Weighted Finite-state Transducer）
- **概述：**
>
>
>
>
>
>
>

- **HCLG：**
>       G:语言模型WFST，输入输出符号相同，实际是一个WFSA（acceptor接受机），为了方便与其它三个WFST进行操作，将其视为一个输入输出相同的WFST。
>           G.fst用于对语言模型进行编码。
>           当使用统计语言模型时，用srilm训练出来的语言模型为arpa格式，可以用arpa2fst将arpa转换成fst，
>       L:发音词典WFST，输入符号：monophone，输出符号：词;
>           L.fst是一个把音素映射成为词的发音词典FST
>       C:上下文相关WFST，输入符号：triphone（上下文相关），输出符号：monophnoe;
>           triphone到monophone的转换器，加入他可以避免枚举所有可能的monophone
>       H:HMM声学模型WFST，输入符号：HMMtransitions-ids，输出符号：triphone。
>
>       WFST的三大算法：
>           Composition
>           Determinization
>           Minimization
>
>       WFST在语音识别中的应用，即HCLG的操作：
>           WFST来表征ASR中的模型（HCLG），可以更方便的对这些模型进行融合和优化，于是可以作为一个简单而灵活的ASR的解码器（simple and flexible ASR decoder design）
>
>

- **FST、WFST、WFSA：**
>       FST和WFST的区别：
>           有限状态转换器FST(finite-state transducer)
>           加权有限状态转换器WFST(weighted finite-state transducer)
>       WFST和WFSA的区别：
>           WFST：只有一个label
>           WFSA(weighted finite-state acceptor)：状态转移上的label既有输入又有输出
>
>
>
>
>

- **待续：**
>       参考：http://antkillerfarm.github.io/speech/2018/07/26/speech_6.html   语音识别（六）——语言模型进阶, GMM-HMM, WFST
>           https://blog.csdn.net/l_b_yuan/article/details/50876340     走进语音识别中的WFST（一）（详解）！！！
>           https://blog.csdn.net/fengzhou_/article/details/80776805    语音识别WFST核心算法讲解(1. WFST的基本概念)
>           https://x-algo.cn/index.php/2017/04/29/speech-recognition-decoder-1-automata-and-semi-circular/     语音识别解码器(1)—自动机与半环
>           https://blog.csdn.net/lucky_ricky/article/details/77511543  Kaldi WFST 构图 学习
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
