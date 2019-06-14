## cpp-笔记 - 高级特性
- **概述：**
>
>

- **__attribute__属性：**
>       __atrribute__ 是一个编译器指令，它指定声明的特征，允许更多的错误检查和高级优化
>           关键字__attribute__后跟两组括号（双括号使“宏输出”变得容易，尤其是多个属性）
>           括号内是逗号分隔的属性列表。__attribute__指令放在函数，变量和类型声明之后
>       例子：
>           GUARDED_BY(mutex_) THREAD_ANNOTATION_ATTRIBUTE__(guarded_by(mutex_)) __attribute__((guarded_by(mutex_))
>           guarded_by属性是为了保证线程安全，使用该属性后，线程要使用相应变量，必须先锁定mutex_，使得变量是原子操作 
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
>       参考：
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
