## linux - 线上debug
- **概述：**
>       很多程序长期在线上系统跑着，可能跑着跑着就coredump了，而这种bug比较难复现
>       比较常用的方法：
>           1、线上生成coredump文件
>               这个方法在开发环境比较合适，在线上环境就要小心了，原因是coredump文件很大，一两G都有可能，如果程序出现重复或者多次coredump那用不了多长时间硬盘就满了，硬盘满了之后一些重要的日志（比如nginx的访问日志）就无法写入了，所以这种方法在硬盘够大或者只是偶尔出现coredump的情况下比较合适
>           2、screen+gdb
>               首先ssh连接服务器，其次screen打开一个shell，然后gdb attach到指定进程，最后就是等待coredump的出现了。也不是死等，就是每半天或者过一段时间来看看有没有产生coredump就行。
>           3、内核日志+反汇编
>               可以分析dmesg，然后用addr2line或者gdb进行反汇编
>           4、Google breakpad
>               Google breakpad是一个跨平台的崩溃转储和分析框架和工具集合
>           5、处理SIGSEGV信号 （线上重点使用的方法）！！！！！！！
>               重点是想介绍这种方式，而且据了解，很多人也已经采用这种方式
>               原理：
>                   因为coredump主要是由于一些非法操作导致产生SIGSEGV信号而引起的，所以在我们的程序中注册SIGSEGV信号，当进程收到SIGSEGV信号时，
>                       在我们的信号处理函数中调用gdb来attach到自己的进程，然后就可以通过gdb来收集自己想要的信息了。
>                   注册了SIGSEGV信号处理函数之后，在处理函数中是可以启gdb来收集进程死之前的一些关键信息的，因为gdb的-x参数是指定命令脚本，
>                       所以就可以根据自己的需要来修改命令脚本就行了
>               例如：
>                  //组合gdb命令参数，gdb.cmd文件是gdb的命令脚本，gdb的输出重定向到gdb_debug.log日志文件中
>                  snprintf(gdb_cmd, sizeof(gdb_cmd)-1, "gdb -q -p %d -x ./gdb.cmd >gdb_debug.log 2>&1", getpid());
>                  system(gdb_cmd);
>
>
>       查询线上进程的内存分布：
>           1、使用pmap
>               pmap -d 29482
>           2、使用smaps查看
>               /proc/$PID/smaps 文件中查看进程的内存分布
>               smaps文件中，每一条记录表示进程虚拟内存空间中一块连续的区域。其中第一行从左到右依次表示地址范围、权限标识、映射文件偏移、设备号、inode、文件路径
>           3、使用maps查看
>               /proc/29482/maps
>               maps 文件可以查看某个进程的代码段、栈区、堆区、动态库、内核区对应的虚拟地址
>           4、使用status
>               /proc/24475/status
>               关于进程的内存相关的统计
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
>       https://blog.csdn.net/wangzuxi/article/details/44766221  Linux线上系统程序debug思路及方法
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
