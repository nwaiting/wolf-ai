### elasticsearch
- **概述：**
>
>
>
>
>

- **rest查询：**
>       查询格式：
>           http:localhost:9200/my_index/my_type
>           即：http:localhost:9200/数据库/表
>           http:localhost:9200/my_index/my_type/1
>           即：http:localhost:9200/数据库/表/第几个
>
>       http使用方法：
>           get：用get的话，不管什么放肆都是查询全部
>           podt：post方法
>
>       查询语句：
>           https://blog.csdn.net/m_z_g_y/article/details/82628972      ElasticSearch入门：常用查询方法（python）
>           https://www.cnblogs.com/shaosks/p/7592229.html      Python 操作 ElasticSearch
>           https://www.jb51.net/article/156935.htm     Python-ElasticSearch搜索查询的讲解
>           https://blog.csdn.net/qq_15260769/article/details/87918578      ElasticSearch查询方法（python）
>

- **bool查询关键词：**
>       must	查询的结果必须匹配查询条件，并计算score
>       filter	查询的结果必须匹配查询条件，和must不同不会计算score
>       should	查询结果必须符合查询条件中的一个或多个
>       must_not	查询结果必须不符合查询条件
>
>

- **多条件查询案例：**
>       https://www.jianshu.com/p/1dd593186e19      es同个字段，多个值搜索的案例
>
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/ykkBlog/p/4667857.html
>           https://blog.csdn.net/dm_vincent/article/details/41820537
>           https://blog.csdn.net/m_z_g_y/article/details/82628972      ElasticSearch入门：常用查询方法（python）
>           https://www.jianshu.com/p/56cfc972d372    Flask 教程 第十六章：全文搜索
>           https://blog.csdn.net/weixin_43031412/article/details/100011282     Elasticsearch 搜索API
>
>           https://blog.csdn.net/R_P_J/article/details/78376622      第三篇 elasticsearch的group by+avg+sort等聚合分析
>
>           https://www.jianshu.com/p/1e970765198c      使用es布尔查询进行多条件查询
>
>           https://www.jianshu.com/p/1dd593186e19      es同个字段，多个值搜索的案例
>
>           https://n3xtchen.github.io/n3xtchen/elasticsearch/2017/07/05/elasticsearch-23-useful-query-example  19 个很有用的 ElasticSearch 查询语句
>
>           https://www.cnblogs.com/leeSmall/p/9215909.html     elasticsearch系列六：聚合分析（聚合分析简介、指标聚合、桶聚合）
>           https://www.cnblogs.com/Neeo/articles/10615739.html     elasticsearch for Python之操作篇
>
>
>
>
>
>
>
