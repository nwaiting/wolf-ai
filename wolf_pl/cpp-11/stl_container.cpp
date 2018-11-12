#include <iostream>

/*
    容器：是一种数据结构，有3种，顺序性容器(vector、deque、list)，关联容器(map、set)，容器适配器(queue,stack)
        1、顺序性容器
            vector：高效的随机存取，插入和删除效率低
            list：高效的插入和删除，随机存取效率低
            deque：随机存取、插入、删除效率平衡（内存空间分布是小片的连续，小片间用链表相连，deque空间的重新分配要比vector快，因为原来的元素不需要拷贝）
        2、关联容器 
            map
            set
        3、容器适配器
            deque：FIFO队列，是在deque基础上封装的
            stack：FILO先进后出，是在deque基础上封装的
*/

int main()
{
    return 0;
}
