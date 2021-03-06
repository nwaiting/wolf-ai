## linux - 线程实现机制
- **概述：**
>       只要是共享的资源，那么它就可以看作临界资源，而临界资源的访问需要同步。
>
>       内核调度的对象是线程，而不是进程。！！！！
>
>       现代操作系统中，系统提供两种虚拟机制：
>           1、虚拟处理器
>           2、虚拟内存
>           注意：线程之间可以共享虚拟内存，但每个都拥有各自的虚拟处理器。！！！
>
>       多进程：
>           1、fork系统调用从内核返回两次：一次回到父进程，一次回到新产生的进程
>               调用结束时，父进程恢复执行，子进程开始执行
>           Unix创建进程分为两步：
>               1、fork
>                   拷贝当前进程创建一个子进程。linux的fork使用写时拷贝页实现。进程创建后会马上运行一个可执行文件。
>                   内核有意选择子进程先运行，因为一般子进程都会马上调用exec函数，这样可以避免写时拷贝的额外开销，如果父进程先执行的话，有可能会开始向地址空间写入。
>                   fork实际开销：
>                       复制父进程的页表以及给子进程创建唯一的进程描述符
>                   子进程与父进程的区别：pid、ppid和某些资源和统计量（如挂起的信号）
>               2、exec
>                   负责读取可执行文件载入地址空间开始运行
>
>

- **线程共享和独享资源：**
>       共享：
>           地址空间
>           全局变量
>           打开的文件
>           子进程
>           闹钟
>           信号及信号服务程序
>           记账信息
>       独占资源：
>           程序计数器
>           寄存器
>           栈
>           状态字
>
>

- **线程模型：**
>       内核态线程数量极少，用户态线程数量较多。
>       每个内核态线程可以服务一个或多个用户态线程，用户态线程会被多路复用到内核态线程上。
>

- **变量：**
>       寄存器就是CPU的小内存，特点是容量小，速度快。
>       变量一般情况下都存在内存中，如果程序需要使用某个变量，CPU的控制器将从内存中取得变量值后会将其存在寄存器中。
>
>       volatile 变量表示：
>           表示内存中的值可能发生变化，获取变量的值是从内存中获取而不是从寄存器中获取内存的备份。
>
>

- **参考：**
>       https://www.ibm.com/developerworks/cn/linux/kernel/l-thread/index.html  Linux 线程实现机制分析
>       https://cn.aliyun.com/jiaocheng/128492.html
>       https://pan.baidu.com/s/1PvEZ78DjITVnWmCF2NRqxw 提取码: fqks   linux内核设计与实现
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
