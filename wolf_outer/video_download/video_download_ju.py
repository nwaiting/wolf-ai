#coding=utf-8

import requests
import os
import time
import sys
import urlparse

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

sources_ml = """
    /video/play/67/615</span><span class="video-catalog-left">(1) 第1课（上）微积分</span><span>(02:03:32)</span></a></li>
    /video/play/67/1316</span><span class="video-catalog-left">(2) 第1课（下）概率论</span><span>(02:04:46)</span></a></li>
    /video/play/67/617</span><span class="video-catalog-left">(3) 第2课（上） 线性代数</span><span>(03:14:10)</span></a></li>
    /video/play/67/1317</span><span class="video-catalog-left">(4) 第2课（下） 凸优化</span><span>(01:38:30)</span></a></li>
    /video/play/67/620</span><span class="video-catalog-left">(5) 第3课 回归问题与应用</span><span>(02:16:48)</span></a></li>
    /video/play/67/625</span><span class="video-catalog-left">(6) 第4课 决策树、随机森林、GBDT</span><span>(01:50:09)</span></a></li>
    /video/play/67/659</span><span class="video-catalog-left">(7) 第5课 SVM</span><span>(01:53:17)</span></a></li> http://v3.julyedu.com/video/67/659/3f8cb40619.m3u8  http://v3.julyedu.com/video/67/659/3f8cb40619-00001.ts
    /video/play/67/641</span><span class="video-catalog-left">(8) 第6/video/play/67/1358</span><span class="video-catalog-left">(9) 第6课 最大熵与EM算法（下）</span><span>(02:07:04)</span></a></li>
    /video/play/67/639</span><span class="video-catalog-left">(10) 第7课 机器学习中的特征工程处理</span><span>(02:18:09)</span></a></li>
    /video/play/67/666</span><span class="video-catalog-left">(11) 第8课 多算法组合与模型最优化</span><span>(02:08:40)</span></a></li>
    /video/play/67/676</span><span class="video-catalog-left">(12) 第9课 sklearn与机器学习实战</span><span>(01:52:04)</span></a></li>
    /video/play/67/677</span><span class="video-catalog-left">(13) 第10课 高级工具xgboost/lightGBM与建模实战</span><span>(02:12:19)</span></a></li>
    /video/play/67/682</span><span class="video-catalog-left">(14) 第11课 用户画像与推荐系统</span><span>(01:54:57)</span></a></li>
    /video/play/67/685</span><span class="video-catalog-left">(15) 第12课 聚类</span><span>(01:57:19)</span></a></li>
    /video/play/67/692</span><span class="video-catalog-left">(16) 第13课 聚类与推荐系统实战</span><span>(01:42:14)</span></a></li>
    /video/play/67/695</span><span class="video-catalog-left">(17) 第14课 贝叶斯网络</span><span>(01:50:42)</span></a></li>
    /video/play/67/696</span><span class="video-catalog-left">(18) 第15课 隐马尔科夫模型HMM</span><span>(01:50:27)</span></a></li>
    /video/play/67/697</span><span class="video-catalog-left">(19) 第16课 主题模型</span><span>(02:01:10)</span></a></li>
    /video/play/67/702</span><span class="video-catalog-left">(20) 第17课 神经网络初步</span><span>(01:53:25)</span></a></li>
    /video/play/67/706</span><span class="video-catalog-left">(21) 第18课 卷积神经网络与计算机视觉</span><span>(02:10:04)</span></a></li>
    /video/play/67/708</span><span class="video-catalog-left">(22) 第19课 循环神经网络与自然语言处理</span><span>(01:48:31)</span></a></li>
    /video/play/67/714</span><span class="video-catalog-left">(23) 第20课 深度学习实践</span><span>(01:46:37)</span></a></li>
    """
sources_langhua=u"""
    """

sources_math = """
"""

sources_others = """
    /video/play/27/19</span><span class="video-catalog-left">(1) 实战动态规划（直播coding）</span><span>(33:45)</span></a></li>
    /video/play/27/23</span><span class="video-catalog-left">(2) 排序查找实战（直播coding）</span><span>(30:05)</span></a></li>
    /video/play/27/34</span><span class="video-catalog-left">(3) 图搜索实战（直播coding）</span><span>(33:25)</span></a></li>
    /video/play/27/81</span><span class="video-catalog-left">(4) 数组实战（直播coding）</span><span>(35:24)</span></a></li>
    /video/play/27/82</span><span class="video-catalog-left">(5) 字符串实战（直播coding）</span><span>(36:45)</span></a></li>
    /video/play/27/83</span><span class="video-catalog-left">(6) 链表实战（直播coding）</span><span>(27:12)</span></a></li>
    /video/play/27/166</span><span class="video-catalog-left">(7) 树实战（直播coding）</span><span>(29:22)</span></a></li>
"""

sources_urls = ["第1课（上）微积分,http://v3.julyedu.com/video/67/615/585b7925ff.m3u8",
            "第1课（下）概率论,http://v3.julyedu.com/video/67/1316/8fc04380c4.m3u8",
            "第2课（上） 线性代数,http://v3.julyedu.com/video/67/617/689129cdec.m3u8",
            "第2课（下） 凸优化,http://v3.julyedu.com/video/67/1317/65fed5fa90.m3u8",
            "第3课 回归问题与应用,http://v3.julyedu.com/video/67/620/f45c5d2d88.m3u8",
            "第4课 决策树、随机森林、GBDT,http://v3.julyedu.com/video/67/625/3738907e1b.m3u8",
            "第5课 SVM,http://v3.julyedu.com/video/67/659/3f8cb40619.m3u8",
            "第6课 最大熵与EM算法（上）,http://v3.julyedu.com/video/67/641/ee810d8f85.m3u8",
            "第6课 最大熵与EM算法（下）,http://v3.julyedu.com/video/67/1358/35d55e1522.m3u8",
            "第7课 机器学习中的特征工程处理,http://v3.julyedu.com/video/67/639/b708635864.m3u8",
            "第8课 多算法组合与模型最优化,http://v3.julyedu.com/video/67/666/299d366254.m3u8",
            "第9课 sklearn与机器学习实战,http://v3.julyedu.com/video/67/676/d524c0c2e8.m3u8",
            "第10课 高级工具xgboost/lightGBM与建模实战,http://v3.julyedu.com/video/67/677/2dc0222e0b.m3u8",
            "第11课 用户画像与推荐系统,http://v3.julyedu.com/video/67/682/cc4990c83f.m3u8",
            "第12课 聚类,http://v3.julyedu.com/video/67/685/4096fbe221.m3u8",
            "第13课 聚类与推荐系统实战,http://v3.julyedu.com/video/67/692/f9f91cd421.m3u8",
            "第14课 贝叶斯网络,http://v3.julyedu.com/video/67/695/5dfe57e51f.m3u8",
            "第15课 隐马尔科夫模型HMM,http://v3.julyedu.com/video/67/696/89bab3178f.m3u8",
            "第16课 主题模型,http://v3.julyedu.com/video/67/697/357374ff1d.m3u8",
            "第17课 神经网络初步,http://v3.julyedu.com/video/67/702/1ce717ac40.m3u8",
            "第18课 卷积神经网络与计算机视觉,http://v3.julyedu.com/video/67/706/44462aa908.m3u8",
            "第19课 循环神经网络与自然语言处理,http://v3.julyedu.com/video/67/708/cf9fd481fc.m3u8",
            "第20课 深度学习实践,http://v3.julyedu.com/video/67/714/a90b06c249.m3u8"
            ]

sources_urls_lianghua = [
            "第一课 自动化交易综述,http://v2.julyedu.com/ts/50/257/aeca23b0.m3u8",
            "第1课 第1节 算法交易综述,http://v3.julyedu.com/video/50/1035/2109aa4d02.m3u8",
            "第1课 第2节 机器学习流程,http://v3.julyedu.com/video/50/1036/a96887c6fe.m3u8",
            "第1课 第3节 量化交易评估,http://v3.julyedu.com/video/50/1037/b61bed5042.m3u8",
            "第1课 第4节 量化交易策略,http://v3.julyedu.com/video/50/1038/0b7d757dcd.m3u8",
            "第二课  量化交易系统综述,http://v2.julyedu.com/ts/50/258/84d5561a.m3u8",
            "第2课 第1节 掌握Python语言和常用的数据处理包,http://v3.julyedu.com/video/50/1039/8d7c5decb4.m3u8",
            "第2课 第2节 量化交易技术介绍,http://v3.julyedu.com/video/50/1040/cb9e1359af.m3u8",
            "第2课 第3节 从技术分析到机器学习,http://v3.julyedu.com/video/50/1041/ccf4f9377b.m3u8",
            "第三课 搭建自己的量化数据库,http://v2.julyedu.com/ts/50/272/e5e8e7c1.m3u8",
            "第3课 第1节 数据的获取、清理及存储,http://v3.julyedu.com/video/50/1042/170fe23506.m3u8",
            "第3课 第2节 金融策略,http://v3.julyedu.com/video/50/1043/a0c80102d2.m3u8",
            "第3课 第3节 机器学习途径实现,http://v3.julyedu.com/video/50/1044/928ea0a153.m3u8",
            "第四课 用Python进行金融数据分析,http://v2.julyedu.com/ts/50/276/2da8211b.m3u8",
            "第4课 第1节 OLS,http://v3.julyedu.com/video/50/1045/477588d414.m3u8",
            "第4课 第2节 Ridge Lasso,http://v3.julyedu.com/video/50/1046/66ef7b6b6b.m3u8",
            "第4课 第3节 Hands on sklearn,http://v3.julyedu.com/video/50/1047/80091a3986.m3u8",
            "第五课 策略建模综述,http://v2.julyedu.com/ts/50/282/6942f4dd.m3u8",
            "第5课 第1节 特征的选择及实现,http://v3.julyedu.com/video/50/1048/9337aeac4d.m3u8",
            "第5课 第2节 训练集和模型建立,http://v3.julyedu.com/video/50/1049/75e54e685d.m3u8",
            "第5课 第3节 模型介绍,http://v3.julyedu.com/video/50/1050/f1e4a55b38.m3u8",
            "第六课 策略建模：基于机器学习的策略建模,http://v2.julyedu.com/ts/50/289/3777c529.m3u8",
            "第6课 第1节 特征选择,http://v3.julyedu.com/video/50/1051/b018e35f9d.m3u8",
            "第6课 第2节 遗传算法,http://v3.julyedu.com/video/50/1052/c1b0ee6b38.m3u8",
            "第6课 第3节 深入理解BP算法,http://v3.julyedu.com/video/50/1053/b5c63f67ad.m3u8",
            "第6课 第4节 RNN,http://v3.julyedu.com/video/50/1054/b4cf80cd8d.m3u8",
            "第七课 模型评估与风险控制,http://v2.julyedu.com/ts/50/292/e49e786f.m3u8",
            "第7课 第1节 作业点评,http://v3.julyedu.com/video/50/1055/085c88a2e3.m3u8",
            "第7课 第2节 量化交易实战,http://v3.julyedu.com/video/50/1056/2bdc3f9ada.m3u8",
            "第7课 第3节 集成学习,http://v3.julyedu.com/video/50/1057/52cb5ffd90.m3u8",
            "第7课 第4节 adaBoost自适应学习方法,http://v3.julyedu.com/video/50/1058/842cd0ded0.m3u8",
            "第八课 自动交易系统的搭建,http://v2.julyedu.com/ts/50/295/e5a17d46.m3u8",
            "第8课 第1节 极简主义的NLP与量化建模课程,http://v3.julyedu.com/video/50/1059/8f5a36b28e.m3u8",
            "第8课 第2节 风险控制part I,http://v3.julyedu.com/video/50/1060/dcd604f3e1.m3u8",
            "第8课 第3节 基于事件驱动的量化交易,http://v3.julyedu.com/video/50/1061/03ad64acb3.m3u8",
            "第九课 量化策略的实现,http://v2.julyedu.com/ts/50/330/6ce12602.m3u8",
            "第9课 第1节 面试工作闲谈,http://v3.julyedu.com/video/50/1062/5330279e8d.m3u8",
            "第9课 第2节 矩阵特征值,http://v3.julyedu.com/video/50/1063/8910caf30b.m3u8",
            "第9课 第3节 资产组合权重,http://v3.julyedu.com/video/50/1064/b04f090070.m3u8",
            "第9课 第4节 paper,http://v3.julyedu.com/video/50/1065/3d24e1e3a2.m3u8",
            "第十课 策略优化与课程总结,http://v2.julyedu.com/ts/50/331/86dcef5d.m3u8",
            "第10课 第1节 前九课回顾,http://v3.julyedu.com/video/50/1066/5e8b2be2f7.m3u8",
            "第10课 第2节 paper 1,http://v3.julyedu.com/video/50/1067/544dacf5c0.m3u8",
            "第10课 第3节 paper 2,http://v3.julyedu.com/video/50/1068/01d80c4759.m3u8",
            "第10课 第4节 相关国外课程推荐,http://v3.julyedu.com/video/50/1069/24b667140d.m3u8"
            ]

sources_graph_practice = [
            "第1课 图搜索实战班第1讲,http://v2.julyedu.com/ts/51/263/c300c1ee.m3u8",
            "第2课 图搜索实战班第2讲,http://v2.julyedu.com/ts/51/266/13c9d5bc.m3u8",
            "第1课 动态规划实战班第1讲,http://v2.julyedu.com/ts/48/246/c60bc444.m3u8",
            "第2课 动态规划实战班第2讲,http://v2.julyedu.com/ts/48/250/a2fd47b5.m3u8",
            "第1课 算法初步,http://v2.julyedu.com/ts/61/481/ffa59f24.m3u8",
            "第2课 必知必会的数据结构,http://v2.julyedu.com/ts/61/483/a4474359.m3u8",
            "第3课 树堆,http://v3.julyedu.com/video/61/504/dd2f1cbc0f.m3u8",
            "第4课 图论,http://v2.julyedu.com/ts/61/505/e49f3bb8.m3u8",
            "第5课 递归,http://v2.julyedu.com/ts/61/516/aec54b21.m3u8",
            "第6课 图搜索初探,http://v2.julyedu.com/ts/61/521/e633c494.m3u8",
            "第7课 动态规划,http://v3.julyedu.com/video/61/589/160ffb027c.m3u8",
            "第8课 贪心,http://v3.julyedu.com/video/61/593/66ead2e1ac.m3u8",
            "第9课 高并发-海量数据处理-笔试技巧,http://v3.julyedu.com/video/61/598/4763333f8d.m3u8",
            "第10课 博弈论-概率-数论,http://v3.julyedu.com/video/61/601/777a614d0b.m3u8",
            "第20课 概率图模型初步,http://v2.julyedu.com/ts/35/205/de49656f.m3u8",
            "第1课 数据科学与数学基础,http://v2.julyedu.com/ts/40/191/175d6e5a.m3u8",
            "第2课 数据处理-分析-可视化,http://v2.julyedu.com/ts/40/192/4639f96a.m3u8",
            "第3课 海量数据的分布式处理,http://v2.julyedu.com/ts/40/195/39ed847e.m3u8",
            "第4课 关联规则挖掘,http://v2.julyedu.com/ts/40/196/795969fe.m3u8",
            "第5课 数据与聚类,http://v2.julyedu.com/ts/40/202/86531d03.m3u8",
            "第6课 海量高维数据与近似最近邻,http://v2.julyedu.com/ts/40/204/e25fbaf2.m3u8",
            "第7课 分类与排序,http://v2.julyedu.com/ts/40/210/255577a5.m3u8",
            "第8课 推荐系统,http://v2.julyedu.com/ts/40/212/6c9ab65c.m3u8",
            "第9课 海量高维数据与维度约减,http://v2.julyedu.com/ts/40/216/654799ab.m3u8",
            "第10课 PageRank与图挖掘,http://v2.julyedu.com/ts/40/218/7540c896.m3u8"
            ]

sources_url_math = [
            "第一课 机器学习与数学基础,http://v2.julyedu.com/ts/41/200/23c11e9a.m3u8",
            "第1课 第一节 机器学习的分类,http://v2.julyedu.com/ts/41/362/7a3ee27d.m3u8",
            "第1课 第二节 机器学习的一般思路,http://v2.julyedu.com/ts/41/363/22c80044.m3u8",
            "第1课 第三节 微积分基础,http://v2.julyedu.com/ts/41/364/d7e4b8b6.m3u8",
            "第1课 第四节 概率与统计基础,http://v2.julyedu.com/ts/41/365/13142e36.m3u8",
            "第1课 第五节 线性代数基础,http://v2.julyedu.com/ts/41/366/c4bed529.m3u8",
            "第二课 微积分选讲,http://v2.julyedu.com/ts/41/203/1e930019.m3u8",
            "第2课 第一节 极限,http://v2.julyedu.com/ts/41/375/66353831.m3u8",
            "第2课 第二节 函数导数,http://v2.julyedu.com/ts/41/376/cab5120c.m3u8",
            "第2课 第三节 泰勒级数逼近,http://v2.julyedu.com/ts/41/378/1c4928bb.m3u8",
            "第2课 第四节 牛顿法与梯度下降法,http://v2.julyedu.com/ts/41/379/47397e67.m3u8",
            "第2课 第五节 Jensen不等式,http://v2.julyedu.com/ts/41/380/c0d3a530.m3u8",
            "第三课 概率论选讲,http://v2.julyedu.com/ts/41/209/f6a3413a.m3u8",
            "第3课 第一节 积分学,http://v2.julyedu.com/ts/41/381/270204d6.m3u8",
            "第3课 第二节 概率空间,http://v2.julyedu.com/ts/41/382/5c275763.m3u8",
            "第3课 第三节 大数定律,http://v2.julyedu.com/ts/41/383/af62e22e.m3u8",
            "第3课 第四节 中心极限定理,http://v2.julyedu.com/ts/41/384/325f8437.m3u8",
            "第四课 参数估计,http://v2.julyedu.com/ts/41/211/0dd2dda4.m3u8",
            "第4课 第一节 矩估计,http://v2.julyedu.com/ts/41/385/0d308488.m3u8",
            "第4课 第二节 极大似然估计,http://v2.julyedu.com/ts/41/386/df16eb94.m3u8",
            "第4课 第三节 点估计概述,http://v2.julyedu.com/ts/41/387/ae5ecfba.m3u8",
            "第4课 第四节 评判标准,http://v2.julyedu.com/ts/41/388/9ebeb72d.m3u8",
            "第4课 第五节 置信区间,http://v2.julyedu.com/ts/41/389/a36907f1.m3u8",
            "第五课 线性代数初步,http://v2.julyedu.com/ts/41/215/8e92d875.m3u8",
            "第5课 第一节 线性空间与基,http://v2.julyedu.com/ts/41/390/2994c697.m3u8",
            "第5课 第二节 矩阵作为线性映射的代数表达方式,http://v2.julyedu.com/ts/41/391/cce4d05e.m3u8",
            "第5课 第三节 线性方程的几何意义,http://v2.julyedu.com/ts/41/392/a4c1f754.m3u8",
            "第5课 第四节 方程求解、几何逼近中的线性回归,http://v2.julyedu.com/ts/41/393/9b91611f.m3u8",
            "第5课 第五节 最小二乘法,http://v2.julyedu.com/ts/41/394/b40af143.m3u8",
            "第六课 线性代数进阶,http://v2.julyedu.com/ts/41/217/275d900f.m3u8",
            "第6课 第一节 相似变换,http://v2.julyedu.com/ts/41/485/655b07e1.m3u8",
            "第6课 第二节 相合变换,http://v2.julyedu.com/ts/41/486/998a39c8.m3u8",
            "第6课 第三节 正交相似变换,http://v2.julyedu.com/ts/41/487/48186779.m3u8",
            "第6课 第四节 主成分分析,http://v2.julyedu.com/ts/41/488/ce40cbc2.m3u8",
            "第6课 第五节 PCA例子,http://v2.julyedu.com/ts/41/489/bd22607f.m3u8",
            "第七课 凸优化初步,http://v2.julyedu.com/ts/41/222/b7853943.m3u8",
            "第7课 第一节 优化与凸优化简介,http://v2.julyedu.com/ts/41/490/121c4f57.m3u8",
            "第7课 第二节 凸集合与凸函数的关系,http://v2.julyedu.com/ts/41/491/fe7628fc.m3u8",
            "第7课 第三节 凸组合,http://v2.julyedu.com/ts/41/492/2f97ac9c.m3u8",
            "第7课 第四节 集合相交,http://v2.julyedu.com/ts/41/493/fafe10fb.m3u8",
            "第7课 第五节 线性组合与微分,http://v2.julyedu.com/ts/41/494/0cd72564.m3u8",
            "第7课 第六节 光学投影,http://v2.julyedu.com/ts/41/495/ea9977cd.m3u8",
            "第7课 第七节 凸集分离定理,http://v2.julyedu.com/ts/41/496/185211a1.m3u8",
            "第7课 第八节 凸优化问题举例,http://v2.julyedu.com/ts/41/497/d785ab51.m3u8",
            "第八课 凸优化进阶,http://v2.julyedu.com/ts/41/223/801e7027.m3u8",
            "第8课 第一节 共轭函数,http://v2.julyedu.com/ts/41/498/f90db9c0.m3u8",
            "第8课 第二节 拉格朗日对偶函数,http://v2.julyedu.com/ts/41/499/a96518fb.m3u8",
            "第8课 第三节 共轭函数与拉格朗日对偶函数,http://v2.julyedu.com/ts/41/500/67677aaf.m3u8",
            "第8课 第四节 对偶性,http://v2.julyedu.com/ts/41/501/1d49d086.m3u8",
            "第8课 第五节 应用举例,http://v2.julyedu.com/ts/41/502/29e1703c.m3u8",
            "第8课 第六节 总结寄语,http://v2.julyedu.com/ts/41/503/1ac0d2f1.m3u8",
            "第九课 从数学到机器学习分类问题,http://v2.julyedu.com/ts/41/228/b8541444.m3u8",
            "第9课 第一节 定义与问题引入,http://v2.julyedu.com/ts/41/506/9810c0e1.m3u8",
            "第9课 第二节 损失函数与梯度下降,http://v2.julyedu.com/ts/41/507/57c128c9.m3u8",
            "第9课 第三节 从线性回归到分类,http://v2.julyedu.com/ts/41/508/2d233ee4.m3u8",
            "第9课 第四节 逻辑回归,http://v2.julyedu.com/ts/41/509/dfd3633d.m3u8",
            "第9课 第五节 多分类，Softmax与LinearSVM,http://v2.julyedu.com/ts/41/510/692d64ef.m3u8",
            "第十课 深入理解SVM,http://v2.julyedu.com/ts/41/229/b9c39f67.m3u8",
            "第10课 第一节 课程前瞻,http://v2.julyedu.com/ts/41/511/f76e37da.m3u8",
            "第10课 第二节 最大间隔与决策公式,http://v2.julyedu.com/ts/41/512/d2c3c0a4.m3u8",
            "第10课 第三节 目标函数与优化理论,http://v2.julyedu.com/ts/41/513/782d2527.m3u8",
            "第10课 第四节 核方法,http://v2.julyedu.com/ts/41/514/5ec9b408.m3u8",
            "第10课 第五节 Hinge loss及课程回顾,http://v2.julyedu.com/ts/41/515/9dc31300.m3u8",
            "论文公开课 第一期 随机梯度下降算法综述,http://v3.julyedu.com/video/69/646/e93a886e99.m3u8",
            "论文公开课 第二期 深度学习中的归一化,http://v3.julyedu.com/video/69/686/6463661235.m3u8",
            "论文公开课 第三期 AlphaGo Zero背后的算法,http://v3.julyedu.com/video/69/794/553ab8fd79.m3u8"
            ]

sources_url_others = [
            "(1) 实战动态规划（直播coding）,http://v2.julyedu.com/ts/27/19/888ddc11.m3u8",
            "(2) 排序查找实战（直播coding）,http://v2.julyedu.com/ts/27/23/91c2a83b.m3u8",
            "(3) 图搜索实战（直播coding）,http://v2.julyedu.com/ts/27/34/26f136fb.m3u8",
            "(4) 数组实战（直播coding）,http://v2.julyedu.com/ts/27/81/c34ee1e3.m3u8",
            "(5) 字符串实战（直播coding）,http://v2.julyedu.com/ts/27/82/8c1a3ec6.m3u8",
            "(6) 链表实战（直播coding）,http://v2.julyedu.com/ts/27/83/aa550b8a.m3u8",
            "(7) 树实战（直播coding）,http://v2.julyedu.com/ts/27/166/9d1cb8c2.m3u8",
            "概率统计-第1课 概率论基础,http://v3.julyedu.com/video/68/619/5bf7d175c9.m3u8",
            "概率统计-第2课 参数估计,http://v3.julyedu.com/video/68/623/cf296ffd06.m3u8",
            "概率统计-第3课 参数估计的渐进性质,http://v3.julyedu.com/video/68/635/3362eb01c2.m3u8",
            "概率统计-第4课 概率统计在机器学习中的应用,http://v3.julyedu.com/video/68/640/f5fc05c8fc.m3u8",
            "数学第二期-第一课：微分学基本概念,http://v3.julyedu.com/video/106/928/0098d622f9.m3u8",
            "数学第二期-第二课：微分学进阶,http://v3.julyedu.com/video/106/929/0670b39ab0.m3u8",
            "数学第二期-第三课：概率论简介,http://v3.julyedu.com/video/106/930/e183c6dcc6.m3u8",
            "数学第二期-第四课：极大似然估计,http://v3.julyedu.com/video/106/931/cbfd0c2578.m3u8",
            "数学第二期-第五课：线性代数基础(唐博士),http://v3.julyedu.com/video/106/932/df8eefdb50.m3u8",
            "数学第二期-第六课：线性代数进阶(唐博士),http://v3.julyedu.com/video/106/933/9940cd4a03.m3u8",
            "数学第二期-第七课：凸优化简介,http://v3.julyedu.com/video/106/934/4dbece0638.m3u8",
            "数学第二期-第八课：优化的稳定性,http://v3.julyedu.com/video/106/935/4916516d77.m3u8",
            "数学第二期-第九课：从线性模型谈起的机器学习分类与回归,http://v3.julyedu.com/video/106/937/07e66669a8.m3u8",
            "数学第二期-第十课：从信息论到工业界最爱的树模型,http://v3.julyedu.com/video/106/938/e89acfacdb.m3u8",
            "Tensorflow基础-第1课 Tensorflow基础,http://v3.julyedu.com/video/86/718/85144b4f82.m3u8",
            "Tensorflow基础-第2课 详解深度神经网络案例,http://v3.julyedu.com/video/86/720/dc3b1ae716.m3u8",
            "Tensorflow基础-第3课 卷积神经网络与图像应用,http://v3.julyedu.com/video/86/724/5309058c84.m3u8",
            "Tensorflow基础-第4课 海量图像训练预处理,http://v3.julyedu.com/video/86/725/93208e12a3.m3u8",
            "Tensorflow基础-第5课 循环神经网络与应用,http://v3.julyedu.com/video/86/728/4e392ec3e9.m3u8",
            "Tensorflow基础-第6课 Tensorboard工具与模型优化,http://v3.julyedu.com/video/86/729/d711ac7749.m3u8",
            "Tensorflow基础-第7课 Tensorflow应用案例,http://v3.julyedu.com/video/86/738/3c9d1adcfa.m3u8",
            "Tensorflow基础-第8课 Tensorflow之上的工具库,http://v3.julyedu.com/video/86/730/ecb9b1c95e.m3u8",
            "NLP课程-第1课 NLP理论基础,http://v2.julyedu.com/ts/55/324/dcacf215.m3u8",
            "NLP课程-第2课 Word2Vec理论基础,http://v2.julyedu.com/ts/55/325/023ea87d.m3u8",
            "NLP课程-第3课 Word2Vec实战案例课-Kaggle竞赛案例,http://v2.julyedu.com/ts/55/332/eeb0163b.m3u8",
            "NLP课程-第4课 从Word2Vec到FastText的新发展+案例,http://v2.julyedu.com/ts/55/333/99d72976.m3u8",
            "机器学习算法-词嵌入word embedding,http://v2.julyedu.com/ts/35/156/e7c4357c.m3u8",
            "机器学习算法-第1课 机器学习与微积分,http://v2.julyedu.com/ts/35/162/c065228c.m3u8",
            "机器学习算法-第2课 数理统计和参数估计,http://v2.julyedu.com/ts/35/163/20eb6e6f.m3u8",
            "机器学习算法-第3课 矩阵分析与应用,http://v2.julyedu.com/ts/35/164/17763d6e.m3u8",
            "机器学习算法-第4课 凸优化初步,http://v2.julyedu.com/ts/35/165/6b754fd6.m3u8",
            "机器学习算法-第5课 线性回归与逻辑回归,http://v2.julyedu.com/ts/35/167/68c33175.m3u8",
            "机器学习算法-第6课 特征工程,http://v2.julyedu.com/ts/35/168/c35af50e.m3u8",
            "机器学习算法-第7课 工作流程与模型调优,http://v2.julyedu.com/ts/35/169/81672be7.m3u8",
            "机器学习算法-第8课 最大熵与EM算法,http://v2.julyedu.com/ts/35/172/ccf8ee8e.m3u8",
            "机器学习算法-第9课 推荐系统,http://v2.julyedu.com/ts/35/174/e7b10fe3.m3u8",
            "机器学习算法-第10课 聚类算法与应用,http://v2.julyedu.com/ts/35/176/fe2358fb.m3u8",
            "机器学习算法-第11课 决策树、随机森林、Adaboost,http://v2.julyedu.com/ts/35/179/f9b788d2.m3u8",
            "机器学习算法-第12课 SVM,http://v2.julyedu.com/ts/35/182/bc70f821.m3u8",
            "机器学习算法-第13课 贝叶斯方法,http://v2.julyedu.com/ts/35/185/8445a50c.m3u8",
            "机器学习算法-第14课 主题模型,http://v2.julyedu.com/ts/35/188/778cd10f.m3u8",
            "机器学习算法-第15课 采样与变分,http://v2.julyedu.com/ts/35/193/513eb1c3.m3u8",
            "机器学习算法-第16课 人工神经网络,http://v2.julyedu.com/ts/35/194/5b488172.m3u8",
            "机器学习算法-第17课 卷积神经网络,http://v2.julyedu.com/ts/35/197/92ce8ab5.m3u8",
            "机器学习算法-第18课 循环神经网络与LSTM,http://v2.julyedu.com/ts/35/198/a762a365.m3u8",
            "机器学习算法-第19课 关于框架,http://v2.julyedu.com/ts/35/201/0920f308.m3u8",
            "机器学习算法-第20课 概率图模型初步,http://v2.julyedu.com/ts/35/205/de49656f.m3u8",
            "矩阵与凸优化-第1课 理解矩阵,http://v2.julyedu.com/ts/62/517/9d827dbc.m3u8",
            "矩阵与凸优化-第2课 理解微积分和凸优化,http://v2.julyedu.com/ts/62/520/50b7d57c.m3u8",
            "矩阵与凸优化-第3课 微积分与逼近论,http://v3.julyedu.com/video/62/588/db23c2d0ef.m3u8",
            "矩阵与凸优化-第4课 凸优化初步,http://v3.julyedu.com/video/62/592/9fc334adef.m3u8",
            "矩阵与凸优化-第5课 凸优化进阶,http://v3.julyedu.com/video/62/596/14014212c5.m3u8",
            "矩阵与凸优化-第6课 凸优化在机器学习中的应用,http://v3.julyedu.com/video/62/602/78a7f9f507.m3u8"
            ]

sources_chatbot_list = [
            "聊天机器人第1课 聊天机器人的基础模型与综述,http://v3.julyedu.com/video/64/590/e18268eb86.m3u8",
            "聊天机器人第2课 NLP基础及扫盲,http://v3.julyedu.com/video/64/591/a776b32a13.m3u8",
            "聊天机器人第3课 用基础机器学习方法制作聊天机器人,http://v3.julyedu.com/video/64/597/37e1ab59ef.m3u8",
            "聊天机器人第4课 深度学习基础及扫盲,http://v3.julyedu.com/video/64/600/f16fe0646b.m3u8",
            "聊天机器人第5课 深度学习聊天机器人原理,http://v3.julyedu.com/video/64/604/39b6531118.m3u8",
            "聊天机器人第6课 用深度学习方法制作聊天机器人,http://v3.julyedu.com/video/64/606/4b9408b359.m3u8",
            "聊天机器人第7课 看图回答VQA,http://v3.julyedu.com/video/64/622/5d74bc66be.m3u8",
            "聊天机器人第8课 简单易用的聊天机器人开发平台与展望,http://v3.julyedu.com/video/64/626/706f6f2e55.m3u8"
            ]

sources_last_all = [
            "推荐系统实战-掌握BAT推荐系统和常用算法-第1课 推荐系统简介,http://v3.julyedu.com/video/127/1448/c75f2a6d1d.m3u8",
            "推荐系统实战-掌握BAT推荐系统和常用算法-第2课 召回算法和业界最佳实践(一),http://v3.julyedu.com/video/127/1449/c1802687bc.m3u8",
            "推荐系统实战-掌握BAT推荐系统和常用算法-第3课 召回算法和业界最佳实践(二),http://v3.julyedu.com/video/127/1450/19c96a344c.m3u8",
            "推荐系统实战-深入BAT内部推荐&排序架构-第4课 用户建模(召回、排序都会用到),http://v3.julyedu.com/video/127/1451/9680984a58.m3u8",
            "推荐系统实战-深入BAT内部推荐&排序架构-第5课 重排序算法：Learning to Rank,http://v3.julyedu.com/video/127/1453/7440e162b9.m3u8",
            "推荐系统实战-深入BAT内部推荐&排序架构-第6课 排序算法&amp;深度学习模型（一）,http://v3.julyedu.com/video/127/1452/81ee8a365c.m3u8",
            "推荐系统实战-深入BAT内部推荐&排序架构-第7课 排序算法&amp;深度学习模型（二）,http://v3.julyedu.com/video/127/1627/642fa18647.m3u8",
            "推荐系统实战-深入BAT内部推荐&排序架构-第8课 学术界最新算法在BAT的应用,http://v3.julyedu.com/video/127/1454/ba6d30fa8a.m3u8",
            "推荐系统实战-通晓Online Learning和业务场景推荐-第9课 实时化技术升级,http://v3.julyedu.com/video/127/1455/b0e75ee6f3.m3u8",
            "推荐系统实战-通晓Online Learning和业务场景推荐-第10课 掌握真实业务场景下的推荐算法,http://v3.julyedu.com/video/127/1456/66ab942657.m3u8",
            "深度学习项目班-神经网络初步,http://v3.julyedu.com/video/107/1070/50a233b28d.m3u8",
            "深度学习项目班-卷积神经网络与计算机视觉,http://v3.julyedu.com/video/107/1071/1c4e7703b0.m3u8",
            "深度学习项目班-第一课 深度卷积神经网络基础(原理、调参、Kaggle比赛实践),http://v3.julyedu.com/video/107/940/18deef9100.m3u8",
            "深度学习项目班-第二课 深度学习在大规模图像搜索中的实际应用,http://v3.julyedu.com/video/107/941/2dd258becd.m3u8",
            "深度学习项目班-第三课 自然语言处理从入门到进阶,http://v3.julyedu.com/video/107/942/f3f45cae01.m3u8",
            "深度学习项目班-第四课 聊天机器人实战演练,http://v3.julyedu.com/video/107/943/2a5e7742da.m3u8",
            "深度学习项目班-第五课 从FM到DNN到wide&amp;deep model,http://v3.julyedu.com/video/107/944/7029c5469b.m3u8",
            "深度学习项目班-第六课 FNN CCPM PNN与图片混合点击率预估,http://v3.julyedu.com/video/107/945/ded423aaec.m3u8",
            "深度学习项目班-第七课 从矩阵分解到FM_based_NN,http://v3.julyedu.com/video/107/946/3fa05f44fe.m3u8",
            "深度学习项目班-第八课 从CCF神经网络到Deep_Auto-encoder_for_CF,http://v3.julyedu.com/video/107/947/c8a49da9e5.m3u8",
            "语音识别技术的前世今生-GMM-HMM,http://v3.julyedu.com/video/104/916/8cb6338d66.m3u8",
            "语音识别技术的前世今生-神经网络,http://v3.julyedu.com/video/104/917/10ffa52f8c.m3u8",
            "量化交易策略实战-第1课 量化交易基础,http://v3.julyedu.com/video/103/885/7ff7697ce8.m3u8",
            "量化交易策略实战-第2课 衍生品及交易策略A,http://v3.julyedu.com/video/103/886/ed77136a83.m3u8",
            "量化交易策略实战-第3课 衍生品及交易策略B,http://v3.julyedu.com/video/103/887/f34c6b9b25.m3u8",
            "量化交易策略实战-第4课 统计套利,http://v3.julyedu.com/video/103/888/3a1e350450.m3u8",
            "Python基础入门升级版-第1课 Python入门,http://v3.julyedu.com/video/101/800/8e19e9a74b.m3u8",
            "Python基础入门升级版-第2课 关键字，容器及访问，循环控制,http://v3.julyedu.com/video/101/801/09f0cc3018.m3u8",
            "Python基础入门升级版-第3课:函数,http://v3.julyedu.com/video/101/802/1972dd68ca.m3u8",
            "Python基础入门升级版-第4课 面向对象基础,http://v3.julyedu.com/video/101/803/6c65444e36.m3u8",
            "Python基础入门升级版-第5课 文件操作，并发编程及常用系统模块,http://v3.julyedu.com/video/101/804/1ca9b967cd.m3u8",
            "Python基础入门升级版-第6课 常用第三方模块及综合实战,http://v3.julyedu.com/video/101/805/5b8e3f76e4.m3u8",
            "Python基础入门升级版-第7课 Numpy高效数据处理,http://v3.julyedu.com/video/101/806/bbd9366740.m3u8",
            "Python基础入门升级版-第8课 Pandas 表格处理,http://v3.julyedu.com/video/101/807/06e2d23287.m3u8",
            "深度学习论文班-Hinton两篇奠基性的文章，开启深度学习的新纪元-第1课,http://v3.julyedu.com/video/98/774/9ff6bbf3dc.m3u8",
            "深度学习论文班-Hinton两篇奠基性的文章，开启深度学习的新纪元-第2课,http://v3.julyedu.com/video/98/773/a0a758cd6c.m3u8",
            "深度学习论文班-CNN的在图像分类上的重要应用与理论阐释-第3课,http://v3.julyedu.com/video/98/777/7300cb95e2.m3u8",
            "深度学习论文班-CNN的在图像分类上的重要应用与理论阐释-第4课,http://v3.julyedu.com/video/98/776/100d30885f.m3u8",
            "深度学习论文班-CNN的最新进展以及RNN在语音识别上的应用-第5课,http://v3.julyedu.com/video/98/775/3e15c75059.m3u8",
            "深度学习论文班-CNN的最新进展以及RNN在语音识别上的应用-第6课,http://v3.julyedu.com/video/98/778/562605dc1e.m3u8",
            "深度学习论文班-深度模型的训练方法与理论的两项突破性进展-第7课,http://v3.julyedu.com/video/98/779/02f4eb0aa7.m3u8",
            "深度学习论文班-深度模型的训练方法与理论的两项突破性进展-第8课,http://v3.julyedu.com/video/98/780/d166c7e4f1.m3u8",
            "强化学习-第1课 强化学习RL简介,http://v3.julyedu.com/video/93/756/64bf495daa.m3u8",
            "强化学习-第2课 Model—Free Learning,http://v3.julyedu.com/video/93/759/c985d3e276.m3u8",
            "强化学习-第3课 Model-Free Control,http://v3.julyedu.com/video/93/764/16d862e0bc.m3u8",
            "强化学习-第4课 Q-Learning,http://v3.julyedu.com/video/93/765/38c21ad4a6.m3u8",
            "强化学习-第5课 策略梯度学习,http://v3.julyedu.com/video/93/770/6e3ea5f8c0.m3u8",
            "强化学习-第6课 TensorFlow强化学习应用案例,http://v3.julyedu.com/video/93/771/24c6294380.m3u8",
            "迁移学习-第1课 迁移学习详解,http://v3.julyedu.com/video/89/739/a6c8e51117.m3u8",
            "迁移学习-第2课 迁移学习实战,http://v3.julyedu.com/video/89/740/f08c906c4e.m3u8",
            "生成对抗网络-第1课 生成对抗网络基本原理,http://v3.julyedu.com/video/90/746/3b8df29d77.m3u8",
            "生成对抗网络-第2课 多种多样的GAN,http://v3.julyedu.com/video/90/747/c66a607ddd.m3u8",
            "生成对抗网络-第3课 基于能量的GAN,http://v3.julyedu.com/video/90/752/a40ed079eb.m3u8",
            "生成对抗网络-第4课 GAN实战,http://v3.julyedu.com/video/90/757/30f4178406.m3u8",
            "深度学习-第一课 夯实深度学习数据基础,http://v3.julyedu.com/video/79/693/2910927b05.m3u8",
            "深度学习-第二课 DNN与混合网络：google Wide&amp;Deep,http://v3.julyedu.com/video/79/694/a3f6fe829e.m3u8",
            "深度学习-第三课 CNN:从AlexNet到ResNet,http://v3.julyedu.com/video/79/699/2412587396.m3u8",
            "深度学习-第四课 NN框架：caffe, tensorflow与pytorch,http://v3.julyedu.com/video/79/704/7f40203ad5.m3u8",
            "深度学习-第五课 生成对抗网络GAN,http://v3.julyedu.com/video/79/707/3fcbaa8ead.m3u8",
            "深度学习-第六课 图像风格转化,http://v3.julyedu.com/video/79/710/8f2db3eee3.m3u8",
            "深度学习-第七课 RNN/LSTM/Grid LSTM,http://v3.julyedu.com/video/79/713/1bd8f9cbdb.m3u8",
            "深度学习-第八课 RNN条件生成与attention,http://v3.julyedu.com/video/79/716/a138800c35.m3u8",
            "深度学习-第九课 增强学习与Deep Q Network,http://v3.julyedu.com/video/79/719/6df8dfd817.m3u8",
            "深度学习-第十课 物体检测与迁移学习,http://v3.julyedu.com/video/79/721/9b146b8b96.m3u8",
            "机器学习项目班-第1课 音乐推荐系统_(上),http://v3.julyedu.com/video/70/660/442d041970.m3u8",
            "机器学习项目班-第2课 音乐推荐系统_(下),http://v3.julyedu.com/video/70/662/4ea81c5e41.m3u8",
            "机器学习项目班-第3课 神经网络实现机器翻译,http://v3.julyedu.com/video/70/674/e3d5ef60b4.m3u8",
            "机器学习项目班-第4课 基于pytorch的风格转换,http://v3.julyedu.com/video/70/679/75e2bd6187.m3u8",
            "机器学习项目班-第5课 文本主题与分类_(上),http://v3.julyedu.com/video/70/681/fa62cb7280.m3u8",
            "机器学习项目班-第6课 文本主题与分类_(下),http://v3.julyedu.com/video/70/684/2a1da5b15c.m3u8",
            "机器学习项目班-第7课 电商点击率预估_(上),http://v3.julyedu.com/video/70/689/57a27016bc.m3u8",
            "机器学习项目班-第8课 电商点击率预估_(下),http://v3.julyedu.com/video/70/690/5857f0f437.m3u8",
            "机器学习项目班-第9课 视觉聊天机器人,http://v3.julyedu.com/video/70/698/d6ca8fe6f3.m3u8",
            "机器学习项目班-第10课 金融反欺诈模型训练,http://v3.julyedu.com/video/70/700/18835048da.m3u8"
            ]

#条件随机场的视频
crf_addr = ["http://www.kengso.com/s?wd=machine+learning%E9%82%B9%E5%8D%9A%E7%9A%84%E8%AF%BE%E7%A8%8B-%E4%B8%83%E6%9C%88%E7%AE%97%E6%B3%95+%E6%9D%A1%E4%BB%B6%E9%9A%8F%E6%9C%BA%E5%9C%BA%28%E4%B8%8B%29.flv&st=0&p=1",
            "https://pan.baidu.com/share/home?uk=891979294&suk=LJYNPU2zf_8xpr4caS07EA#category/type=0"] #百度个人主页

#七月的条件随机场
jl_crf = "https://www.bilibili.com/video/av26119295/?p=9"

#炼数成金自然语言处理
bilibili_addr = "https://www.bilibili.com/video/av27183045/?p=84"

#邹博图、树等数据结构和动态规划等算法
zb_addr = ["https://www.bilibili.com/video/av18109226/?spm_id_from=333.788.videocard.11"]

#邹博比较早的机器学习课程
bilibili_addr2 = "https://www.bilibili.com/video/av23416351/?p=13"

def parse_titles():
    with open('parse.txt', 'wb') as f:
        for line in sources_math.split('\n'):
            #time.sleep(1)
            line = line.strip('\r\n ')
            find_index = line.find(')')
            if find_index != -1:
                line = line[find_index+1:].strip()
                find_index = line.find('<')
                if find_index != -1:
                    print(u"\"{0},\"".format(line[:find_index].strip()))
                    f.write("\"{0},\"\n".format(line[:find_index].strip()))

def dts(url, save_file):
    chunk_size = 1024 * 1024
    res = requests.get(url)
    with open(save_file, 'wb') as f:
        for chunk in res.iter_content(chunk_size):
            f.write(chunk)

def main():
    url_pre = "http://v3.julyedu.com/video"
    for line in sources_urls:
        title = None
        title_url = None
        line_item = None
        try:
            items = line.strip().split(',')
            if len(items) == 2:
                title = items[0]
                title_url = items[1]
                zh_dir_path = items[0].decode('utf-8').encode('gbk')
                if not os.path.exists(zh_dir_path):
                    try:
                        os.mkdir(zh_dir_path)
                    except Exception as e:
                        print("error mkdir {0}".format(e))
                m3u8_url = url_pre + items[1]
                print(os.path.basename(items[1]))
                print(os.path.dirname(items[1]))
                res = requests.get(m3u8_url)

                with open(os.path.join(zh_dir_path,"m3u8.m3u8"), 'w') as f:
                    f.write(res.text)

                for res_line in res.text.split('\n'):
                    if res_line.startswith('#'):
                        continue
                    time.sleep(0.5)
                    res_line = res_line.strip('\r\n ')
                    line_item = res_line
                    ts_url = url_pre + os.path.dirname(items[1]) + '/' + res_line
                    file_name = os.path.join(items[0].decode('utf-8').encode('utf-8'),res_line)
                    print(ts_url, file_name)
                    dts(ts_url, file_name)
        except Exception as e:
            print("error {0}".format(e))
            with open(error_file, 'a') as f:
                f.write("{0},{1},{2}\n".format(title, title_url, line_item))

def downnew():
    for item in [sources_urls_lianghua,sources_graph_practice,sources_url_math,sources_url_others]:
        for line in item:
            title = None
            title_url = None
            line_item = None
            try:
                items = line.strip().split(',')
                if len(items) == 2:
                    title = items[0]
                    title_url = items[1]
                    zh_dir_path = items[0].decode('utf-8').encode('gbk')
                    if not os.path.exists(zh_dir_path):
                        try:
                            os.mkdir(zh_dir_path)
                        except Exception as e:
                            print("error mkdir {0}".format(e))

                    res = requests.get(item[1].strip())
                    with open(os.path.join(zh_dir_path,"m3u8.m3u8"), 'w') as f:
                        f.write(res.text)

                    # add new url pre
                    m3u8_url = item[1].strip()
                    url_items = urlparse.urlparse(m3u8_url)
                    url_last = os.path.basename(url_items.path)
                    new_url_pre = m3u8_url.replace(url_last, '')

                    for res_line in res.text.split('\n'):
                        if res_line.startswith('#'):
                            continue
                        time.sleep(0.1)
                        res_line = res_line.strip('\r\n ')
                        line_item = res_line

                        ts_url = new_url_pre + res_line
                        file_name = os.path.join(items[0],res_line)
                        if os.path.exists(file_name):
                            continue
                        print(ts_url, file_name)
                        dts(ts_url, file_name)
            except Exception as e:
                print("error {0}".format(e))
                with open(error_file, 'a') as f:
                    f.write("{0},{1},{2}\n".format(title, title_url, line_item))

if __name__ == '__main__':
    error_file = 'error.txt'
    #main()
    #parse_titles()
    #downnew()
