# stap 实例
- **概述：**
>       安装systemtap后，在/usr/share/systemtap/examples/ 目录中，有很多测试用例
>
>       首先可通过stap -L 查看函数中的哪些变量可以被看到,后面写脚本时可以直接引用这些变量
>           如：stap -L 'process("/lib64/libc.so.6").function("malloc")'
>               或者 stap -L 'kernel.statement("*@arch/x86/kernel/cpu/perf_event.c:824")'
>
>       stap func_call.stp -d /home/pplive/work/test_stap/test_cpp/main --ldd -x 12345
>
>       statement定位到具体的line或者函数，将这些定位点作为跟踪点
>           func@file:linenumber
>           如：stap -L 'kernel.statement("*@arch/x86/kernel/cpu/perf_event.c:824")'
>               或者 stap -L 'process("/usr/local/ppngx/sbin/nginx").statement("ngx_netcall_create_ctx")'
>               或者 stap -L 'process("/usr/local/ppngx/sbin/nginx").statement("*@ngx_netcall.c:99")'
>
>       stap -l 可以查看某个函数在哪个文件的哪一行定义的，可以是内核代码也可以是用户态代码
>           如：stap -l 'process("/lib64/libc.so.6").function("malloc")'
>               或者 stap -l 'process("/usr/local/ppngx/sbin/nginx").statement("*@ngx_netcall.c:99")'
>
>       stap统计c++程序：
>           function("operator new")：$sz 表示new申请的字节数
>           function("operator delete")：$ptr：应该就是地址
>           probe process("main").library("libstdc++.so.6").{function("operator new"), function("operator delete")} {
>               print_ustack(ubacktrace())
>               printf("========== %s\n",ppfunc())
>           }
>       参考：http://sourceware-org.1504.n7.nabble.com/Systemtap-Probe-C-new-and-delete-Operator-td407597.html
>       解释：
>           operator new/operator delete,operator new[]/operator delete[]是标准库函数，用法和malloc/free的用法一样，只负责分配/释放空间，
>               但实际上operator new/operator delete只是malloc/free的一层封装
>               函数申明：
>                   void* operator new(size_t size);
>                   void operator delete(size_t size);
>                   void* operator new[](size_t size);
>                   void operator delete[](size_t size);
>           new和delete：
>               new：先调用operator new分配空间，再调用构造函数初始化空间。
>               new[n]：调用operator new分配空间，再调用n次构造函数初始化对象。
>               delete：先调用析构函数清理对象，再调用operator delete释放空间
>               delete[n]：调用n次析构函数清理对象，再调用operator delete释放空间。
>

- **systemtap安装：**
>       https://www.cnblogs.com/wipan/p/9333623.html    systemtap安装
>       https://segmentfault.com/a/1190000000671438     SystemTap 学习笔记 - 安装篇
>       https://www.cnblogs.com/the-tops/p/5715854.html     debuginfo-install安装
>           http://ftp.riken.jp/Linux/scientific/6.2/archive/debuginfo/
>           http://www.rpm-find.net/linux/rpm2html/search.php?query=kernel-devel
>           https://oss.oracle.com/el6/debuginfo/
>           http://vault.centos.org/6.2/os/x86_64/Packages
>
>       Systemtap looks for the debug info in these locations
>           /boot/vmlinux-`uname -r`
>           /usr/lib/debug/lib/modules/`uname -r`/vmlinux
>           /lib/modules/`uname -r`/vmlinux
>
>
>       1、安装如下两个RPM包
>           systemtap
>           systemtap-runtime
>       2、在运行SystemTap之间，还需要装必要的内核信息包。在现代系统上，可以运行如下stap-prep来安装这些包
>           stap-prep
>           运行stap-prep的时候，它探测出还要安装kernel-devel-3.10.0-693.2.2.el7.x86_64包和kernel-debuginfo-3.10.0-693.2.2.el7.x86_64包
>               (实际上还有kernel-debuginfo-common包)，但是自动安装失败。需要手动安装。
>               kernel-debuginfo
>               kernel-debuginfo-common
>               kernel-devel
>           注意：不要直接yum install kernel-debuginfo kernel-debuginfo-common kernel-devel, 即使能找到相应的包，也是安装的最新版本，不会自动匹配当前版本。
>               所以下载RPM包，再用rpm命令依次安装
>
>

- **修改变量的值：**
>       修改show_value变量的值：
>       probe process("/home/pplive/work/test_stap/test_cpp/main").function("Solution::show") {
>           $this->show_value = 1
>       }
>       stap func_cpp.stp -g -d /home/pplive/work/test_stap/test_cpp/main --ldd -x 54945
>

- **打印变量的值：**
>       1、先转换类型，在输出类型
>           printf("type=%d\n", @cast($cand, "CandidateInfo")->hostType)
>
>
>
>
>

- **耗时统计直方图：**
>       @hist_linear(v, start, stop, interval) # 打印start-stop区间interval间隔的直方图
>       @hist_log(v)       # 打印以2为底指数分布的直方图
>
>       例如：
>           global sends # 声明全局的统计存储容器
>
>           # function中为函数名，同时支持通配符*等，在该函数return时计算耗时
>           probe process("/home/pplive/work/test_stap/test_cpp/main").function("*").return {
>               # 以微秒精度来统计，entry方法将一个表达式放置于函数入口处
>               sends <<< gettimeofday_us() - @entry(gettimeofday_us())
>           }
>
>           probe timer.s(10) {
>               print(@hist_log(sends))
>               # 清空数据
>               delete sends
>           }
>


- **待续：**
>       参考：https://jin-yang.github.io/post/linux-systemtap.html     Systemtap
>           https://consen.github.io/2018/01/04/systemtap/  SystemTap（Cuckoo沙箱Linux检测引擎就使用了SystemTap）
>           https://spacewander.gitbooks.io/systemtapbeginnersguide_zh/content/6_1_ParseAndSemanticErrors.html  systemtap详解
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
