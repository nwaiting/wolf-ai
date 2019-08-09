## dl - Transformer
- **概述：**
>       Attention Is All You Need是一篇Google提出的将Attention思想发挥到极致的论文
>       这篇论文中提出一个全新的模型，叫 Transformer，抛弃了以往深度学习任务里面使用到的 CNN 和 RNN ，目前大热的Bert就是基于Transformer构建的
>       Transformer应用领域：
>           这个模型广泛应用于NLP领域，例如机器翻译，问答系统，文本摘要和语音识别等等方向
>
>       transform是目前效果最好的特征抽取器，本质是self attention叠加结构。！！！
>
>       Transformer中的这种多层-多子层的机制，可以使得模型的复杂度和可训练程度都变高，达到非常强的效果，值得借鉴。！！！
>
>

- **Transformer架构：**
>       和Attention模型一样，Transformer模型中也采用了 encoer-decoder 架构。但其结构相比于Attention更加复杂，论文中encoder层由6个encoder堆叠在一起，decoder层也一样
>

- **长距离依赖信息：**
>       1、一个词其实是一个可以表达多样性语义信息的符号（歧义问题）
>       2、一个词的语义确定，要依赖其所在的上下文环境。（根据上下文消岐）
>       3、有的词可能需要一个范围较小的上下文环境就能确定其语义（短距离依赖现象），有的词可能需要一个范围较大的上下文环境才能确定其语义（长距离依赖现象）
>

- **RNN、CNN和Attention比较：**
>       1、RNN
>           带有门控（Gate）机制的RNN模型理论上可以对历史信息进行有选择的存储和遗忘，具有比纯RNN结构更好的表现，但是门控参数量一定的情况下，这种能力是一定的。
>           随着句子的增长，相对距离的增大，存在明显的理论上限。
>       2、CNN
>           多层的CNN结构体现的是一种从局部到全局的特征抽取过程。
>           词之间的交互距离，与他们的相对距离成正比。距离较远的词只能在较高的CNN节点上相遇，才产生交互。这个过程可能会存在较多的信息丢失。
>       3、Attention
>           每个词和第一层self-attention layer中的节点都是全连接的关系，第一层self-attention layer和第二层self-attention layer之间的节点也都是全连接的关系。
>           在这种建模方法中，任意两个词之间的交互距离都是1，与词之间的相对距离不存在关系。
>           每个词的语义的确定，都考虑了与整个句子中所有的词的关系。
>           多层的self-attention机制，使得这种全局交互变的更加复杂，能够捕获到更多的信息。
>           self-attention机制在建模序列问题时，能够捕获长距离依赖知识，具有更好的理论基础。
>

- **Self-attention机制的变种：**
>       Transformer里面的self-attention机制是一种新的变种，体现在两点：
>           1、一方面是加了一个缩放因子（scaling factor）
>               缩放因子体现在Attention的计算公式中多了一个向量的维度作为分母，目的是想避免维度过大导致的点乘结果过大，进入softmax函数的饱和域，引起梯度过小
>           2、另一方面是引入了多头机制（multi-head attention）
>               多头机制是指，引入多组的参数矩阵来分别对Q、K、V进行线性变换求self-attention的结果，然后将所有的结果拼接起来作为最后的self-attention输出。
>               这种方式使得模型具有多套比较独立的attention参数，理论上可以增强模型的能力
>

- **位置编码：**
>       CNN模型其实也存在同样的难以建模相对位置（时序信息）的缺陷，Facebook提出了位置编码的方法。
>       1、一种直接的方式是，直接对绝对位置信息建模到embedding里面，即将词Wi的i映射成一个向量，加到其embedding中去
>           缺点：只能建模有限长度的序列
>       2、Transformer文章中提出了一种非常新颖的时序信息建模方式
>           利用三角函数的周期性，来建模词之间的相对位置关系。
>           直观解释：（仅供参考）
>           (1)、一方面三角函数有很好的周期性，也就是隔一定的距离，因变量的值会重复出现，这种特性可以用来建模相对距离
>           (2)、三角函数的值域是[-1,1]，可以很好的提供embedding元素的值
>
>       Tensor2Tensor中Positional encoding的实现：
>           论文中根据维度下标的奇偶性来交替使用sin和cos函数的说法，在代码中并不是这样实现的，而是前一半的维度使用sin函数，后一半的维度使用cos函数，并没有考虑奇偶性
>

- **Transformer优点：**
>       Transformer使用了很多之前验证过的有效方法，比如：
>           1、residual connection（残差网络）
>               Residual connection 残差连接是resnet的基本层构造
>               g(x) = f(x) + x
>               残差网络优点：（仅供参考）
>                   那么该层网络对x求偏导的时候，多了一个常数项，所以在反向传播过程中，梯度连乘，也不会造成梯度消失
>           2、layer normalization
>               可以加快模型的收敛速度
>           3、self-attention层与Feed Forward层的堆叠
>

- **Encoder：**
>       每一层的Encoder，包含了两个子层（sub-layer），包含：
>           1、第一个子层是多头的self-attention layer
>           2、第二个子层是一个Feed Forward层
>       每个子层的输入和输出都存在着residual connection，这种方式理论上可以很好的回传梯度。
>
>       Feed Forward子层：
>           Feed Forward子层实现中有两次线性变换，一次Relu非线性激活
>           FFN(x) = max(0, w1*X+b1)w2+b2
>           文章的附页中将这种计算方式也看做是一种attention的变种形式
>

- **Decoder：**
>       Decoder的一层结构，包含三个子层结构，包含：
>           1、第一层是self-attention layer用来建模已经生成的目标端句子
>               在训练的过程中，需要一个mask矩阵来控制每次self-attention计算的时候，只计算到前t-1个词
>           2、第二个子层是Encoder和Decoder之间的attention机制
>               就是去源语言中找相关的语义信息，这部分的计算与其他序列到序列的注意力计算一致，在Transformer中使用了dot-product的方式
>           3、第三个子层是Feed Forward层，与Encoder中的子层完全一致
>               每个子层也都存在着residual connection和layer normalization操作，以加快模型收敛
>

- **优化方法与正则策略：**
>       优化方法：
>           模型的训练采用了Adam方法，文章提出了一种叫warm up的学习率调节方法
>           所以整体来看，学习率呈先上升后下降的趋势，有利于模型的快速收敛
>       正则策略：
>           使用了两个正则化方法，
>           1、一个就是常用的dropout方法
>               用在每个子层的后面和attention的计算中
>           2、label smoothing方法
>               就是训练的时候，计算交叉熵的时候，不再是one-hot的标准答案了，而是每个0值处也填充上一个非0的极小值
>               优点：可以增强模型的鲁棒性，提升模型的BLEU值
>               这个思路其实也是一定程度在解决训练和解码过程中存在的exposure bias的问题。
>

- **如何做mask：**
>       由于模型是以batch为单位进行训练的，batch的句长以其中最长的那个句子为准，其他句子要做padding
>       padding项在计算的过程中如果不处理的话，会引入噪音，所以就需要mask，来使padding项不对计算起作用
>       mask在attention机制中的实现非常简单，就是在softmax之前，把padding位置元素加一个极大的负数，强制其softmax后的概率结果为0
>       举个例子，[1,1,1]经过softmax计算后结果约为[0.33,0.33,0.33]，[1,1,-1e9] softmax的计算结果约为[0.5, 0.5,0]。这样就相当于mask掉了数组中的第三项元素
>       在对target sequence进行建模的时候，需要保证每次只attention到前t-1个单词，这个地方也需要mask，整体的mask是一个上三角矩阵，非0元素值为一个极大的负值
>

- **基于batch的解码：**
>       解码的时候，如果是基于文件的，那么就会将句子组成batch来并行解码
>       这里有个小trick，就是先对句子进行排序，然后从长的句子开始组batch，翻译，再把句子恢复成原先的顺序返回
>       这种方式可以很好的检测到显存不足的错误，因为解句子最长的一个batch的时候，显存都是够得，那其他的batch也不存在问题
>
>
>

- **待续：**
>       参考：https://zhuanlan.zhihu.com/p/48508221    详解Transformer （Attention Is All You Need）！！
>           https://zhuanlan.zhihu.com/p/44121378       Transformer详解
>           https://terrifyzhao.github.io/2019/01/11/Transformer%E6%A8%A1%E5%9E%8B%E8%AF%A6%E8%A7%A3.html   Transformer模型详解！！
>           http://blog.itpub.net/31562039/viewspace-2375080/   BERT大火却不懂Transformer？读这一篇就够了 ！！
>           https://blog.csdn.net/pipisorry/article/details/84946653    深度学习：transformer模型
>           https://www.jianshu.com/p/d2ae158fc9e5      Transformer详解（二）：Attention机制
>           http://www.mayexia.com/NLP/Attention%E6%9C%BA%E5%88%B6%E5%92%8CTransformer%E6%A1%86%E6%9E%B6%E8%AF%A6%E8%A7%A3/     Attention机制和Transformer框架详解
>           https://cupdish.com/2018/03/28/attention-is-all-you-need/#Decoder-%E9%83%A8%E5%88%86    Attention is all you need 论文阅读报告及代码详解
>           https://blog.csdn.net/malefactor/article/details/78767781   深度学习中的注意力机制(2017版)
>           http://shukebeta.me/NLP-attention-03-self-attention/    Transformer - 多头自注意力编码机制
>           https://lonepatient.top/2019/01/18/BERT-Transformer.html    Transformer原理和实现 ！！！
>           http://fancyerii.github.io/2019/03/09/transformer-illustrated/  Transformer图解
>           https://cloud.tencent.com/developer/article/1153079     “变形金刚”为何强大：从模型到代码全面解析Google Tensor2Tensor系统  ！！！
>
>
>
>
>
>
>
>
