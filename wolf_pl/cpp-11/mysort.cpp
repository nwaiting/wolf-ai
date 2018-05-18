#include <iostream>
#include <algorithm>
#include <stdlib.h>
using namespace std;

/*
    qsort和sort的区别：  
        qsort：
        include<stdlib.h>
        （基本快速排序的方法，每次把数组分成两部分和中间的一个划分值，而对于有多个重复值的数组来说，基本快速排序的效率较低，且不稳定）。集成在C语言库函数里面的的qsort函数，使用 三 路划分的方法解决排序这个问题。所谓三路划分，是指把数组划分成小于划分值，等于划分值和大于划分值的三个部分。
        具体介绍：-^^
            void qsort(void *base, int nelem, int width, int (*fcmp)(const void *,const void *)); 
            int compare (const void *elem1, const void *elem2 ) );

        qsort（即，quicksort）主要根据你给的比较条件给一个快速排序，主要是通过指针移动实现排序功能。排序之后的结果仍然放在原来数组中。
        参数意义如下:
            第一个参数 base 是 需要排序的目标数组名（或者也可以理解成开始排序的地址，因为可以写&s[i]这样的表达式）
            第二个参数 num 是 参与排序的目标数组元素个数
            第三个参数 width 是单个元素的大小（或者目标数组中每一个元素长度），推荐使用sizeof(s[0]）这样的表达式
            第四个参数 compare 就是让很多人觉得非常困惑的比较函数啦。

        sort：
            include<algorithm>
            sort是qsort的升级版，如果能用sort尽量用sort，使用也比较简单，不像qsort还得自己去写 cmp 函数
            与qsort同为排序函数，复杂度为n*log2(n)
            std::sort函数优于qsort的一些特点：对大数组采取9项取样，更完全的三路划分算法，更细致的对不同数组大小采用不同方法排序
*/
void func1()
{

}

int main()
{
    cin.get();
    return 0;
}
