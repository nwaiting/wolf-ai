## NLP_ML - Apriori
- **概述：**
>       Apriori是常用的用于挖掘出数据关联规则的算法，用来找出数据值中频繁出现的数据集合，找出这些集合的模式有助于做一些决策。如：
>           1、超时购物数据集（可以优化产品的位置摆放）
>           2、电商的网购数据（优化商品所在的仓库位置）
>           可以达到节约成本，增加效益的目的。
>
>       关联规则挖掘算法：
>           1、Apriori
>           2、PrefixSpan
>           3、CBA
>
>       频繁数据集的评估，需要解决的两个问题：
>           1、当数据集很大时，催生了关联规则挖掘算法
>           2、频繁数据集的评估标准
>               常见的频繁数据集的评估标准有：
>                   1、支持度
>                       一般支持度高的数据不一定构成频繁项集，但是支持度太低的数据肯定不构成频繁项集
>                   2、置信度
>                       体现了一个数据出现后，另一个数据出现的概率，或者说数据的条件概率
>                   3、提升度
>                       表示含有y的条件下，同时含有x的概率，与x总体发生的概率之比
>               要选择一个数据集合中的频繁数据集，需要自定义评估标准。
>               最常用的评估标准是用自定义的支持度，或者是自定义支持度和置信度的一个组合
>
>

- **支持度：**
>       几个关联的数据在数据集中出现的次数占总数据集的比重，或者说几个关联数据出现的概率。
>

- **置信度：**
>       条件概率
>

- **提升度：**
>       提升度体现了x和y之间的关联关系，提升度大于1则x、y是有效的强关联关系，提升度小于等于1则x、y是无效的强关联规则
>
>

- **Apriori算法总结：**
>       Apriori算法每轮迭代都要扫描数据集，因此在数据集很大，数据种类很多时，算法效率很低。
>       现在工业界很少直接用Apriori来挖掘数据，但是Apriori是一个非常经典的频繁项集的挖掘算法，很多算法都是基于Apriori而产生的，
>       如：FPTree、GSP、CBA等，这些算法利用了Apriori算法思想，但是对算法做了改进，效率更高
>
>
>
>

- **Apriori算法过程：**
>       算法过程如下图，
>       ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/data_pic/data_pic_apriori_detail_1.jpg)
>       ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/data_pic/data_pic_apriori_detail_2.jpg)
>       ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/data_pic/data_pic_apriori_detail_3.jpg)
>
>
>
>
>
>

- **待续：**
>       参考：<<数据挖掘：概念与技术>> 范明 孟小峰
>           https://www.cnblogs.com/pinard/p/6293298.html   Apriori算法原理总结
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
