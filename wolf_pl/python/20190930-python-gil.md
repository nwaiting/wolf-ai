## python - gil
- **概述：**
>       gil(Global Interpreter Lock)
>       在 CPython 中, 全局解释器锁, 或者 GIL, 是一把互斥锁, 这把互斥锁被用来保护 python 对象, 防止多个线程同时执行 python 字节码.。
>       这把锁是有存在的必要的, 主要原因是 CPython 的内存管理机制在实现的时候是非线程安全的(因为GIL的存在, 很多第三方的扩展和功能在写的时候都深度的依赖这把锁, 更加加深了对 GIL 的依赖)
>

- **python特点：**
>       python的目标不是一个性能高效的语言，出于脚本动态类型的原因虚拟机做了大量计算来判断一个变量的当前类型，并且整个python虚拟机是基于栈逻辑的，频繁的压栈出栈操作也需要大量计算。
>       动态类型变化导致python的性能优化非常困难，尽管如此python在编译阶段还是在操作码层做了简单的peephole(窥空优化)。
>
>

- **opcode：**
>       opcode又称为操作码，是将python源代码进行编译之后的结果，python虚拟机无法直接执行human-readable的源代码，因此python编译器第一步先将源代码进行编译，以此得到opcode。
>           例如在执行python程序时一般会先生成一个pyc文件，pyc文件就是编译后的结果，其中含有opcode序列。
>
>       dis是python提供的对操作码进行分析的内置模块。
>           其中LOAD_CONST，STORE_FAST，BINARY_ADD即是我们提到的opcode，**python是基于栈的语言**，LOAD_CONST是将常量进行压栈，SOTRE_FAST是将栈顶元素赋值给参数指定的变量。
>           LOAD_CONST 0 表示将co_consts中的第0个（下标0）放入栈中。
>           STORE_FAST 0 表示将栈顶元素赋值给co_names中存放的第0个元素。
>       python 2.7版中共计定义了约110个操作码，其中90以上的操作码需要参数，操作码定义参见opcode.h
>
>
>       1、不是所有的 opcode 执行之前都会检查 gil_drop_request 的, 有一些 opcode 结束时的代码为 FAST_DISPATCH(), 这部分 opcode 会直接跳转到下一个 opcode 对应的代码的部分进行执行。
>       2、而另一些 DISPATCH() 结尾的作用和 continue 类似, 会跳转到 for loop 顶端, 重新检测 gil_drop_request, 必要时释放 gil
>

- **python32 之前的线程切换：**
>       tick 是一个计数器, 表示当前线程在释放 gil 之前连续的执行了多少个字节码(实际上有部分执行较快的字节码并不会被计入计数器)
>       因为 tick 并不是以时间为基准计数, 而是以 opcode 个数为基准的计数, 有一些 opcode 代码复杂耗时长, 一些耗时短, 进而导致同样的 100 个 tick, 一些线程的执行时间总是执行的比另一些线程长
>
>       1、如果当前的线程正在执行一个 CPU 密集型的任务, 它会在 tick 计数器到达 100 之后就释放 gil, 给其他线程一个获得 gil 的机会
>       2、如果当前的线程正在执行一个 IO 密集型的任务, 你执行 sleep/recv/send(...etc) 这些会阻塞的系统调用时, 即使 tick 计数器的值还没到 100, gil 也会被主动地释放
>       3、调用 sys.setcheckinterval() 这个函数把 tick 计数器的值从默认的 100 改为其他的值
>

- **python32 之后的线程切换：**
>       优化：
>           1、如果当前只有一个线程, 那么这个线程会永远执行下去, 无需检查并释放 gil
>           2、如果当前有不止一个线程, 当前等待 gil 的线程在超过一定时间的等待后, 会把全局变量 gil_drop_request 的值设置为 1, 之后继续等待相同的时间, 这时拥有 gil 的线程看到了 gil_drop_request 变为 1,
>               就会主动释放 gil 并通过 condition variable 通知到在等待中的线程, 第一个被唤醒的等待中的线程会抢到 gil 并执行相应的任务
>               sys.getswitchinterval() 是线程在设置 gil_drop_request 这个变量之前需要等待的时长(单位微秒), 5000 微秒 等价于 0.005 秒
>               注意：
>                   把 gil_drop_request 设置为 1 的线程不一定是抢到 gil 的线程
>           3、如果当前的线程正在等待 gil, 并且在等待的过程中 gil 被释放并且被其他的线程获得了, 那么当前的线程过了等待时间之后, 需要重新等待, 把 gil_drop_request 设置为 1 并再次进入等待的循环
>

- **python初始化：**
>       python 解释器本质上是一个 C 程序, 所有的可执行的 C 程序都有 main 函数的入口, python 解释器也不例外
>       你可以在 cpython/Modules/main.c 找到和 main 函数相关的部分, 通过这部分函数你可以发现, 在执行 main loop 之前, 解释器做了很多相关变量的初始化, 其中就包括创建 _gil_runtime_state 和初始化里面的值
>

- **mutex互斥锁：**
>       mutex 是一把互斥锁, 用来保护 locked, last_holder, switch_number 还有 _gil_runtime_state 中的其他变量
>

- **cond信号：**
>       cond 是一个 condition variable, 和 mutex 结合起来一起使用, 当前线程释放 gil 时用来给其他等待中的线程发送信号
>

- **switch_cond：**
>       switch_cond 是另一个 condition variable, 和 switch_mutex 结合起来可以用来保证释放后重新获得 gil 的线程不是同一个前面释放 gil 的线程, 避免 gil 换手但是线程未切换浪费 cpu 时间
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
>
>
>
>
>
>
>
>
