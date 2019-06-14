## cpp-笔记 - iterator
- **概述：**
>
>
>

- **iterator失效处理：**
>       一般会有两种办法：
>           1、it=my_container.erase(it);
>
>           2、my_container.erase(iter++);
>               my_container.erase(iter++);这句话分三步走，先把iter传值到erase里面，然后iter自增，然后执行erase,所以iter在失效前已经自增了
>
>       C++标准中，顺序容器的erase函数会返回iterator，但关联容器的erase函数不返回iterator
>           1、对于顺序容器 vector、deque，删除当前的iterator会使后面所有元素的iterator都失效。
>               这是因为vector、deque使用了连续分配的内存，删除一个元素导致后面所有的元素会向前移动一个位置。erase方法可以返回下一个有效的iterator。
>           2、对于关联容器map、set、multimap、multiset，删除当前的iterator，仅仅会使当前的iterator失效，只要在erase时，递增当前iterator即可。
>               这是因为map之类的容器，使用了红黑树来实现，插入、删除一个结点不会对其他结点造成影响
>           3、对于顺序容器list，erase方法可以返回下一个有效的iterator。
>               由于list是一个链表，删除当前的iterator，仅仅会使当前的iterator失效，所以也可以在erase时，递增当前的iterator
>       在STL中，不能以指针来看待迭代器，指针是与内存绑定的，而迭代器是与容器里的元素绑定的。
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
>       参考：https://blog.csdn.net/u010318270/article/details/78575371    C++ STL 迭代器失效问题的剖析
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
>
>
>
>
