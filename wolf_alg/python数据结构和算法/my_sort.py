#coding=utf-8



"""
    https://www.cnblogs.com/clement-jiao/p/9243066.html     python sort函数内部实现原理
    http://blog.donews.com/maverick/archive/2006/07/19/968616.aspx  学习笔记：Sample Sort

    python的sorted和list.sort()的区别：
        sorted：
            lista经过sorted之后，得到一个排序结果，但是，原有的lista并没有受到影响
        list.sort：
            经过list.sort()之后，原有a的顺序已经发生变化，与上述不同之处
        在list.sort()和sorted中，都可以根据指定的key值排序

    python的sorted原理：
        python中的sorted排序，真的是高大上，用的Timsort算法

    python 的内部排序算法 list.sort：
        1.5.2版本前，都是使用ansi c的qsort，但不同平台上的qsort实现不同，也造成python的排序效果的不一致
        1.5.2版本后，python自己实现了排序算法，不再使用qsort
        python对不同情况的数据自动采用不同的排序算法：
            首先检查数据是否已经排序(或reverse sorted)了，O(N)，如果有，那么就直接返回了
            如果已经基本排序了，就使用binary insertion sort算法
            1、如果数据集很小（小于100个），那么就使用binary insertion sort算法；
            2、如果数据集很大，就会使用samplesort

    1、Binary Insertion Sort：
        binary insertion sort与普通的插入排序算法基本一样，只是在确定插入位置时使用binary search算法
        折半插入排序, 即查找插入点的位置, 可以使用折半查找
        可以减少比较的次数,移动的次数不变, 时间复杂度仍为O(n^2)


    2、samplesort：
        大小为s的样本从n元素的序列中选取，并且选择样本排序后m-1个元素确定桶的范围。这些元素（称为分离器(splitter)）用来分离m个大小相等的桶。
        ！！！！！确定桶的范围后，该算法变成了一般方式的桶排序。！！！！！！！！
        样本排序的性能取决于样本的大小s和从n个元素中选定样本的方式。！！！
        基本思想：
            1、用P-1个分隔值（splitter），将序列分散到P个bucket（桶）中。
            2、每个Processor（处理器）按照这些分隔值，把元素送到合适的bucket中。
            3、对每个桶排序，归并。

        具体算法过程：
            1、为每个processor分配n/p个元素
            2、每个processor对自己分配的元素排序
            3、每个processor从自己分配的元素中选出p-1个分隔元素，将已排序元素分隔为平等的p段
            4、将每个processor选出的分隔元素（共有p(p-1)个）合并，再从中选出p-1个分隔元素，将这p(p-1)个元素平分为p段
            5、以上一步选出的p-1个元素为界限，每个processor分配给自己的元素划分为p段
            6、每个processor将位于自己第i段的元素送到编号为i的processor
            7、使用radix sort（基数排序）对这些bucket进行排序，即先对每个bucket排序，再按顺序将各个bucket中的元素收集起来。


    3、Timsort：
        结合了合并排序（merge sort）和插入排序（insertion sort）而得出的排序算法
        TimSort 算法为了减少对升序部分的回溯和对降序部分的性能倒退，将输入按其升序和降序特点进行了分区
        算法过程：
            1、如何数组长度小于某个值，直接用二分插入排序算法
            2、找到各个run，并入栈
            3、按规则合并run

    4、桶排序：
        桶排序(bucket sort)算法是一种流行的串行算法，用于排序包含n个元素数组，其值在区间[a, b]上匀分布。
        在该算法中，区间[a, b]被分为m个大小相等的子区间称为桶，并且每个元素被放置在适当的桶中。由于n个元素在区间[a, b]上均匀分布，每个桶的元素数目大致为n/m。然后，该排序算法对每个桶中的元素进行排序。
        缺点：
            在大多数情况下，实际的输入可以不具有这样的分布，或它的分布可能是未知的。因此，使用桶排序可能会导致各个桶中的元素数量显著不同，从而降低排序性能。！！！！
            优化：
                在这种情况下的使用称为样本排序(Sample Sort)的算法将产生更显著的性能。


    并行算法一般有几种思路：
        Centralize：
            （由一个中心节点统一管理协调所有节点，拓扑结构为星型，易于理解，但要求子任务相对独立，对中心节点的依赖程度很高）；
        Network：
            节点之间互相通信协调，拓扑结构为完全图，好处是易于实现，各节点的算法相通，但通信效率低，成本高）
        Ring：
            各节点处于同一个环上，拓扑结构为环形，通信效率高，但整体速度很慢）
    SampleSort应该是综合了Centralize和Network两种思路的算法


"""







def main():
    pass








if __name__ == '__main__':
    main()
