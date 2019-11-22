## 深入理解计算机系统 - IO性能 - IO原理
- **概述**
>       常用命令：
>       slabtop：找到内存占用最多的缓存类型
>       iostat：每块磁盘的使用率（指标实际上来自/proc/diskstats）
>       pidstat： 查看进程I/O情况
>       iotop：  按照io大小对进程排序，然后找到I/o较大的那些进程
>
>       io性能分析步骤：
>           1、先用iostat -x -d 1 查看系统的io情况
>               可以查看到写请求的响应时间多少秒、每秒写入数据多少
>           2、然后使用pidstat分析进程的io情况，
>           3、strace分析python进程调用
>           4、lsof查看python进程打开了那些文件
>
>
>

- **索引节点、目录项及其关系：**
>       索引节点：
>           索引节点记录文件的元数据（inode索引、文件大小、访问权限、修改日期、数据的位置）
>           索引节点和文件一一对应，和文件内容一样，都会被持久化存储到磁盘，所以索引节点同样占用磁盘
>
>       目录项：
>           记录文件的名字、索引节点指针以及与其目录项的关联关系
>           多个关联的项目，就构成了文件系统目录结构
>           目录项是由内核维护的一个内存数据结构，也叫目录项缓存
>
>       关系：
>           目录项维护的是文件系统的树状结构
>
>       相互关系见下图：
>![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/linux_pic/linux_io_file_system_inode.png)
>
>


- **linux文件系统架构：**
>       系统调用、VFS、缓存、文件系统以及存储之间的关系图，如下：
>![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/linux_pic/linux_io_file_system_framework.png)
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
