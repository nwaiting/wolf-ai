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
