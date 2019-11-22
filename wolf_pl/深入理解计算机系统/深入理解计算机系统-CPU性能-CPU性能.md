## 深入理解计算机系统 - CPU性能 - CPU性能
- **概述**
>
>
>

- **CPU性能指标：**
>       常见的CPU性能指标：
>           1、CPU使用率
>               用户CPU（说明应用程序繁忙）
>               系统CPU（说明内核比较忙）
>               iowait（说明系统与硬件设备的io交互时间比较长）
>               软中断（内核调用软中断）
>               硬中断（硬中断处理时间长，说明系统发生了大量的中断）
>               窃取CPU
>               客户CPU
>           2、上下文切换
>               自愿上下文切换
>               非自愿上下文切换
>               过多上下文切换
>           3、平均负载
>           4、CPU缓存命中率
>
>

- **常用的性能查看工具：**
>       1、系统CPU使用率
>           vmstat      #系统整体的CPU使用率、上下文切换、中断次数
>           mpstat      #每个CPU的软中断次数
>           sar
>           /proc/stat
>           top
>       2、进程CPU使用率
>           pidstat     #进程和线程CPU使用率、中断上下文切换次数
>       3、系统上下文切换
>           vmstat
>       4、进程上下文切换
>           pidstat
>           pstree      #进程的父子关系
>       5、软中断
>           /proc/softirqs  #软中断类型和每个CPU上的累积中断次数
>           mpstat
>       6、硬中断
>           vmstat
>           /proc/interrupts    #硬中断类型和每个CPU上的累积中断次数
>       7、网络
>           dstat
>           sar
>           tcpdump
>       8、I/O
>           dstat
>           sar
>       9、CPU硬件情况
>           lscpu
>       10、时间剖析
>           perf
>           strace      #追踪进程的堆栈
>               比如：strace -p $(pgrep app)
>
>       注：
>           1、pidstat 中的 %wait 跟 top 中的 iowait% 有什么不同？
>               pidstat 中， %wait 表示进程等待 CPU的时间百分比
>               top 中 ，iowait% 则表示等待 I/O 的 CPU的时间百分比

- **系统优化：**
>       1、CPU绑定
>           把进程绑定到一个或多个CPU上，可以提高CPU缓存的命中率
>

- **应用程序优化：**
>       1、编译器优化
>           gcc -O2等优化选项
>       2、算法优化
>           降低复杂度
>       3、异步处理
>       4、多线程代替多进程
>       5、善用缓存
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/luoahong/p/10592001.html     CPU性能分析
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
