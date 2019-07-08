## 深度学习 - Tensor2Tensor
- **概述**：
>
>
>
>
>
>
>

- **Transformer原理：**
>       《Attention Is All You Need》这篇文章，描述了一个基于self-attention的序列到序列的模型，即“Transformer”。
>       Transformer模型：
>           该模型的表现的如此好的原因，其实不仅仅是一个self-attention机制导致的，
>               实际上Transformer模型中使用了非常多有效的策略来使得模型对数据的拟合能力更强，收敛速度更快。
>           整个Transformer的模型是一套解决方案，而不仅仅是对序列建模机制的改进。
>
>       一、Transformer里面的self-attention机制是一种新的变种，有两个方面：
>           1、一方面是加了一个缩放因子（scaling factor）
>                缩放因子体现在Attention的计算公式中多了一个向量的维度作为分母，目的是想避免维度过大导致的点乘结果过大，进入softmax函数的饱和域，引起梯度过小。
>           2、一方面是引入了多头机制（multi-head attention）
>               多头机制是指，引入多组的参数矩阵来分别对Q、K、V进行线性变换求self-attention的结果，然后将所有的结果拼接起来作为最后的self-attention输出。
>       二、位置编码（Positional Encoding）
>           self-attention机制建模序列的方式，既不是RNN的时序观点，也不是CNN的结构化观点，而是一种词袋（bag of words）的观点。
>               进一步阐述的话，应该说该机制视一个序列为扁平的结构，因为不论看上去距离多远的词，在self-attention机制中都为1。
>               这样的建模方式，实际上会丢失词之间的相对距离关系。
>           为了缓解这个问题，Transformer中将词在句子中所处的位置映射成vector，补充到其embedding中去。
>           该思路并不是第一次被提出，CNN模型其实也存在同样的难以建模相对位置（时序信息）的缺陷，Facebook提出了位置编码的方法。
>           1、一种直接的方式是，直接对绝对位置信息建模到embedding里面，即将词Wi的i映射成一个向量，加到其embedding中去。
>               这种方式的缺点是只能建模有限长度的序列。
>           2、Transformer文章中提出了一种非常新颖的时序信息建模方式，就是利用三角函数的周期性，来建模词之间的相对位置关系。
>               具体的方式是将绝对位置作为三角函数中的变量做计算，公式略
>               直观解释：（仅供参考）
>                   一方面三角函数有很好的周期性，也就是隔一定的距离，因变量的值会重复出现，这种特性可以用来建模相对距离；
>                   另一方面，三角函数的值域是[-1,1]，可以很好的提供embedding元素的值。
>       三、多层结构
>           Transformer中的多层结构非常强大，使用了之前已经被验证过的很多有效的方法
>               包括residual connection、layer normalization，另外还有self-attention层与Feed Forward层的堆叠使用
>           Encoder中：
>               这一层中包含了两个子层（sub-layer），第一个子层是多头的self-attention layer，第二个子层是一个Feed Forward层。
>               每个子层的输入和输出都存在着residual connection，这种方式理论上可以很好的回传梯度。
>               Layer Normalization的使用可以加快模型的收敛速度。
>           Decoder中：
>               这一层中存在三个子层结构，
>               第一子层是self-attention layer用来建模已经生成的目标端句子。
>                   在训练的过程中，需要一个mask矩阵来控制每次self-attention计算的时候，只计算到前t-1个词
>               第二个子层是Encoder和Decoder之间的attention机制
>                   就是去源语言中找相关的语义信息，这部分的计算与其他序列到序列的注意力计算一致，在Transformer中使用了dot-product的方式。
>               第三个子层是Feed Forward层
>                   与Encoder中的子层完全一致。
>               每个子层也都存在着residual connection和layer normalization操作，以加快模型收敛。
>
>           总结：
>               Transformer中的这种多层-多子层的机制，可以使得模型的复杂度和可训练程度都变高，达到非常强的效果，值得我们借鉴。
>
>       优化方法与正则策略：
>           模型的训练采用了Adam方法，文章提出了一种叫warm up的学习率调节方法
>               lrate = d * min(step_num^(-0.5), step_num*warmup_steps^(-1.5))
>               需要预先设置一个warmup_steps超参
>               当训练步数step_num小于该值时，以括号中的第二项公式决定学习率，该公式实际是step_num变量的斜率为正的线性函数。
>               当训练步数step_num大于warm_steps时，以括号中的第一项决定学习率，该公式就成了一个指数为负数的幂函数。
>               所以整体来看，学习率呈先上升后下降的趋势，有利于模型的快速收敛。
>           模型中也采用了两项比较重要的正则化方法：
>               1、常用的dropout方法，用在每个子层的后面和attention的计算中。
>               2、label smoothing方法，也就是训练的时候，计算交叉熵的时候，不再是one-hot的标准答案了，而是每个0值处也填充上一个非0的极小值。
>                   这样可以增强模型的鲁棒性，提升模型的BLEU值。
>               这个思路其实也是一定程度在解决训练和解码过程中存在的exposure bias的问题。
>

- **Transformer总结：**
>       Transformer系统的强大表现，不仅仅是self-attention机制，还需要上述的一系列配合使用的策略。
>       设计该系统的研究者对深度学习模型和优化算法有着非常深刻的认识和敏锐的感觉，很多地方值得我们借鉴学习。
>       
>
>
>
>
>

- **待续：**
>       参考：https://cloud.tencent.com/developer/article/1153079  “变形金刚”为何强大
>           https://segmentfault.com/a/1190000015575985
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
>
>
>
>
