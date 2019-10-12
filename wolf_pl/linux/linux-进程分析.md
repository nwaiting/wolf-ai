## linux - 进程分析
- **概述：**
>       1、ldd /path/to/program
>           查看可执行程序的共享库依赖关系
>           注意：
>               并不推荐为任何不可信的第三方可执行程序运行ldd，因为某些版本的ldd可能会直接调用可执行程序来明确其库文件依赖关系，这样可能不安全
>               取而代之的是用一个更安全的方式来显示一个未知应用程序二进制文件的库文件依赖，比如objdump
>       2、objdump -p /path/to/program | grep NEEDED
>           显示一个未知应用程序二进制文件的库文件依赖
>       3、sudo pldd <PID>
>           查看运行进程的共享库依赖关系，需要root权限去执行pldd命令
>           想要找出被一个运行中的进程载入的共享库，你可以使用pldd命令，它会显示出在运行时被载入一个进程里的所有共享对象
>       4、sudo pmap <PID>
>           报告一个进程的内存映射，也能显示出运行进程的库文件依赖
>

- **进程内存工具区别：**
>       (以下仅供参考)
>       Valgrind：
>           适合解决非法读写，无主内存泄露等问题定位
>       gperftools：
>           长期运行进程内存使用量应该是稳定的，gperftools适合发现运行过程中内存差异，提供泄露的函数范围。
>           而且对影响影响小，适合高压力快速复现。
>       getrusage：
>           虽然对于定位问题帮助不大，但是可以用以守护进程监控管理业务进程的内存使用情况。
>

- **gperftools内存泄漏分析：**
>       # 用动态载入tcmalloc的方式执行你自己的可执行程序(加-g编译选项)。
>       # 下面三个参数的意思是检查堆内存，每当累计分配内存(无论是否释放)达到100MB时，将当前堆内存快照输出到memtm.xxxx.heap的文件中
>       LD_PRELOAD=libtcmalloc.so HEAPCHECK=strict HEAPPROFILE=memtm HEAP_PROFILE_ALLOCATION_INTERVAL=100000000 ./exefile
>       # 之后持续运行一段时间，如果是服务进程，需要压测一段时间，假设压测到稳定阶段的内存快照文件是memtm.0005.heap
>       # 继续压测一段时间，直到确认内存已经开始非正常增加，停止，假设最后的内存快照文件是memtm.0010.heap.
>       # 然后利用gperftools通过对比这两个快照文件，分析diff部分是否有内存增长，增长主要来自于哪些函数调用
>       # (分析结果中有每个函数对应分配的增长内存总量和占比，顺藤摸瓜可以基本定位是哪部分内存分配后未及时释放)。
>       # 之所以不使用memtm.0001.heap作为对比base，是因为对于一些程序，初期会显示或者隐式的使用一些缓存，这部分也会导致一定的内存增长。
>       # 等到进入稳定阶段后，这些缓存基本达到稳定状态，不再增长了。这时再对比可以去掉正常缓存的干扰。
>       pprof --pdf --base=memtm.0005.heap ./exefile memtm.0010.heap > diff.pdf
>
>       比较两个内存镜像增长的内存来自哪里：
>       ./pprof --pdf --base=/tmp/mem_tcmalloc_nginx.0016.heap /root/download/usr/local/nginx/nginx /tmp/mem_tcmalloc_nginx.0017.heap > mem_tcmalloc_nginx.0017.diff.0016.heap.pdf
>
>
>
>
>
>

- **待续：**
>       参考：https://www.jianshu.com/p/6854085d54cd   利用Valgrind和gperftools解决内存问题
>           https://www.jianshu.com/p/3104a74c4389  C++内存泄漏检查
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
