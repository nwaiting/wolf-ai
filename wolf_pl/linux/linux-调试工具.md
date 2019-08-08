## linux - 调试工具
- **概述：**
>       linux下常用的五大调试工具和技术：
>           printf打印
>           查询(/proc，/sys等)
>           跟踪（strace/ltrace）
>           valgrind（memwatch）
>           GDB
>           SystemTap
>           perf
>

- **printf：**
>       打印信息
>
>

- **查询(/proc,/sys等)**
>       /proc是一个伪文件系统
>       收集的运行的每一个进程的细节信息
>       /proc/cmdline   内核命令行
>       /proc/filesystems   文件系统的内核支持的信息
>       /proc/<pid>/cmdline 命令行参数传递到当前进程
>       /proc/<pid>/mem 当前进程持有的内存
>       /proc/<pid>/status  当前进程的状态
>
>

- **跟踪（strace/ltrace）：**
>       strace和ltrace用于拦截和记录系统调用及其接收的信号。
>
>

- **Valgrind：**
>       是一套调试和分析工具
>       Valgrind检测作用：
>           内存泄漏
>           重释放
>           访问越界
>           使用未初始化的内存
>           使用已经被释放的内存
>       Valgrind有一些缺点：
>           增加了内存的占用，减慢程序的运行，有时会误报或漏报
>           不能检测出静态分配的数组的访问越界问题
>

- **GDB**
>       调试程序
>
>
>

- **SystemTap**
>       1、Linux systemtap定位系统IO资源使用情况（ok）
>       2、SystemTap是一个强大的调试工具，是监控和跟踪运行中的Linux 内核的操作的动态方法，确切的说应该是一门调试语言，
>           因为它有自己的语法，也有解析、编译、运行等过程（准确的说有五个阶段）。
>       3、但它主要解决的问题是收集Linux内核或者用户进程的信息，主要目的是调试
>       4、gdb、kgdb同是linux最强大的调试器，gdb和SystemTap不是竞争关系，而是互补关系，gdb能做的事情SystemTap做不到，比如断点/watch变量等等这些SystemTap都做不到
>           而SystemTap能做的事情gdb做不到或者非常麻烦才做到，比如很方便查看内核调试栈/嵌入C语言等等gdb就很难
>       5、systemtap 是利用Kprobe 提供的API来实现动态地监控和跟踪运行中的Linux内核的工具，相比Kprobe，systemtap更加简单，
>           提供给用户简单的命令行接口，以及编写内核指令的脚本语言。对于开发人员，systemtap是一款难得的工具
>
>
>
>
>
>
>
>

- **总结：**
>       查询进程的系统信息，使用/proc
>       查询进程的调用库相关的，了解程序流程，使用strace
>       分析程序崩溃，使用GDB
>
>
>
>
>

- **待续：**
>       参考：https://linux.cn/article-5047-1.html
>       https://www.ibm.com/developerworks/cn/linux/sdk/l-debug/index.html
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
