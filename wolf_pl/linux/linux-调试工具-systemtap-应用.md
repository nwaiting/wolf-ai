## linux - systemtap 应用
- **概述：**
>
>
>
>
>
>
>
>

- **观测某个函数在哪里调用:**
>       cat stack_of_func.stp
>       probe process("home/ning/mongodb/mongo/bin/mongod").function("mongo::Matcher::matchesDotted").return {
>           printf("%s returned \n", probefunc());
>           print_ustack(ubacktrace());
>           //printf("%s\n",$$locals$$);
>       }
>       stap --ldd -d home/ning/mongodb/mongo/bin/mongod --all-modules stack_of_func.stp
>
>

- **定位函数调用堆栈：**
>       probe process("/usr/local/ppngx/sbin/nginx").function("*").call {
>                   printf("=========== %s -> %s\n", thread_indent(4), ppfunc());
>       }
>
>       probe process("/usr/local/ppngx/sbin/nginx").function("*").return {
>                   printf("%s <- %s\n", thread_indent(-4), ppfunc());
>       }
>       解释：
>           thread_indent(n): 补充空格
>           ppfunc(): 当前探测点所在的函数
>           在call探测点调用 thread_indent(4)补充 4 个空格，在 return 探测点调用 thread_indent(-4)回退 4 个空格
>

- **改变变量的值：**
>       probe process("./stap_set_var").statement("main@./stap_set_var.c:17") {
>           $p->id = 222;
>           printf("$p$: %s\n", $p$)
>       }
>       表示在stap_set_var.c文件的main函数的17行改变变量的值
>       stap -g stap_set_var.stp -c ./stap_set_var
>       (需要注意的是 stap 要加-g 参数在 guru 模式下才能修改变量的值)
>
>

- **查看代码执行路径：**
>       probe process("/home/admin/tengine/bin/nginx").statement("ngx_http_process_request@src/http/ngx_http_request.c:*") {
>           printf("%s\n", pp())
>       }
>       pp(): 输出当前被激活的探测点
>       stap ngx_http_process_request.stp   可以看出该函数哪些行被执行了
>

- **收集网络包个数. (net.stp)**
>        global recv, xmit
>        probe netdev.receive {
>          recv[dev_name, pid(), execname()] <<< length
>        }
>        probe netdev.transmit {
>          xmit[dev_name, pid(), execname()] <<< length
>        }
>
>        probe end {
>          printf("\nEnd Capture\n\n")
>          printf("Iface Process........ PID.. RcvPktCnt XmtPktCnt\n")
>          foreach ([dev, pid, name] in recv) {
>            recvcount = @count(recv[dev, pid, name])
>            xmitcount = @count(xmit[dev, pid, name])
>            printf( "%5s %-15s %-5d %9d %9d\n", dev, name, pid, recvcount, xmitcount )
>          }
>
>          delete recv
>          delete xmit
>        }
>

- **Systemtap辅助设置tcp_init_cwnd,免对操作系统打Patch：**
>       probe kernel.function("tcp_init_cwnd").return {
>           $return = $1
>       }
>

- **systemtap的网络监控应用和系统应用：**
>       https://segmentfault.com/a/1190000000680628     几种可以用来监测和调查不同的子系统的 SystemTap 脚本
>       https://sourceware.org/systemtap/SystemTap_Beginners_Guide/useful-systemtap-scripts.html    几种可以用来监测和调查不同的子系统的 SystemTap 脚本
>       http://blog.yufeng.info/archives/2497   dropwatch 网络协议栈丢包检查利器
>
>

- **待续：**
>       参考：https://www.v2ex.com/t/387987
>
>
>
>
>
>
>
>
