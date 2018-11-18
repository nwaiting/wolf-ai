### Google算法 - LDA算法
- **概述：**
>       pLS模型的作者Thomas Hoffmann提出的机器学习算法是EM。EM是各种机器学习算法中少数适合用MapReduce框架描述的：
>           map phase用来推测隐含变量的分布，也就是实现E步；
>           reduce phase利用上述结果来更新模型，就是M步
>       但是2008年的时候，pLSA已经被新兴的LDA掩盖。LDA是pLSA的generalization：
>           一方面LDA的hyperparameeter设为特定值的时候，就specialize成pLSA了。
>       从工程应用价值的角度看，这个数学方法的generalization，允许我们用一个训练好的模型解释任何一段文本中的语义。
>           而pLSA只能理解训练文本中的语义。这就使得继续研究pLSA价值不明显了。
>       LDA：pLSA加上topics的Dirichlet先验分布后得到的Bayesiab model，数学上更漂亮。为什么是Dirichlet先验分布，主要是利用了
>           Dirichlet和multinomial分布的共轭性，方便计算。
>
>       Google在07年左右或者更早就抛弃了pLSA转向LDA。
>           pLSA只能对训练样本中进行语义识别，而对不在样本中的文本是无法识别其语义的，但是LDA能。
>           目前LDA的挑战主要在于长尾分类这块，Google推出了Rephil解决这个问题，借此Google Ads收入占到Google输入的50%以上。
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
>
>
>
>
>
>
>
>
>
