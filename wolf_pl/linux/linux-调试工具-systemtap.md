## linux - systemtap
- **概述：**
>       对管理员，SystemTap可用于监控系统性能，找出系统瓶颈，而对于开发者，可以查看他们的程序运行时在linux系统内核内部的运行情况。
>           主要用于查看内核空间事件信息，对用户空间事件的探测，目前正加紧改进
>
>
>

- **命令行参数：**
>       SystemTap使用$或@传递命令行参数：$传递整数参数，@传递字符串参数
>       stap命令从文件或标准输入中读取SystemTap脚本
>           stap file_name
>       stap命令行选项：
>           -v 让SystemTap会话输出更加详细的信息。你可以重复该选项多次来提高执行信息的详尽程度
>               stap -vvv script.stp
>           -o file_name
>               将标准输出重定向到file_name
>           -S size[,count]
>               将输出文件的最大大小限制成sizeMB，存储文件的最大数目为count。这个命令实现了logrotate的功能，每个输出文件会以序列号作为后缀。
>           -x process_id
>               设置SystemTap处理函数target()为指定PID
>           -c 'command'
>               运行command，并在command结束时退出。该选项同时会把target()设置成command运行时的PID
>           -e 'code'
>               直接执行给定的code。（译注：如stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'）
>           -F
>               进入SystemTap的飞行记录仪模式（flight recorder mode），并在后台运行该脚本
>           -L
>               -L选项来列出特定探测点下可用的目标变量
>               -l（或-L）选项可以列出指定的某个probe描述中所有符合的probe点的列表
>           -d
>               -d选项负责加载模块/可执行程序的符号表信息，而-ldd则加载-d module中module或是probe需要的共享库符号表信息
>

- **输出变量：**
>       $$vars：类似sprintf("parm1=%x ... parmN=%x var1=%x ... varN=%x", parm1, ..., parmN, var1, ..., varN)，目的是打印probe点处的每个变量；
>       $$locals：$$vars子集，仅打印local变量；
>       $$parms：$$vars子集，仅包含函数参数；
>       $$return：仅在return probes存在，类似sprintf("return=%x", $return)，如果没有返回值，则是空串
>
>

- **不绑定到内核的特定指令或位置处：**
>       不绑定到内核的特定指令或位置处。包括：
>           1、begin：SystemTap session开始时触发，当SystemTap脚本开始运行时触发；
>           2、end ：SystemTap session终止时触发；
>           3、timer事件：
>                probe timer.s(4){
>	                      printf("hello world/n")
>                       }
>               • timer.ms(milliseconds)
>               • timer.us(microseconds)
>               • timer.ns(nanoseconds)
>               • timer.hz(hertz)
>               • timer.jiffies(jiffies)
>
>
>

- **events：**
>       探测点指定了在内核的什么位置进行探测，探测点还可以定义在与目标程序上某个点没有联系的抽象事件上，但这时转换器就不能获得太多关于探测点的符号信息
>           begin
>           end
>           kernel.function("sys_sync")
>           kernel.function("sys_sync").call
>           kernel.function("sys_sync").return
>           kernel.syscall.*
>           kernel.function(“*@kernel/fork.c:934”)
>           kernel.trace("tracepoint")
>           module(“ext3”).function(“ext3_file_write”)
>           timer.jiffies(1000)
>           timer.ms(200).randomize(50)
>           process.(“PATH”).syscall
>           process.(PID).function.return
>
>

- **Handlers：**
>       探测点名称后紧跟的一组大括号内定义了每次内核运行到该探测点时需要进行的操作，比如可以指定输出数据过滤的条件，或者更为复杂的控制逻辑。
>           这些操作完成后再返回探测点，继续下面的指令。
>
>

- **Helper functions：**
>       Helper functions
>           tid() The id of the current thread.
>           pid() The process (task group) id of the current thread.
>           uid() The id of the current user.
>           execname() The name of the current process.
>           cpu() The current cpu number.
>           gettimeofday_s() Number of seconds since epoch.
>           get_cycles() Snapshot of hardware cycle counter.
>           pp() A string describing the probe point being currently handled.（pp()：描述当前被处理的探针点的字符串；）
>           probefunc() If known, the name of the function in which this probe was placed.
>           $$vars If available, a pretty-printed listing of all local variables in scope.
>           print_backtrace() If possible, print a kernel backtrace.
>           print_ubacktrace() If possible, print a user-space backtrace.
>
>

- **安装Systemtap**
>       Systemtap*
>       Kernel-debug-info
>       Kernel-source or kernel development environment (/usr/src/linux).
>       Elfutils
>
>
>

- **运行原理：**
>       How is SystemTap working？
>       1、语法分析阶段（parse）
>           主要是检查输入脚本是否存在语法错误，例如大括号是否匹配、变量定义是否规范等
>       2、细化（Elaborate）
>           细化是分析输入脚本并解析对内核的引用或用户符号与 tapsets 的处理阶段。Tapsets 是用来扩展脚本能力的脚本或 C 代码库。细化将脚本中的外部引用解析为符号信息并导入脚本子程序，为下一步转换为 C 程序做准备，这个过程就类似于将库文件链接到目标文件。对内核数据如函数参数、局部和全局变量、函数以及源地址都需要被解析为运行时实际的地址，这是通过对构建内核时编译器产生的 DWARF 调试信息进行处理来实现的。所有的调试数据都会在内核模块运行之前被处理。调试数据包含足够的信息来定位内联函数、局部变量、类型以及一些通常不被导出到内核模块的声明。
>        下面总结一下细化阶段所做的主要工作：
>                获取用户的探测脚本
>                预处理宏
>                包含所需要的脚本库
>                解析代码中对符号的引用
>                查找函数入口地址
>                查找行号信息
>                查找全局和局部变量的类型及地址
>       3、转换（Translate）
>           脚本被细化后它将会被转换为 C 语言代码，每个脚本子程序都被扩展成C语言代码块并进行安全检查，例如对循环结构进行递增检查了防止无限循环。由多个探测点共享的变量会被映射成适当的静态声明，并以块为单位进行访问保护。在内核中使用kprobes中的注册APIs对探测点处理器（probe handlers）进行注册。对于在内核中的探测点，会被插入到内核的内存空间中；对于用户级别探测点，它将被插入到可执行代码中，当处理器在内核中运行时将其载入到用户的内存空间。
>       4、构造（Build）
>           转换完成后，产生的 C 语言代码会被编译并与运行时进行链接成一个stand-alone 内核模块。该模块可被加密标记以用于安全归档或远程使用。
>       5、运行（Execution）
>           生成模块后 SystemTap 驱动程序会使用 insmod 将内核模块载入。该模块会进行初始化、插入探测点，然后等待探测点被触发。探测点被触发后会调用相关联的处理器程序并挂起执行线程，当该探测点所有的处理器都运行后，线程重新运行。当用户发送中断或脚本调用 exit 时，SystemTap 脚本将中止运行。然后卸载模块并移除探测点。
>       6、数据采集
>           SystemTap 需要将从内核中获取的数据传输到用户空间，并且需要很高的吞吐量、低延迟以及最小化对被监测系统性能的影响。缺省情况下，SystemTap 的输出会在脚本出口以批处理的方式写入 stdout，同时该输出会被自动保存到文件中。在用户空间，SystemTap 可以以简单的文本方式显示数据，或使用图形类的应用程序生成计算机可读的表格数据等。
>
>
>       可见Systemtap使用的较为成熟的已有技术：
>           1、Kprobes/Uprobes
>           2、Relayfs
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
>       http://abcdxyzk.github.io/blog/2015/06/01/debug-systemtap-beginner/     SystemTap Beginner
>       https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/stap-intro?lang=en    Systemtap introduction
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
