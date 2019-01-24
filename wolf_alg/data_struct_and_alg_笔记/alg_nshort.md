## data_struct_and_alg 笔记 - NShortPath基本思想是Dijkstra算法的变种
- **概述：**
>       N最短路径分词算法是一种基于词典的分词算法。每个句子将生成一个有向无环图，每一个字作为图的一个顶点，边代表可能的分词权重。
>       N表示N条路径
>
>
>

- **算法详解：**
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nshort1.png)
> 
>       如图，计算过程如下：
>       (1)、首先将最后一个元素压入堆栈(例如6号节点)，当这个元素弹出时任务结束。
>       (2)、对于每个节点的PreNode队列，维护了一个当前指针，初始状态都指向PreNode队列中第一个元素
>       (3)、从右向左依次取出PreNode队列中的当前元素并压入堆栈，并将队列指针重新指向队列中第一个元素（例如6号元素preNode是3,3号preNode是1,1号preNode是0）
>       (4)、当第一个元素压入堆栈后，输出堆栈内容即为一条队列（本例中0,1,3,6便是一条路径）
>       (5)、将堆栈内容依次弹出，没弹出一个元素，就将当时压堆栈时对应的PreNode队列指针下移一格。如果到了末尾无法继续下移，则继续执行第5步，如果仍然可以移动，则执行第3步
>
>       对于本例中，先将0弹出堆栈，该元素对应是1号A节点的PreNode队列，该队列的当前指针已经无法下移，因此继续弹出堆栈中的"1"；该元素对应3号"C"节点，因此将3号"C"节点对应的PreNode队列指针下移。
>           由于可以移动，因此将队列中的2压入堆栈，2号"B"节点的PreNode是1，因此再压入1，依次类推，直到0被压入，此时又得到了一条最短路径，就是0,1,2,3,6。如下图：
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nshort2.png)
>
>       再往下，0,1,2都被弹出堆栈，3被弹出堆栈后，由于它对应的6号元素preNode队列记录指针仍然可以下移，因此将5压入堆栈并依次将其PreNode入栈，直到0被入栈。
>           此时输出第3条最短路径:0,1,2,4,5,6。如下图：
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/nshort3.png)
>
>       输出完成后，紧接着又是出栈，此时已经没有任何堆栈元素对应的PreNode队列指针可以下移，于是堆栈中的最后一个元素6也被弹出堆栈，此时输出工作完全结束。最后我们得出3条最短路径，分别为：
>           0,1,3,6
>           0,1,2,3,6
>           0,1,2,4,5,6
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
>       参考：https://www.cnblogs.com/zhenyulu/articles/669795.html
>           https://www.cnblogs.com/Finley/p/6619187.html
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
