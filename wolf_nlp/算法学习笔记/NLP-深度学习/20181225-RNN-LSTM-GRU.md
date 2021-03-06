### 深度学习 - RNN、GRU、LSTM
- **概述**：
>       RNN中，前向是输入信息到输出信息的传递过程，反向是计算梯度，就是根据输出的cost来对变量进行调整的过程。
>
>
>
>
>
>
>

- **RNN：**
>       对于一次任务的损失函数L，即每一时刻损失值的累加。
>       如使用随机梯度下降法训练RNN，其实就是对Wx、Ws、Wo以及b1、b2求偏导，并不断调整是L到达最小。
>       当对Wx、Ws求偏导时，会随着时间序列产生长期依赖，即产生梯度小时或梯度爆炸。！！！
>
>       针对公式中，求偏导中的连乘项，可以使用方法进行规避，这个就是LSTM做的优化。
>       由于RNN反向传播时，短期记忆h被不断累乘，所以会有梯度消失和爆炸问题；
>       LSTM是累积，所以LSTM解决了梯度消失问题，但是依然有梯度爆炸问题。
>
>

- **LSTM：**
>       LSTM只能避免RNN的梯度消失，梯度爆炸不是个严重的问题，一般靠裁剪后的优化算法即可解决，比如gradient clipping（如果梯度的范数大于某个给定值，将梯度同比收缩）
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
>       参考：https://lonepatient.top/2018/03/11/understand%20LSTM.html    理解LSTM ！！！
>           https://zhuanlan.zhihu.com/p/28749444
>           https://www.zhihu.com/question/34878706     LSTM如何来避免梯度弥散和梯度爆炸？（从不同角度分析为什么LSTM能避免弥散）
>           https://www.zhihu.com/question/34878706/answer/665429718    LSTM如何来避免梯度弥散和梯度爆炸？
>           https://www.cnblogs.com/zhangchaoyang/articles/6684906.html     RNN和LSTM
>           https://blog.csdn.net/mpk_no1/article/details/72875185      深度学习笔记——RNN（LSTM、GRU、双向RNN）学习总结
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
