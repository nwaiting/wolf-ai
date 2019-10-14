## linux - 内存分配
- **概述：**
>       内存的延迟分配，系统开始只为进程分配一块虚拟内存，当使用这块内存时，内核才会分配具体的物理内存页面给用户。
>       glibc对于heap内存申请大于128K的空间，glibc采用mmap的方式向内存申请内存。小于128K的采用brk，128K是阈值。
>       大块内存申请：
>           glibc直接使用mmap系统调用申请一块虚拟地址，供进程单独使用，使用unmmap系统调用进行释放，过程中不会产生内存碎片。
>       内核内存释放：
>           当glibc发现堆顶有连续的128K空间是空闲的时候，通过brk或sbrk系统调用，来调整heap顶的位置，将占用的内存返回给系统。
>           内存会通过删除相应的线性区，释放占用的物理内存
>           只要堆顶的部分申请内存还在占用，在下面释放的内存再多，都不会被返回到系统中，仍然占用着物理内存，为什么这样设计？
>           因为：
>               内核处理堆的时候，过于简单，只能通过调整堆顶指针的方式来调整程序占用的线性区（虚拟内存）
>               而又只能通过调整线性区的方式，来释放内存。
>           所以只要堆顶不减小，占用的内存就不会释放。
>
>       glibc申请内存：
>           glibc为每一块内存维护了一个chunk结构，内存申请时，最少分配16个字节，以便能够维护chunk结构
>
>       查看机器可用内存：
>           linux系统中，会尽可能的cache和buffer一些数据，方便下次使用，所以一般free很小
>           可用内存 = free + buffers + cached = total - used
>

- **内存释放：**
>       C++中delete释放内存时效性问题：
>           1、内存被释放后 表示这块儿内存可以被操作系统重新分配
>           2、delete之后只是程序告诉操作系统这一块内存不需要了，操作系统可以随时回收。至于什么时候回收这一块内存，就是和操作系统有关了
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

- **常用的linux内存统计分析：**
>       常用的linux内存统计工具：
>           1、/proc/meminfo
>               这个动态更新的虚拟文件实际上是许多其他内存相关工具(如：free / ps / top)等的组合显示
>              /proc/1/statm
>              /proc/[pid]/status
>           2、free
>               free命令是一个快速查看内存使用情况的方法，它是对 /proc/meminfo 收集到的信息的一个概述
>           3、htop
>               htop命令显示了每个进程的内存实时使用率。它提供了所有进程的常驻内存大小、程序总内存大小、共享库大小等的报告
>           4、memstat
>               memstat是一个有效识别executable(s), process(es) and shared libraries使用虚拟内存情况的命令。给定一个进程ID，memstat可以列出这个进程相关的可执行文件、数据和共享库
>           5、nmon
>               nmon是一个基于ncurses的系统基准测试工具，它可以监控CPU、内存、I/O、文件系统及网络资源等的互动模式。对于内存的使用，它可以实时的显示 总/剩余内存、交换空间等信息
>               /nmon/nmon_x86_rhel6 -f -N -m /nmon -s 60 -c 1440 -y
>
>
>
>

- **待续：**
>       https://blog.csdn.net/fivedoumi/article/details/7057253     内存分配——深入浅出
>       https://www.cnblogs.com/zhuiluoyu/p/6154898.html    Linux下查看内存使用情况方法总结
>       http://www.wowotech.net/memory_management/meminfo_1.html    /proc/meminfo分析（一）
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
