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
    <li c/video/play/50/257</span><span class="video-catalog-left">(1) 第一课 自动化交易综述</span><span>(01:58:49)</span></a></li>
    /video/play/50/1035</span><span class="video-catalog-left">(2) 第1课 第1节 算法交易综述</span><span>(36:09)</span></a></li>
    /video/play/50/1036</span><span class="video-catalog-left">(3) 第1课 第2节 机器学习流程</span><span>(38:16)</span></a></li>
    /video/play/50/1037</span><span class="video-catalog-left">(4) 第1课 第3节 量化交易评估</span><span>(22:47)</span></a></li>
    /video/play/50/1038</span><span class="video-catalog-left">(5) 第1课 第4节 量化交易策略</span><span>(22:32)</span></a></li>
    /video/play/50/258</span><span class="video-catalog-left">(6) 第二课  量化交易系统综述</span><span>(01:56:09)</span></a></li>
    /video/play/50/1039</span><span class="video-catalog-left">(7) 第2课 第1节 掌握Python语言和常用的数据处理包</span><span>(25:55)</span></a></li>
    /video/play/50/1040</span><span class="video-catalog-left">(8) 第2课 第2节 量化交易技术介绍</span><span>(35:11)</span></a></li>
    /video/play/50/1041</span><span class="video-catalog-left">(9) 第2课 第3节 从技术分析到机器学习</span><span>(55:40)</span></a></li>
    /video/play/50/272</span><span class="video-catalog-left">(10) 第三课 搭建自己的量化数据库</span><span>(01:53:20)</span></a></li>
    /video/play/50/1042</span><span class="video-catalog-left">(11) 第3课 第1节 数据的获取、清理及存储</span><span>(50:54)</span></a></li>
    /video/play/50/1043</span><span class="video-catalog-left">(12) 第3课 第2节 金融策略</span><span>(38:29)</span></a></li>
    /video/play/50/1044</span><span class="video-catalog-left">(13) 第3课 第3节 机器学习途径实现</span><span>(19:56)</span></a></li>
    /video/play/50/276</span><span class="video-catalog-left">(14) 第四课 用Python进行金融数据分析</span><span>(02:02:30)</span></a></li>
    /video/play/50/1045</span><span class="video-catalog-left">(15) 第4课 第1节 OLS</span><span>(42:24)</span></a></li>
    /video/play/50/1046</span><span class="video-catalog-left">(16) 第4课 第2节 Ridge\Lasso</span><span>(42:02)</span></a></li>
    /video/play/50/1047</span><span class="video-catalog-left">(17) 第4课 第3节 Hands on sklearn</span><span>(38:38)</span></a></li>
    /video/play/50/282</span><span class="video-catalog-left">(18) 第五课 策略建模综述</span><span>(01:57:51)</span></a></li>
    /video/play/50/1048</span><span class="video-catalog-left">(19) 第5课 第1节 特征的选择及实现</span><span>(44:35)</span></a></li>
    /video/play/50/1049</span><span class="video-catalog-left">(20) 第5课 第2节 训练集和模型建立</span><span>(46:02)</span></a></li>
    /video/play/50/1050</span><span class="video-catalog-left">(21) 第5课 第3节 模型介绍</span><span>(27:50)</span></a></li>
    /video/play/50/289</span><span class="video-catalog-left">(22) 第六课 策略建模：基于机器学习的策略建模</span><span>(02:11:58)</span></a></li>
    /video/play/50/1051</span><span class="video-catalog-left">(23) 第6课 第1节 特征选择</span><span>(18:47)</span></a></li>
    /video/play/50/1052</span><span class="video-catalog-left">(24) 第6课 第2节 遗传算法</span><span>(39:22)</span></a></li>
    /video/play/50/1053</span><span class="video-catalog-left">(25) 第6课 第3节 深入理解BP算法</span><span>(46:25)</span></a></li>
    /video/play/50/1054</span><span class="video-catalog-left">(26) 第6课 第4节 RNN</span><span>(28:17)</span></a></li>
    /video/play/50/292</span><span class="video-catalog-left">(27) 第七课 模型评估与风险控制</span><span>(01:58:01)</span></a></li>
    /video/play/50/1055</span><span class="video-catalog-left">(28) 第7课 第1节 作业点评</span><span>(16:27)</span></a></li>
    /video/play/50/1056</span><span class="video-catalog-left">(29) 第7课 第2节 量化交易实战</span><span>(15:47)</span></a></li>
    /video/play/50/1057</span><span class="video-catalog-left">(30) 第7课 第3节 集成学习</span><span>(35:09)</span></a></li>
    /video/play/50/1058</span><span class="video-catalog-left">(31) 第7课 第4节 adaBoost自适应学习方法</span><span>(51:38)</span></a></li>
    /video/play/50/295</span><span class="video-catalog-left">(32) 第八课 自动交易系统的搭建</span><span>(01:50:50)</span></a></li>
    /video/play/50/1059</span><span class="video-catalog-left">(33) 第8课 第1节 极简主义的NLP与量化建模课程</span><span>(01:03:20)</span></a></li>
    /video/play/50/1060</span><span class="video-catalog-left">(34) 第8课 第2节 风险控制part I</span><span>(15:42)</span></a></li>
    /video/play/50/1061</span><span class="video-catalog-left">(35) 第8课 第3节 基于事件驱动的量化交易</span><span>(32:24)</span></a></li>
    /video/play/50/330</span><span class="video-catalog-left">(36) 第九课 量化策略的实现</span><span>(02:07:36)</span></a></li>
    /video/play/50/1062</span><span class="video-catalog-left">(37) 第9课 第1节 面试工作闲谈</span><span>(12:16)</span></a></li>
    /video/play/50/1063</span><span class="video-catalog-left">(38) 第9课 第2节 矩阵特征值</span><span>(49:04)</span></a></li>
    /video/play/50/1064</span><span class="video-catalog-left">(39) 第9课 第3节 资产组合权重</span><span>(45:37)</span></a></li>
    /video/play/50/1065</span><span class="video-catalog-left">(40) 第9课 第4节 paper</span><span>(21:09)</span></a></li>
    /video/play/50/331</span><span class="video-catalog-left">(41) 第十课 策略优化与课程总结</span><span>(01:54:34)</span></a></li>
    /video/play/50/1066</span><span class="video-catalog-left">(42) 第10课 第1节 前九课回顾</span><span>(11:27)</span></a></li>
    /video/play/50/1067</span><span class="video-catalog-left">(43) 第10课 第2节 paper 1</span><span>(25:39)</span></a></li>
    /video/play/50/1068</span><span class="video-catalog-left">(44) 第10课 第3节 paper 2</span><span>(26:12)</span></a></li>
    /video/play/50/1069</span><span class="video-catalog-left">(45) 第10课 第4节 相关国外课程推荐</span><span>(52:06)</span></a></li>
    """

sources_math = """
        /video/play/41/200</span><span class="video-catalog-left">(1) 第一课 机器学习与数学基础</span><span>(02:03:15)</span></a></li>
        /video/play/41/362</span><span class="video-catalog-left">(2) 第1课 第一节 机器学习的分类</span><span>(24:54)</span></a></li>
        /video/play/41/363</span><span class="video-catalog-left">(3) 第1课 第二节 机器学习的一般思路</span><span>(12:48)</span></a></li>
        /video/play/41/364</span><span class="video-catalog-left">(4) 第1课 第三节 微积分基础</span><span>(17:39)</span></a></li>
        /video/play/41/365</span><span class="video-catalog-left">(5) 第1课 第四节 概率与统计基础</span><span>(36:00)</span></a></li>
        /video/play/41/366</span><span class="video-catalog-left">(6) 第1课 第五节 线性代数基础</span><span>(23:05)</span></a></li>
        /video/play/41/203</span><span class="video-catalog-left">(7) 第二课 微积分选讲</span><span>(02:06:16)</span></a></li>
        /video/play/41/375</span><span class="video-catalog-left">(8) 第2课 第一节 极限</span><span>(20:50)</span></a></li>
        /video/play/41/376</span><span class="video-catalog-left">(9) 第2课 第二节 函数导数</span><span>(32:42)</span></a></li>
        /video/play/41/378</span><span class="video-catalog-left">(10) 第2课 第三节 泰勒级数逼近</span><span>(23:49)</span></a></li>
        /video/play/41/379</span><span class="video-catalog-left">(11) 第2课 第四节 牛顿法与梯度下降法</span><span>(26:53)</span></a></li>
        /video/play/41/380</span><span class="video-catalog-left">(12) 第2课 第五节 Jensen不等式</span><span>(22:26)</span></a></li>
        /video/play/41/209</span><span class="video-catalog-left">(13) 第三课 概率论选讲</span><span>(02:20:46)</span></a></li>
        /video/play/41/381</span><span class="video-catalog-left">(14) 第3课 第一节 积分学</span><span>(20:35)</span></a></li>
        /video/play/41/382</span><span class="video-catalog-left">(15) 第3课 第二节 概率空间</span><span>(41:13)</span></a></li>
        /video/play/41/383</span><span class="video-catalog-left">(16) 第3课 第三节 大数定律</span><span>(50:57)</span></a></li>
        /video/play/41/384</span><span class="video-catalog-left">(17) 第3课 第四节 中心极限定理</span><span>(28:31)</span></a></li>
        /video/play/41/211</span><span class="video-catalog-left">(18) 第四课 参数估计</span><span>(02:01:20)</span></a></li>
        /video/play/41/385</span><span class="video-catalog-left">(19) 第4课 第一节 矩估计</span><span>(15:58)</span></a></li>
        /video/play/41/386</span><span class="video-catalog-left">(20) 第4课 第二节 极大似然估计</span><span>(20:51)</span></a></li>
        /video/play/41/387</span><span class="video-catalog-left">(21) 第4课 第三节 点估计概述</span><span>(18:38)</span></a></li>
        /video/play/41/388</span><span class="video-catalog-left">(22) 第4课 第四节 评判标准</span><span>(42:24)</span></a></li>
        /video/play/41/389</span><span class="video-catalog-left">(23) 第4课 第五节 置信区间</span><span>(24:21)</span></a></li>
        /video/play/41/215</span><span class="video-catalog-left">(24) 第五课 线性代数初步</span><span>(02:01:28)</span></a></li>
        /video/play/41/390</span><span class="video-catalog-left">(25) 第5课 第一节 线性空间与基</span><span>(25:13)</span></a></li>
        /video/play/41/391</span><span class="video-catalog-left">(26) 第5课 第二节 矩阵作为线性映射的代数表达方式</span><span>(34:40)</span></a></li>
        /video/play/41/392</span><span class="video-catalog-left">(27) 第5课 第三节 线性方程的几何意义</span><span>(14:55)</span></a></li>
        /video/play/41/393</span><span class="video-catalog-left">(28) 第5课 第四节 方程求解、几何逼近中的线性回归</span><span>(22:20)</span></a></li>
        /video/play/41/394</span><span class="video-catalog-left">(29) 第5课 第五节 最小二乘法</span><span>(25:25)</span></a></li>
        /video/play/41/217</span><span class="video-catalog-left">(30) 第六课 线性代数进阶</span><span>(02:25:37)</span></a></li>
        /video/play/41/485</span><span class="video-catalog-left">(31) 第6课 第一节 相似变换</span><span>(38:03)</span></a></li>
        /video/play/41/486</span><span class="video-catalog-left">(32) 第6课 第二节 相合变换</span><span>(12:46)</span></a></li>
        /video/play/41/487</span><span class="video-catalog-left">(33) 第6课 第三节 正交相似变换</span><span>(22:07)</span></a></li>
        /video/play/41/488</span><span class="video-catalog-left">(34) 第6课 第四节 主成分分析</span><span>(33:27)</span></a></li>
        /video/play/41/489</span><span class="video-catalog-left">(35) 第6课 第五节 PCA例子</span><span>(41:15)</span></a></li>
        /video/play/41/222</span><span class="video-catalog-left">(36) 第七课 凸优化初步</span><span>(02:20:27)</span></a></li>
        /video/play/41/490</span><span class="video-catalog-left">(37) 第7课 第一节 优化与凸优化简介</span><span>(15:21)</span></a></li>
        /video/play/41/491</span><span class="video-catalog-left">(38) 第7课 第二节 凸集合与凸函数的关系</span><span>(29:46)</span></a></li>
        /video/play/41/492</span><span class="video-catalog-left">(39) 第7课 第三节 凸组合</span><span>(19:41)</span></a></li>
        /video/play/41/493</span><span class="video-catalog-left">(40) 第7课 第四节 集合相交</span><span>(10:52)</span></a></li>
        /video/play/41/494</span><span class="video-catalog-left">(41) 第7课 第五节 线性组合与微分</span><span>(12:29)</span></a></li>
        /video/play/41/495</span><span class="video-catalog-left">(42) 第7课 第六节 光学投影</span><span>(13:20)</span></a></li>
        /video/play/41/496</span><span class="video-catalog-left">(43) 第7课 第七节 凸集分离定理</span><span>(20:10)</span></a></li>
        /video/play/41/497</span><span class="video-catalog-left">(44) 第7课 第八节 凸优化问题举例</span><span>(20:40)</span></a></li>
        /video/play/41/223</span><span class="video-catalog-left">(45) 第八课 凸优化进阶</span><span>(02:29:30)</span></a></li>
        /video/play/41/498</span><span class="video-catalog-left">(46) 第8课 第一节 共轭函数</span><span>(21:22)</span></a></li>
        /video/play/41/499</span><span class="video-catalog-left">(47) 第8课 第二节 拉格朗日对偶函数</span><span>(30:36)</span></a></li>
        /video/play/41/500</span><span class="video-catalog-left">(48) 第8课 第三节 共轭函数与拉格朗日对偶函数</span><span>(18:22)</span></a></li>
        /video/play/41/501</span><span class="video-catalog-left">(49) 第8课 第四节 对偶性</span><span>(17:28)</span></a></li>
        /video/play/41/502</span><span class="video-catalog-left">(50) 第8课 第五节 应用举例</span><span>(21:31)</span></a></li>
        /video/play/41/503</span><span class="video-catalog-left">(51) 第8课 第六节 总结寄语</span><span>(36:24)</span></a></li>
        /video/play/41/228</span><span class="video-catalog-left">(52) 第九课 从数学到机器学习分类问题</span><span>(02:11:46)</span></a></li>
        /video/play/41/506</span><span class="video-catalog-left">(53) 第9课 第一节 定义与问题引入</span><span>(24:31)</span></a></li>
        /video/play/41/507</span><span class="video-catalog-left">(54) 第9课 第二节 损失函数与梯度下降</span><span>(36:04)</span></a></li>
        /video/play/41/508</span><span class="video-catalog-left">(55) 第9课 第三节 从线性回归到分类</span><span>(12:35)</span></a></li>
        /video/play/41/509</span><span class="video-catalog-left">(56) 第9课 第四节 逻辑回归</span><span>(26:51)</span></a></li>
        /video/play/41/510</span><span class="video-catalog-left">(57) 第9课 第五节 多分类，Softmax与LinearSVM</span><span>(32:55)</span></a></li>
        /video/play/41/229</span><span class="video-catalog-left">(58) 第十课 深入理解SVM</span><span>(01:44:07)</span></a></li>
        /video/play/41/511</span><span class="video-catalog-left">(59) 第10课 第一节 课程前瞻</span><span>(15:11)</span></a></li>
        /video/play/41/512</span><span class="video-catalog-left">(60) 第10课 第二节 最大间隔与决策公式</span><span>(13:33)</span></a></li>
        /video/play/41/513</span><span class="video-catalog-left">(61) 第10课 第三节 目标函数与优化理论</span><span>(32:57)</span></a></li>
        /video/play/41/514</span><span class="video-catalog-left">(62) 第10课 第四节 核方法</span><span>(21:47)</span></a></li>
        /video/play/41/515</span><span class="video-catalog-left">(63) 第10课 第五节 Hinge loss及课程回顾</span><span>(21:33)</span></a></li>
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
    for item in [sources_urls_lianghua,sources_graph_practice,sources_url_math]:
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
                        time.sleep(0.5)
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
