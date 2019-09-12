## linux - 异常分析
- **概述：**
>
>
>
>

- **SIGABRT的可能原因：**
>       第三方库如glic检测到内部错误或者破坏约束条件3种可能：
>           1、double free/free 没有初始化的地址或者错误的地址
>           2、堆越界
>           3、assert
>

- **信号：**
>       程序不可捕获、阻塞或忽略的信号有：SIGKILL,SIGSTOP
>       不能恢复至默认动作的信号有：SIGILL,SIGTRAP
>       默认会导致进程流产的信号有：SIGABRT,SIGBUS,SIGFPE,SIGILL,SIGIOT,SIGQUIT,SIGSEGV,SIGTRAP,SIGXCPU,SIGXFSZ
>       默认会导致进程退出的信号有：SIGALRM,SIGHUP,SIGINT,SIGKILL,SIGPIPE,SIGPOLL,SIGPROF,SIGSYS,SIGTERM,SIGUSR1,SIGUSR2,SIGVTALRM
>       默认会导致进程停止的信号有：SIGSTOP,SIGTSTP,SIGTTIN,SIGTTOU
>       默认进程忽略的信号有：SIGCHLD,SIGPWR,SIGURG,SIGWINCH
>

- **编译程序库更新导致程序运行时异常：**
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
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/hokyhu/archive/2012/09/14/2685437.html   深入分析glibc内存释放时的死锁bug
>           https://zhuanlan.zhihu.com/p/62863972   一次malloc分配内存失败导致deadlock分析
>           https://cloud.tencent.com/developer/article/1182935     __lll_mutex_lock_wait的错误原因
>           https://blog.csdn.net/rikeyone/article/details/89226508     Linux SIGABRT和abort()函数
>           https://www.itranslater.com/qa/details/2105686903008789504  c ++ - 如何在程序崩溃时自动生成堆栈跟踪
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
