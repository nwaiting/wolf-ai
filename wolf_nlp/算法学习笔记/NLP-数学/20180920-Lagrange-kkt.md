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

- **对偶问题：**
>       将某类数学结构A转换为另一种对等的数学结构B。
>       在优化问题中，可以将非凸问题转化为凸优化问题进行求解。
>
>       Lagrange对偶问题是指对于原问题 min f(x)，通过构造对偶函数g(u,v)，然后最大化该对偶函数的优化问题，即max g(u,v)
>
>       对于原问题的对偶问题，有两个重要性质：
>           1、弱对偶性
>               无论是凸优化或非凸优化原问题，f*>=g*（因为f(x)>=g(x)）称为**弱对偶性**
>              强对偶性
>               如果我们获得f*=g*，那么就可以保证求解对偶问题获得的最优解可以变换为原问题的最优解
>               将f*=g*形式称为**强对偶性**
>           2、对偶问题是凸优化问题
>               无论原问题是凸优化还是非凸，对偶问题永远是凸优化问题，
>               对于非凸问题一般无法获得或者较难获得其对偶问题的表达式g(u,v)
>
>       强对偶性条件：
>           如果原问题为凸优化问题，同时存在至少一个可行解满足h1(x)<0,h2(x)<0,...,hm(x<0),l1(x)=...=lr(x)=0，
>           那么该问题的强对偶性成立，即f*=g*
>
>       对偶间隙：
>           对偶间隙的最大用途是作为算法停止迭代的条件，即如果我们需要保证f(x)-f*<=ϵ，那么需要f(x)-g(u,v)<=ϵ
>
>
>

- **SMO优化：**
>       SMO算法由1998年提出，并成为最快的二次规划优化算法，特别针对线性SVM和数据稀疏时性能更优。
>           SMO之所以高效，是因为在固定其他参数后，对一个参数优化过程很高效。
>       SMO VS 坐标上升法：
>           SMO算法的思想与坐标上升法的思想类似。
>           坐标上升算法每次通过更新多元函数中的一维，经过多次迭代直到收敛来达到优化函数的目的。
>               即不断选中一个变量做一维最优化直到函数达到局部最优解
>
>           如果我们依然按照坐标上升算法来求解最优解，因为a1,a2,...,an之间有约束关系，所以当其他的变量固定的时候，剩下的一个变量也就是常量了（可以由约束条件计算出），
>           因此一次选取两个参数做优化，比如a1和a2，此时a2可以由a1和其他参数表示出来，然后回带入到W中，则W就只是a1的表达式，就可以解出结果了。
>
>
>
>
>
>


- **KKT条件：**
>       KKT条件：
>           KKT来源于三个人们缩写，主要研究不等约束下的最优化问题，所以叫kkt条件
>       KKT条件是拉格朗日乘子法的推广，
>       如果去掉不等式的约束部分，那么就是Laglange乘子法的精确表达。
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
>           https://www.zhihu.com/question/23311674     非线性优化中的 KKT 条件该如何理解？
>           https://zhuanlan.zhihu.com/p/26514613   浅谈最优化问题的KKT条件
>           http://www.hanlongfei.com/convex/2015/11/05/duality/    凸优化-对偶问题(讲解的比较通俗易懂)
>           http://www.cnblogs.com/jerrylead/archive/2011/03/18/1988419.html    支持向量机（五）SMO算法（参考SMO作者的论文）
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
