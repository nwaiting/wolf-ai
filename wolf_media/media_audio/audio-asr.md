## media-audio audio asr
- **概述：**
>       asr流程如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_ASR.png)
>
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_asr_flow.png)
>
>

- **asr知识图谱：**
>       如下图，
>![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_asr_graph.png)
>
>
>

- **传统的语音识别**
>       传统的语音识别过程中：
>           1、声学模型的输出单元一般为音素或者是音素的状态
>           2、语言模型一般是词级别的语言模型
>           两者的联合解码（也就是一般的测试推断过程）时需要知道每个词（word）是由哪些音素（phoneme）组成的，也就是这个词是怎么发音的。
>           3、一个发音词典，一般也被叫做音素模型
>
>       目的是构建一个模型，使得P(W|O)最大
>       根据贝叶斯公式，通常在进行解码（或者说推断）的时候输入O是保持不变的，目的是找到一个W使得后验概率最大，所以我们忽略分母项。
>       P(O|W) = P(O,Q|W)，Q为音素序列
>
>
>
>
>

- **待续：**
>       参考：https://zhuanlan.zhihu.com/p/33464788?edition=yidianzixun&utm_source=yidianzixun&yidian_docid=0IHnKxdI   基于CTC的语音识别基础与实现
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
