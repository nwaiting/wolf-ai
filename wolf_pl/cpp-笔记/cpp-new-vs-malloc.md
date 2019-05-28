## cpp-笔记 - new和malloc 区别
- **概述：**
>       new和malloc的差异：
>           1、malloc/free是标准的库函数， new/delete是操作符；
>           2、malloc/free只是分配/释放内存 ，new/delete不仅分配/释放内存还调用构造函数初始化和析构函数清理；
>           3、malloc/free手动计算类型大小，返回值void*，new/delete自动计算类型大小，返回对应类型的指针；
>           4、malloc/free失败返回0， new/delete失败抛异常
>
>       new和delete：
>           函数声明如下：
>               void* operator new(size_t size);
>               void operator delete(size_t size);
>               void* operator new[](size_t size);
>               void operator delete[](size_t size);
>           operator new/operator delete,operator new[]/operator delete[]是标准库函数，用法和malloc/free的用法一样，只负责分配/释放空间，但实际上operator new/operator delete只是malloc/free的一层封装。
>
>
>       new/delete实际上做了什么事呢？？
>           new：先调用operator new分配空间，再调用构造函数初始化空间。
>           delete：先调用析构函数清理对象，再调用operator delete释放空间。
>
>       为什么编译器会知道调用多少次构造函数，析构函数呢？
>           原来在new[]分配空间的时候会在头部多分配4个字节来存n，这样在调用new[]/delete[]时就知道调用几次构造函数和析构函数了。
>
>       new/delete，new[]/delete[]为什么要成对出现?
>           当new在开辟内置类型的空间时，不成对出现是可以的；但是当开辟非内置类型空间时，就要多开辟4个字节，这时如果不成对使用就会造成内存泄漏或者程序崩溃。
>
>       new[]/delete[]实际上做了什么事呢？
>           new[n]：调用operator new分配空间，再调用n次构造函数初始化对象。
>           delete[n]：调用n次析构函数清理对象，再调用operator delete释放空间。
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
>       参考：https://zhuanlan.zhihu.com/p/65409604
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
