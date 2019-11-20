## 深入理解计算机系统 - 优化程序性能 - 磁盘io性能
- **概述**
>
>
>
>

- **定位io问题：**
>       当有io性能问题时，可以先通过top简单查看是否有io问题，如果发现有io问题，然后 dstat 具体查看到底是read还是write的io问题。
>       dstat 1 10  #每隔一秒输出10组数据
>
>

- **定位磁盘读写进程：**
>       使用top命令查看处于不可中断状态（D）的进程PID
>       pidstat定位进程的磁盘io情况：
>           使用pidstat命令，加上-d参数，可以看到i/o使用情况（如 pidstat -d -p <pid> 1 3）,发现处于不可中断状态的进程都没有进行磁盘读写
>           -d 展示 I/O 统计数据，-p 指定进程号，间隔 1 秒输出 3 组数据
>           如：pidstat -d -p 4344 1 3
>
>
>       pidstat命令查看所有进程的i/o情况：
>           查看所有进程的i/o情况（pidstat -d 1 20），可以定位到进行磁盘读写的进程
>           间隔 1 秒输出多组数据 (这里是 20 组)
>           如：pidstat -d 1 20
>
>       strace查看进程的系统调用 strace -p <pid>：
>           strace -p 6082
>           strace: attach: ptrace(PTRACE_SEIZE, 6082): Operation not permitted
>           出现上述问题，有两种情况：
>               1、没有权限
>               2、进程状态不正常了，进程已经挂了
>
>       以上工具不能定位到问题，可以使用基于事件记录的动态追踪工具perf：
>           见<<深入理解计算机系统-优化程序性能-上下文切换>>中
>
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/luoahong/p/10811704.html     Linux性能优化实战学习笔记：第八讲
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
