## 深入理解计算机系统 - 网络性能 - NAT
- **概述**
>
>       发现网络延迟增大的情况后，可以先从路由、网络包的收发、网络包的处理，再到应用程序等，从各个层级分析网络延迟，等到找出网络延迟的来源层级后，再深入定位瓶颈所在。
>
>       不管是http请求慢还是nat网络慢，如果从业务逻辑日志中看不出具体的问题，则直接抓包分析
>
>
>       常用命令：
>           1、iptables
>               iptables -nL -t nat     确认 DNAT 规则是否已经创建
>           2、perf
>               记录网络丢包的堆栈
>               perf record -a -g -- sleep 30      # 记录一会（比如 30s）后按 Ctrl+C 结束
>               perf report -g graph,0      # 输出报告
>           3、修改linux内核配置选项
>               Linux 内核为用户提供了大量的可配置选项，可以通过 proc 文件系统，或者 sys 文件系统还可以用 sysctl 这个命令行工具，来查看和修改内核配置
>           4、查看 netfilter 相关的配置选项
>               sysctl -a | grep conntrack
>           5、查看系统内核日志
>               dmesg | tail
>           6、conntrack
>               查看连接跟踪表的内容
>               conntrack -L -o extended | head     # -L 表示列表，-o 表示以扩展格式显示
>
>

- **nat性能分析流程：**
>       当已经确认是使用nat造成延迟或网络慢（可以通过排除法或者抓包分析），分析流程：
>           1、SystemTap 检测是否发生丢包行为
>               probe kernel.trace("kfree_skb") { locations[$location] <<< 1 }      # increment a drop counter for every location we drop at
>           2、已经确认有丢包行为，然后通过perf 确认丢包具体行为
>               perf record -a -g -- sleep 30       # 记录行为
>           3、根据记录行为的线索和一些系统日志 dmesg，进一步确认问题，然后对应修改系统内核配置
>               sysctl -w net.netfilter.nf_conntrack_max=131072
>

- **Netfilter 框架：**
>       NAT 基于 Linux 内核的连接跟踪机制，实现了 IP 地址及端口号重写的功能，主要被用来解决公网 IP 地址短缺的问题
>
>       Linux 内核提供的 Netfilter 框架，允许对网络数据包进行修改（比如 NAT）和过滤（比如防火墙）
>           在这个基础上，iptables、ip6tables、ebtables 等工具，又提供了更易用的命令行接口，以便系统管理员配置和管理 NAT、防火墙的规则
>           iptables 就是最常用的一种配置工具。要掌握 iptables 的原理和使用方法，最核心的就是弄清楚，网络数据包通过 Netfilter 时的工作流向
>
>       Netfilter 框架图如下：
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/linux_pic/linux_net_netfilter_pack_flow.png)
>
>       见： https://www.cnblogs.com/luoahong/p/11540288.html
>
>

- **NAT 性能问题定位：**
>       根据Netfilter的原理，要保证 NAT 正常工作，就至少需要两个步骤：
>           1、利用 Netfilter 中的钩子函数（Hook），修改源地址或者目的地址
>           2、利用连接跟踪模块 conntrack ，关联同一个连接的请求和响应
>
>       在分析 NAT 性能问题时，
>           1、可以先从内核连接跟踪模块 conntrack 角度来分析，比如用systemtap、perf、netstat 等工具，以及 proc 文件系统中的内核选项，来分析网络协议栈的行为；
>           2、然后，通过内核选项调优、切换到无状态 NAT、使用 DPDK 等方式，进行实际优化
>
>

- **NAT原理：**
>       NAT 技术可以重写 IP 数据包的源 IP 或者目的 IP，被普遍地用来解决公网 IP 地址短缺的问题。
>           主要原理就是，网络中的多台主机，通过共享同一个公网 IP 地址，来访问外网资源。同时，由于 NAT 屏蔽了内网网络，自然也就为局域网中的机器提供了安全隔离。
>
>       既可以在支持网络地址转换的路由器（称为 NAT 网关）中配置 NAT，也可以在 Linux服务器中配置 NAT。
>           如果采用第二种方式，Linux 服务器实际上充当的是“软”路由器的角色。
>
>       根据实现方式的不同，NAT 可以分为三类：
>           1、静态 NAT
>               即内网 IP 与公网 IP 是一对一的永久映射关系；
>           2、动态 NAT
>               即内网 IP 从公网 IP 池中，动态选择一个进行映射；
>           3、网络地址端口转换 NAPT
>               网络地址端口转换 NAPT（Network Address and Port Translation），即把内网 IP 映
>           4、射到公网 IP 的不同端口上，让多个内网 IP 可以共享同一个公网 IP 地址。
>       注：
>           NAPT 是目前最流行的 NAT 类型，我们在 Linux 中配置的 NAT 也是这种类型。
>
>       NAPT 分为三类：
>           1、源地址转换 SNAT，即目的地址不变，只替换源 IP 或源端口。
>               SNAT 主要用于，多个内网 IP 共享同一个公网 IP ，来访问外网资源的场景。
>           2、目的地址转换 DNAT，即源 IP 保持不变，只替换目的 IP 或者目的端口
>               DNAT主要通过公网 IP 的不同端口号，来访问内网的多种服务，同时会隐藏后端服务器的真实IP 地址。
>           3、双向地址转换，即同时使用 SNAT 和 DNAT。
>               当接收到网络包时，执行DNAT，把目的 IP 转换为内网 IP；而在发送网络包时，执行 SNAT，把源 IP 替换为外部IP。
>
>       在使用 iptables 配置 NAT 规则时，Linux 需要转发来自其他 IP 的网络包，所以你千万不要忘记开启 Linux 的 IP 转发功能。
>           查看这一功能是否开启。如果输出的结果是 1，就表示已经开启了 IP 转发：
>               sysctl net.ipv4.ip_forward
>           写入配置：
>               sysctl -w net.ipv4.ip_forward=1
>           为了避免重启后配置丢失，不要忘记将配置写入 /etc/sysctl.conf 文件中
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
