## 深入理解计算机系统 - CPU性能 - 进程的定位
- **概述**
>       当一个进程不知道在什么位置被调用的时候，可以使用pstree命令查看：
>           pstree | grep [xx]  xx表示进程名
>           如：pstree | grep stress
>
>       pidstat 可以查看进程的负载情况
>           如：pidstat -p 44361
>               pidstat 查看进程负载
>

- **进程组：**
>       进程组表示一组相互关联的进程，比如每个子进程都是父进程所在组的成员，而会话是指共享同一个控制终端的一个或多个进程组
>

- **会话：**
>       比如使用ssh登录到服务器，这个控制终端就对应一个会话，在终端运行的命令以及他们的子进程就构成了一个个的进程组。
>           其中，在后台运行的命令，构成后台进程组，在前台运行的命令，构成前台进程组
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
>
>
