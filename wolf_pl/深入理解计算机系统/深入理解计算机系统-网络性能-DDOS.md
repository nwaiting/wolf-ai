## 深入理解计算机系统 - 网络性能 - DDOS
- **概述**
>
>       常用命令：
>           1、netstat
>               查看连接数 netstat -np
>           2、iptables
>               限制ip访问
>               a、找出源 IP 后，要解决 SYN 攻击的问题，只要丢掉相关的包就可以
>                   iptables -I INPUT -s 192.168.0.2 -p tcp -j REJECT
>               b、限制 syn 并发数为每秒 1 次
>                   iptables -A INPUT -p tcp --syn -m limit --limit 1/s -j ACCEPT
>               c、限制单个 IP 在 60 秒新建立的连接数为 10
>                   iptables -I INPUT -p tcp --dport 80 --syn -m recent --name SYN_FLOOD --update --seconds 60 --hitcount 10 -j REJECT
>           3、sysctl
>               sysctl 命令修改的配置都是临时的，重启后这些配置就会丢失。
>                   为了保证配置持久化，你还应该把这些配置，写入 /etc/sysctl.conf 文件中。
>                   写入 /etc/sysctl.conf 的配置，需要执行 sysctl -p 命令后，才会动态生效。
>
>               查看半连接数量限制：
>                   sysctl net.ipv4.tcp_max_syn_backlog
>               设置半连接数量：
>                   sysctl -w net.ipv4.tcp_max_syn_backlog=1024
>               设置重试次数：连接为 SYN_RECV 时，如果失败的话，内核还会自动重试，并且默认的重试次数是 5 次
>                   sysctl -w net.ipv4.tcp_synack_retries=1
>           4、ping（Internet Control Message Protocol”，Internet控制消息协议）
>               通过计算 ICMP 回显响应报文与 ICMP 回显请求报文的时间差，来获得往返延时
>           5、traceroute
>               traceroute 可以知道信息从你的计算机到互联网另一端的主机是走的什么路径。
>                   当然每次数据包由某一同样的出发点（source）到达某一同样的目的地(destination)走的路径可能会不一样，但基本上来说大部分时候所走的路由是相同的。
>               traceroute 会在路由的每一跳发送三个包，并在收到响应后，输出往返延时。
>               如果无响应或者响应超时（默认 5s），就会输出一个星号。
>
>
>       总结：
>           可以用 traceroute、hping3、tcpdump、Wireshark、strace 等多种工具，来定位网络中的潜在问题。
>           可以依次从路由、网络包的收发、再到应用程序等，逐层排查，直到定位问题根源。
>
>
>

- **TCP 套接字延迟确认机制：**
>       延迟确认。是针对 TCP ACK 的一种优化机制，也就是说，不用每次请求都发送一个 ACK，而是先等一会儿（比如 40ms），看看有没有“顺风车”。
>           如果这段时间内，正好有其他包需要发送，那就捎带着 ACK 一起发送过去。当然，如果一直等不到其他包，那就超时后单独发送 ACK。
>
>        TCP 套接字设置了TCP_QUICKACK ：
>           TCP 套接字专门设置了TCP_QUICKACK ，才会开启快速确认模式；否则，默认情况下，采用的就是延迟确认机制：
>

- **Nagle 算法（纳格算法）：**
>       只有设置了 TCP_NODELAY 后，Nagle 算法才会禁用。
>
>       Nagle 算法，是 TCP 协议中用于减少小包发送数量的一种优化算法，目的是为了提高实际带宽的利用率。
>       例如：当有效负载只有 1 字节时，再加上 TCP 头部和 IP 头部分别占用的 20 字节，整个网络包就是 41 字节，这样实际带宽的利用率只有 2.4%（1/41）。
>            往大了说，如果整个网络带宽都被这种小包占满，那整个网络的有效利用率就太低了。
>            Nagle 算法正是为了解决这个问题。它通过合并 TCP 小包，提高网络带宽的利用率。
>            Nagle 算法规定，一个 TCP 连接上，最多只能有一个未被确认的未完成分组；在收到这个分组的 ACK 前，不发送其他分组。这些小分组会被组合起来，并在收到 ACK 后，用同一个分组发送出去。
>

- **DDOS类型：**
>       1、带宽耗尽
>           带宽耗尽后，就会发生网络拥堵，从而无法传输其他正常的网络报文
>       2、耗尽操作系统资源
>           一旦资源耗尽，系统就不能处理其他正常的网络连接
>       3、消耗应用程序资源
>

- **防御DDOS：**
>       1、设置内核参数
>           比如增加半连接数量限制
>       2、TCP SYN Cookies 也是一种专门防御 SYN Flood 攻击的方法
>           SYN Cookies基于连接信息（包括源地址、源端口、目的地址、目的端口等）以及一个加密种子（如系统启动时间），计算出一个哈希值（SHA1），这个哈希值称为 cookie。
>           然后，这个 cookie 就被用作序列号，来应答 SYN+ACK 包，并释放连接状态。
>           当客户端发送完三次握手的最后一次 ACK 后，服务器就会再次计算这个哈希值，确认是上次返回的SYN+ACK 的返回包，才会进入 TCP 的连接状态。
>           因而，开启 SYN Cookies 后，就不需要维护半开连接状态了，进而也就没有了半连接数的限制。
>           注意，开启 TCP syncookies 后，内核选项net.ipv4.tcp_max_syn_backlog 也就无效了。
>       3、可以购买专业的流量清洗设备和网络防火墙，在网络入口处阻断恶意流量，只保留正常流量进入数据中心的服务器
>
>       总结：
>           在实际应用中，我们通常要让 Linux 服务器，配合专业的流量清洗以及网络防火墙设备，一起来缓解这一问题。！！！
>

- **ping原理：**
>       ping 基于ICMP（Internet Control Message Protocol”，Internet控制消息协议）协议，它通过计算 ICMP 回显响应报文与 ICMP 回显请求报文的时间差，来获得往返延时。
>       是TCP/IP协议族的一个子协议，用于在IP主机、路由器之间传递控制消息。 它是用来检查网络是否通畅或者网络连接速度的命令。
>
>       traceroute 会在路由的每一跳发送三个包，并在收到响应后，输出往返延时。如果无响应或者响应超时（默认 5s），就会输出一个星号。
>
>       这个过程并不需要特殊认证，常被很多网络攻击利用，比如端口扫描工具nmap、组包工具 hping3 等等。
>       所以，为了避免这些问题，很多网络服务会把 ICMP 禁止掉，这也就导致我们无法用 ping，来测试网络服务的可用性和往返延时。
>           这时，你可以用 traceroute 或 hping3 的 TCP 和 UDP 模式，来获取网络延迟。
>

- **待续：**
>       参考：https://www.cnblogs.com/luoahong/p/11539979.html     TCP 延迟确认
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
