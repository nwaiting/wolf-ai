## 深入理解计算机系统 - IO性能 - IO性能分析
- **概述**
>
>       常用命令：
>           1、iostat
>               磁盘的IO使用率、吞吐量、响应时间、IOPS
>           2、pidstat
>               进程的IO吞吐量、IO的延迟等
>           3、strace lsof
>               找到对应进程的读写文件
>
>       常用命令如下：
>![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/linux_pic/linux_io_file_system_commands.png)
>
>
>

- **IO性能分析步骤：**
>       1、通过top查看系统整体的负载情况，可以查看到iowait的负载
>       2、通过iostat查看具体系统的IO负载情况
>       3、通过pidstat查看进程的IO负载情况
>       4、查询到对应的进程后，则可使用strace、lsof、pstree查询到进程具体的读写文件情况
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
>
>
>
>
>
>
>
>
