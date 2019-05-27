## linux - systemtap
- **概述：**
>       对管理员，SystemTap可用于监控系统性能，找出系统瓶颈，而对于开发者，可以查看他们的程序运行时在linux系统内核内部的运行情况。
>           主要用于查看内核空间事件信息，对用户空间事件的探测，目前正加紧改进
>
>       由于systemtap运行需要内核的调试信息支撑，默认发行版的内核在配置时这些调试开关没有打开，所以安装完systemtap也是无法去探测内核信息的，
>           由于发行版的内核默认无内核调试信息，所以我们还需要一个调试内核镜像，在http://ddebs.ubuntu.com/pool/main/l/linux/ 找到你的内核版本相对应的内核调试镜像（版本号包括后面的发布次数、硬件体系等都必须一致）
>           如：wget http://ddebs.ubuntu.com/pool/main/l/linux/linux-image-debug-3.8.0-30-generic_dbgsym_3.8.0-30.43_i386.ddeb
>               dpkg -i linux-image-debug-3.8.0-30-generic_dbgsym_3.8.0-30.43_i386.ddeb
>               注：方法仅限于Ubuntu发行版，至于其他的发行版并不能照搬
>
>
>       开源工具：
>           https://github.com/nwaiting/stapxx
>           https://github.com/openresty/openresty-systemtap-toolkit
>           https://github.com/brendangregg/FlameGraph
>
>

- **原理：**
>       解析stap文件，生成对应的c代码，然后将其编译为一个内核模块，并加载到内核中，模块加载之后，将所有探测的事件以钩子的方式挂到内核上，当任何处理器上的某个事件发生时，相应钩子上句柄就会被执行。最后，当systemtap会话结束之后，钩子从内核上取下，移除模块。整个过程用一个命令 stap 就可以完成
>
>
>

- **安装Systemtap**
>       Systemtap*
>       Kernel-debug-info
>       Kernel-source or kernel development environment (/usr/src/linux).
>       Elfutils
>
>       开发调试时需要安装的包：
>       nss-softokn-debuginfo-3.15.4-2.el7.x86_64
>       kernel-debuginfo-3.10.0-123.el7.x86_64
>       glibc-debuginfo-common-2.17-55.el7.x86_64
>       glibc-debuginfo-2.17-55.el7.x86_64
>       kernel-debuginfo-common-x86_64-3.10.0-123.el7.x86_64
>       systemtap-devel-3.3-3.el7.x86_64
>       systemtap-runtime-3.3-3.el7.x86_64
>       systemtap-sdt-devel-2.4-14.el7.x86_64
>       systemtap-3.3-3.el7.x86_64
>       systemtap-client-3.3-3.el7.x86_64
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
>       $$vars：作用域内所有变量的 $$vars
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

- **常用参数**
>       -e SCRIPT               Run given script.
>       -l PROBE                List matching probes.
>       -L PROBE                List matching probes and local variables.
>       -g                      guru mode
>       -D NM=VAL               emit macro definition into generated C code
>       -o FILE                 send script output to file, instead of stdout.
>       -x PID                  sets target() to PID
>
>
>

- **想要获取参数的问题：**
>       首先可通过stap -L 查看函数中的哪些变量可以被看到,后面写脚本时可以直接引用这些变量
>           如：stap -L 'process("/lib64/libc.so.6").function("malloc")'
>
>
>       stap -l 可以查看某个函数在哪个文件的哪一行定义的，可以是内核代码也可以是用户态代码
>           如：stap -l 'process("/lib64/libc.so.6").function("malloc")'
>

- **使用宏功能：**
>       @define part1 %(  "/path/part/1" %)
>       @define part2 %(  "/part/2" %)
>       probe process(@part1 @part2).function("...") { ... }
>
>
>
>
>

- **不打印调试信息问题：**
>       参考：http://blog.yufeng.info/archives/1229
>       使用SystemTap打印user-space程序的调用栈信息时，需要产生足够的调试信息。这时需要-d和--ldd两个选项
>           有时候我们并没能得到全部的符号信息， 比如# 0xffffffff8803826a 这行是谁没打印出来吧。 原因是我们的模块可能被未知的模块所调用，这些模块的符号信息没有自动加载，所以systemtap当然就不知道谁是谁了
>           -d选项负责加载模块/可执行程序的符号表信息
>           --ldd则加载-d module中module或是probe需要的共享库符号表信息
>           --all-modules 加载所有模块
>
>       如：stap func_call.stp -d /opt/nginx/sbin/nginx --ldd -x 12345
>          或者  stap func_call.stp -d /opt/nginx/sbin/nginx --all-modules -x 12345
>
>
>           -D MAXMAPENTRIES=20480
>               Maximum number of rows in any single global array, default 2048
>           -D MAXACTION=20000
>               Maximum number of statements to execute during any single probe hit (with interrupts disabled), default 1000
>           -D MAXTRACE=40
>           -D MAXSTRINGLEN=4096
>               Maximum length of strings, default 128
>           -D MAXBACKTRACE=40
>
>           -D 宏作用：
>               看到gcc编译的时候使用了-D "MAXMAPENTRIES=10240" 来替换模块源码里面的macro MAXMAPENTRIES,最大项改成了10240
>
>
>
>
>

- **events：**
>       探测点指定了在内核的什么位置进行探测，探测点还可以定义在与目标程序上某个点没有联系的抽象事件上，但这时转换器就不能获得太多关于探测点的符号信息
>           begin
>           end
>           kernel.function("sys_sync")
>               在函数的入口处放置探测点，可以获取函数参数$PARM
>           kernel.function("sys_sync").call
>               取补集，取不符合条件的函数
>           kernel.function("sys_sync").return
>               在函数的返回处放置探测点，可以获取函数的返回值$return，以及可能被修改的函数参数$PARM
>           kernel.syscall.*
>           kernel.function(“*@kernel/fork.c:934”)
>           kernel.trace("tracepoint")
>           module(“ext3”).function(“ext3_file_write”)
>           timer.jiffies(1000)
>           timer.ms(200).randomize(50)
>           process.(“PATH”).syscall
>           process.(PID).function().return
>

- **设置探测点：**
>       begin The startup of the systemtap session.
>       end The end of the systemtap session.
>       kernel.function("sys_open") The entry to the function named sys_open in the kernel.
>       syscall.close.return The return from the close system call.
>       module("ext3").statement(0xdeadbeef) The addressed instruction in the ext3 filesystem driver.
>       timer.ms(200) A timer that fires every 200 milliseconds.
>       timer.profile A timer that fires periodically on every CPU.
>       perf.hw.cache_misses A particular number of CPU cache misses have occurred.
>       procfs("status").read A process trying to read a synthetic file.
>       process("a.out").statement("*@main.c:200") Line 200 of the a.out program.
>       kernel.function("*@net/socket.c") 表示net文件夹socket.c文件的所有函数
>
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
>           execname() The name of the current process. (gettimeofday_ms,gettimeofday_us)
>           cpu() The current cpu number.
>           gettimeofday_s() Number of seconds since epoch.
>           get_cycles() Snapshot of hardware cycle counter.
>           pp() A string describing the probe point being currently handled.（pp()：描述当前被处理的探针点的字符串；）
>           probefunc() If known, the name of the function in which this probe was placed.(探测器到达的函数名)
>           $$vars If available, a pretty-printed listing of all local variables in scope.
>           $$parms：表示函数参数
>           $$return：表示函数返回值
>           print_backtrace() If possible, print a kernel backtrace.
>           print_ubacktrace() If possible, print a user-space backtrace.
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

- **变量的应用风格：**
>      Refers to all kernel functions with "init" or "exit" in the name
>           kernel.function("init"), kernel.function("exit")
>       Refers to any functions within the "kernel/time.c" file that span line 240
>           kernel.function("*@kernel/time.c:240")
>       Refers to all functions in the ext3 module
>           module("ext3").function("*")
>       Refers to the statement at line 296 within the kernel/time.c file
>           kernel.statement("*@kernel/time.c:296")
>       Refers to the statement at line bio_init+3 within the fs/bio.c file
>           kernel.statement("bio_init@fs/bio.c+3")
>
>       部分在编译单元内可见的源码变量，比如函数参数、局部变量或全局变量，在探测点处理函数中同样是可见的。
>       在脚本中使用$加上变量的名字就可以引用了。
>
>       变量的引用有两种风格：
>           $varname // 引用变量varname
>           $var->field // 引用结构的成员变量
>           $var[N] // 引用数组的元素
>           &$var // 变量的地址
>           @var("varname") // 引用变量varname
>           @var("var@src/file.c") // 引用src/file.c在被编译时的全局变量varname
>           @var("varname@file.c")->field // 引用结构的成员变量
>           @var("var@file.c")[N] // 引用数组的元素
>           &@var("var@file.c") // 变量的地址
>           $var$ // provide a string that includes the values of basic type values
>           $var$$ // provide a string that includes all values of nested data types
>           $$vars // 一个包含所有函数参数、局部变量的字符串
>           $$locals // 一个包含所有局部变量的字符串
>           $$params // 一个包含所有函数参数的字符串
>

- **运算符：**
>       使用@cast()操作符支持类型转换
>       当指针是一个void *类型，或是保存为整数后，可以使用cast运算符指定指针的数据类型：
>       下面的语句将P翻译成一个指向名为type_name的结构体或联合体的指针，并对指针解引用获取其成员的值，可选模块参数告诉翻译器在哪个寻找该类型的信息
>           如：
>               @cast(p,"type_name"[, "module"])->member
>               @cast(pointer, "task_struct","kernel")->parent->tgid
>               @cast(tv,"timeval", "<sys/time.h>")->tv_sec
>

- **常用函数：**
>       @entry(gettimeofday_us())   entry方法将一个表达式放置于函数入口处
>       @defined($flags)    随着代码运行，变量可能失效，因此需要用@defined()来判断该变量是否可用
>           如：write_access = (@defined($flags)? $flags & FAULT_FLAG_WRITE : $write_access)
>       @hist_log(sends) 打印以2为底指数分布的直方图
>           分为两行：value代表原始的值，count代表有多少次
>           例如：sends = [1,2,4,8,12,12,12,16,16,16,16,16,16,16,16,16,16,16,32,32,32,32,64]
>               print(@hist_log(sends))
>               # 2^0到2^9之间，统计个数
>               value |-------------------------------------------------- count
>                   0 |                                                    0
>                   1 |@                                                   1
>                   2 |@                                                   1
>                   4 |@                                                   1
>                   8 |@@@@                                                4
>                  16 |@@@@@@@@@@@                                        11
>                  32 |@@@@                                                4
>                  64 |@                                                   1
>                 128 |                                                    0
>                 256 |                                                    0
>
>       @hist_linear(v, start, stop, interval) # 打印start-stop区间interval间隔的直方图
>           例如：sends = [1,2,4,8,12,12,12,16,16,16,16,16,16,16,16,16,16,16,32,32,32,32,64]
>               print(@hist_linear(sends, 10, 30, 5))
>               # 在10到30间，以5为间隔，统计个数
>           value |-------------------------------------------------- count
>             <10 |@@@@                                                4
>              10 |@@@                                                 3
>              15 |@@@@@@@@@@@                                        11    (表示大于15小于20的个数)
>              20 |                                                    0
>              25 |                                                    0
>              30 |@@@@                                                4
>             >30 |@                                                   1
>
>

- **统计变量：**
>       aggregates 用于读取统计变量（statistics）的一系列统计函数
>           @min 返回statistics中的元素的最小值
>           @max 返回statistics中的元素的最大值
>           @count 返回statistics中的元素的个数
>           @avg 返回statistics中的元素的平均值
>           @sum 返回statistics中的元素的总和
>           @hist_log 用@来图形化打印statistics
>           如：sum_bytes_to_read = @sum(total_bytes_to_read)
>

- **tapset库：**
>       SystemTap提供了tapset库（通常情况下，安装在/usr/share/systemtap/tapset文件夹），类似于C语言的函数库libc，
>           tapset提供了函数，全局变量等供SystemTap脚本使用
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
>       https://www.kancloud.cn/digest/tcpdive/120064   内核调试神器SystemTap — 探测点与语法（二）
>       https://tcler.github.io/2017/09/11/systemtap-modify-syscall-parameters/     systemtap 修改系统调用参数（详细介绍）
>       http://blog.yufeng.info/archives/2033   systemtap如何跟踪libc.so
>       https://blog.csdn.net/wangzuxi/article/details/44901285   SystemTap使用技巧【四】
>       https://vcpu.me/systemtap-skills/   systemtap能做什么？第一篇
>       http://baotiao.github.io/2017/06/14/systemtap-pika/     使用systemtap 找内存泄露问题
>       http://bean-li.github.io/systemtap-check-memory-leak/   SystemTap 定位 Memory Leak
>       http://www.lenky.info/archives/tag/systemtap
>           Linux Kprobes介绍 && 使用systemtap调试Linux内核 && 如何追踪函数的完整调用过程 && systemtap初试用
>       http://blog.yufeng.info/archives/tag/systemtap
>           巧用Systemtap注入延迟模拟IO设备抖动 && Linux下如何知道文件被那个进程写
>           GLIBC 2.16 支持systemtap静态检查点 && MYSQL数据库网卡软中断不平衡问题及解决方案
>       https://www.v2ex.com/t/387987   SystemTap 使用技巧之三 (跟踪进程执行流程)
>       https://blog.csdn.net/wangzuxi/article/category/2647873
>           SystemTap使用技巧【一】 && SystemTap使用技巧【二】 && SystemTap使用技巧【三】 && SystemTap使用技巧【四】 && systemtap双指针（多级指针）解引用
>       https://github.com/vincentbernat/systemtap-cookbook/blob/master/tcp     用python写stap程序
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
