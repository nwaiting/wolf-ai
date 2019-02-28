### NLP_数学 -- 拉格朗日乘子法和KKT条件
- **概述**：
>       在求解有约束条件的最优化问题中，两种最常用的方法：
>           1、拉格朗日乘子法：
>               有等式约束时使用拉格朗日乘子法
>           2、KKT：
>               如果含有不等式约束时使用KKT条件
>           这两个方法求得的结果只是必要条件，只有当是凸函数的时候，才能保证是充分必要条件
>           **KKT条件是拉格朗日乘子法的泛化**
>
>

- **等高线：**
>       如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nlp_math_Lagrange_contour.jpg)
>
>       Lagrange乘子α的含义是约束条件边界直线的法向量与目标函数等高线的法向量是共线向量。
>           目标函数的梯度可以表示为约束条件的梯度展开的向量空间，系数为Lagrange乘子α和β，继续增加限制条件，结论是一致的。
>       Lagrange乘子α，如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nlp_math_Lagrange_a_mean.jpg)
>
>       Lagrange乘子α和β，如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nlp_math_Lagrange_a_b_mean.jpg)
>
>       Lagrange乘子α和β的曲线图，如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nlp_math_Lagrange_a_b_graph.jpg)
>
>
>

- **待续：**
>       参考：https://kknews.cc/zh-sg/other/r32k6lo.html   支持向量机（三）：图解KKT条件和拉格朗日乘子法
>           https://www.matongxue.com/madocs/987/   如何理解拉格朗日乘子法和KKT条件？
>           https://zhuanlan.zhihu.com/p/55719829   图解KKT条件和拉格朗日乘子法
>           https://zhuanlan.zhihu.com/p/27731819   为什么梯度的方向与等高线切线方向垂直？
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
