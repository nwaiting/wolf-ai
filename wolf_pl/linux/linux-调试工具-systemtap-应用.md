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
>

- **获取探测点的上下文变量：**
>       probe kernel.function("filp_close") {
>            printf("%s %d: %s(%s:%d)\n",
>            execname(),
>            pid(),
>            ppfunc(),
>            kernel_string($filp->f_path->dentry->d_iname),
>            $filp->f_path->dentry->d_inode->i_ino);
>       }
>       在探测点处理函数所在的上下文种获取，可以直接使用被跟踪函数的参数变量等
>
>

- **希望找出访问/dev/vdb的进程：**
>       iotop 也可以观察进程的动态I/O
>       iostat等命令看到的是系统级的统计，比如下例中我们看到/dev/vdb很忙，如果要追查是哪个进程导致的I/O繁忙，应该怎么办？
>           1、pidstat 命令，它就是利用了/proc/<pid>/io 中的原始数据计算单位时间内的增量
>           2、 iotop 也可以观察进程的动态I/O
>       pidstat 和 iotop 也有不足之处，它们无法具体到某个硬盘设备，如果系统中有很多硬盘设备，都在忙，而我们只想看某一个特定的硬盘的I/O来自哪些进程，这两个命令就帮不上忙了。怎么办呢？
>
>     probe kernel.function("submit_bio") {
>  　　　　dev = $bio->bi_bdev->bd_dev
>  　　　　if (dev == device_of_interest)
>    　　　　　　printf ("[%s](%d) dev:0x%x rw:%d size:%d\n",
>           　　　　　　 execname(), pid(), dev, $rw, $bio->bi_size)
>　　　}
>
>
>
>

- **定位函数调用堆栈：**
>       probe process("/usr/local/ppngx/sbin/nginx").function("*").call {
>                   printf("=========== %s -> %s(%s)\n", thread_indent(4), ppfunc(), $$parms);
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
>       https://tcler.github.io/2017/09/11/systemtap-modify-syscall-parameters/     systemtap 修改系统调用参数
>       https://zhengheng.me/2015/02/11/systemtap-analy/    分析一个进程的读写效率
>
>
>
>
>
>
