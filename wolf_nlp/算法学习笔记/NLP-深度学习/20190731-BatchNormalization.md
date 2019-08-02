## dl - BatchNormalization
- **概述：**
>       BatchNormalization不仅能够大大加快收敛速度，还自带正则化功能，是Google 2015年提出的。(Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift)
>
>       机器学习的一个重要的假设是：数据是独立同分布的。训练集合测试集的数据是同分布的，这样模型才有好的泛化效果。神经网络其实也是在学习这个分布。
>       但是在实际训练过程中，数据经过前一个隐藏层向后一个隐藏层传播（线性+非线性运算），分布通常会发生变化（作者称之为Internal Covariate Shift），这会导致网络学习变慢。
>
>

- **BatchNormalization：**
>       比如激活函数是sigmoid函数的时候，当反向求导时，当x逐渐增大时，激活函数的导数值接近0，导致收敛速度变慢。如果想要收敛速度变快，则可以把x拉到靠近0的位置就行，这里附近的导数值最大
>       BatchNormalization就是解决这个问题的，将隐藏层的输入强行变换为同一分布（解决了第一个问题，前后数据分布不一致情况），这个分布就是正态分布（解决了第二个问题，收敛速度问题）
>
>       强行变换到正态分布，有两个问题：
>           1、谁说数据一定是正态分布的，偏正态不行吗？
>           2、把数据全部拉到接近0的位置，sigmoid不就接近于一个线性函数了吗，没有起到激活的作用啊
>       为了解决上面两个问题，引入了两个参数gamma和beta，这两个参数是在训练中学习的。
>      
>       预测过程，例如只预测一个样本，均值和方差如何计算？
>           事实上，预测的时候用的是全局的均值和方差
>           训练过程中记录下每个Mini-Batch的均值和方差，求个期望就是全局的均值和方差
>           
>       BatchNormalization缺点：
>           1、对batch_size非常敏感
>               BatchNormalization的一个重要出发点是保持每层输入的数据同分布
>               实验也证明，batch_size取得大一点， 数据shuffle的好一点，BatchNormalization的效果就越好
>           2、不能很方便地用于RNN
>               在应用BatchNormalization时，这就要求对每个time step的batch_size个输入计算一个均值和方差。那么问题就来了，假如有一个句子S非常长，那就意味着对S而言，
>                   总会有个time_step的batch_size为1，均值方差没意义，这就导致了BatchNormalization在RNN上无用武之地了
>       为了避免这两个问题，LayerNormalization就应运而生了
>           
>       BatchNormalization在处理不等长序列上存在天生的缺陷，但是除此之外，它的效果都要好于其他Normalization方式（比如LN，WN，IN）
>           
>

- **LayerNormalization：**
>       LayerNormalization，可以说层归一化是BatchNormalization的2.0版本，它是由Hinton神和他的学生提出的
>       LayerNormalization的特点：
>           1、不再对Mini-Batch中的N的样本在各个维度做归一化，而是针对同一层的所有神经元做归一化。
>               BatchNormalization是在每个神经元上对batch_size个数据做归一化，每个神经元的均值和方差均不相同
>               LayerNormalization则是对所有神经元做一个归一化，这就跟batch_size无关了。哪怕batch_size为1，这里的均值和方差只和神经元的个数有关系
>           2、测试的时候可以直接利用LN，所以训练时不用保存均值和方差，这节省了内存空间
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
>       参考：https://lonepatient.top/2019/01/17/BERT-Transformer.html     Transformer原理和实现
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
