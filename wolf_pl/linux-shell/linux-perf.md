## linux-shell - perf
- **概述：**
>
>       线上环境问题定位追踪：
>       1、GDB 所基于的 ptrace 这种很古老的系统调用，其中的坑和问题也非常多
>       2、动态追踪的工具很多，systemtap，perf，ftrace，sysdig，dtrace，eBPF等
>

- **perf stat：**
>       perf stat可以对程序运行过程中的性能计数器(包括Hardware，software counters)进行统计，分析程序的整体消耗情况
>
>
>

- **perf Top：**
>       实时显示当前系统的性能统计信息或者某个进程的统计信息
>       1、Perf top 用于实时显示当前系统的性能统计信息
>           该命令主要用来观察整个系统当前的状态，看当前系统最耗时的内核函数
>       2、比如可以通过查看该命令的输出来查看某个用户进程。
>           perf top -p 16279
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
>       参考：http://walkerdu.com/2018/09/13/perf-event/#5-2-_perf_stat    性能分析利器之perf浅析
>           http://github.tiankonguse.com/blog/2016/03/29/perf-record.html      perf 性能分析
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
