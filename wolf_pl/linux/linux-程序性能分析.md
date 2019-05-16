## Linux- 程序性能分析
- **概述：**
>       对应用程序的性能分析：
>           1、systemstap
>           2、perf
>           3、gprof
>           4、火焰图
>
>
>
>
>

- **统计程序耗时：**
>       当需要对应用程序进行系能分析时，通常可以使用perf或者火焰图。但是这些工具通常只能定性问题，发现那些函数占用cpu较多，需要优化。
>           但是给不出定量的数据，比如这个函数的耗时情况，它耗时1ms还是5ms
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
>       https://openresty.org/posts/dynamic-tracing/    动态追踪技术漫谈
>       https://lrita.github.io/2017/09/16/get-function-elapse/     统计函数执行耗时
>
>       BCC：
>       https://github.com/iovisor/bcc      Tools for BPF-based Linux IO analysis, networking, monitoring, and more
>
>       gprof：
>       https://blog.csdn.net/baidu_35692628/article/details/76687062   Linux系统-耗时检测-gprof操作入门
>       https://www.ibm.com/developerworks/cn/linux/l-gnuprof.html  使用 GNU profiler 来提高代码运行速度
>       https://blog.csdn.net/21aspnet/article/details/1534306  程序分析工具gprof介绍
>
>       perf资料：
>       https://stackoverrun.com/cn/q/7617704
>       http://linux.51yip.com/search/perf  perf使用教程
>       https://dupengair.github.io/2016/10/12/%E7%B3%BB%E7%BB%9F%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95-%E7%B3%BB%E7%BB%9F%E6%80%A7%E8%83%BD%E5%B7%A5%E5%85%B7%E7%AF%87-perf/     系统性能工具篇(perf)
>       https://www.ibm.com/developerworks/cn/linux/l-cn-perf2/     Perf -- Linux下的系统性能调优工具
>
>       Flame Graph：
>       https://github.com/brendangregg/FlameGraph  Stack trace visualizer
>
>
>
>
>
>
>
