## NLP_搜索引擎 - 基础知识
- **概述：**
>
>
>

- **搜索引擎的整体架构：**
>       采用分治思路，文档通过url计算md5，根据md5进行分布式存储，每个机器视为一个节点，可以并行工作。当发生query查询时
>       第一轮粗排序：
>           先在每个节点中找到所有匹配该query的文档，这个过程完成文档召回，这里会对文档进行一个简单的打分和去重，返回指定数目的候选文档，同时对这些选定文档进行query相关特征抽取
>       第二轮精排序：
>           使用一个核心排序函数(Core Ranking Function)打分，得到最佳的文档
>
>
>
>
>
>
>
>
>

- **用到的文档特征：**
>       用到的特征：
>           1、Web graph
>               通过www的链接情况进行文档质量打分，这里有大名鼎鼎的pagerank
>           2、Document statistics
>               一些文档相关的基础统计特征，如词频，词的数目等等
>           3、Document classifier
>               会用到一系列分类器，判断是否作弊文档，是否色情，文档语言，主题，质量和页面类型
>           4、Query features
>               词的数目，query频次和其中不同词的词频
>           5、Text match
>               包括词之间的匹配，例如(query-doc.title), (query-doc.url), (query, doc.keywords), (query, doc.abstract)等等。
>               这些特征可以进行组合形成新的特征，例如BM25. 以此判断文档和query的匹配程度
>           6、Topical matching
>               语义层面的匹配
>           7、Click
>               利用用户的点击信息，预测包括prob of click, first click, last click, long dwell time click or only click
>           8、Time
>               对于强时效性需求的query，文档的时效性要求很高
>
>
>
>
>
>
>
>

- **待续：**
>       参考：http://mlnote.com/2016/09/13/Ranking-Relevance-in-Yahoo-Search/      Ranking Relevance in Yahoo Search
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
