### http - err
- **概述**
>
>
>

- **监听套接字队列：**
>       listen函数的第二个参数为backlog. 这个参数的意义在不同的Linux内核版本或操作系统定义是不同的.
>
>       在Linux2.2以前的版本中, backlog的值是未完成连接建立的socket队列长度
>       在Linux2.2以后的版本中,backlog的值就是指代已经完成连接建立, 等待accept调用的socket队列最大长度。未完成连接建立的队列最大长度可以由/proc/sys/net/ipv4/tcp_max_syn_backlog配置来控制
>
>       listen之后内核为给定的监听套接字维护两个队列：
>           1、未完成连接队列
>               已接受客户端的SYN分节，而且已经发送了第二个SYN分节和第一个SYN分节的ACK
>           2、已完成连接队列
>               在未连接基础上接受到了客户端的ACK响应，TCP3路握手完成（此时accept并没有参与），等待accept从该队列头返回
>
>       未完成连接队列和已完成连接队列大小设置：
>           已完成连接队列的数目是由backlog指定的，那么未完成队列的数目又是多少？
>           Berkeley给出了一个模 糊因子，backlog乘以1.5得到两个队列数目之和。假如backlog=10，那么未完成连接队列数目就是5。
>
>       注:
>           当队列已满时，一个客户SYN到达时，服务器的TCP就忽略该分节（一般不向客户端发送RST），让对端 的TCP重传机制来处理。
>           如果有黑客编写了一个以高速率给受害主机发送SYN的程序，就会导致正常的客户SYN排不上队，这就是 SYN flooding攻击。主流的解决方法是从防火墙那里入手，确保到达服务器的TCP连接都是正常。
>
>       建立Tcp连接需要3次握手, 因此在一个连接的状态变为ESTABLISHED之前,它会有一个过渡的中间状态SYN RECEIVED：
>           TCP/IP协议栈就有2种方法来实现一个处于listen状态SOCKET连接：
>           1、只使用一个队列, 也就是说未成功建立连接的和已经成功建立连接的socket都放入一个队列.但是只有处于状态ESTABLISHED的socket才能被应用程序调用accept获取.
>           2、使用2个队列, 一个队列保存处于状态SYN RECEIVED的socket, 一个队列保存已经成功建立连接的socket.在历史上BSD采用这种实现方式.
>
>

- **Broken Pipe：**
>       前端的nginx(或其他客户端)已经等待超时，关闭了这个连接。当FPM处理完之后，再往这个SOCKET ID 写数据时，却发现连接已关闭，得到的是“error: Broken Pipe”
>
>

- **SYN超时：**
>       SYN超时一般通过抓包查看
>       一般SYN 超时是由于服务端backlog引起的
>       SYN超时一般是服务器端完成连接队列满导致的
>       注：
>           backlog的定义是已连接但未进行accept处理的SOCKET队列大小，已是(并非syn的SOCKET队列)
>           backlog参数就是指已完成连接队列的个数
>           backlog 即上述已完成队列的大小, 这个设置是个参考值,不是精确值. 内核会做些调整, 大于/proc/sys/net/core/somaxconn, 则取somaxconn的值
>
>

- **网络问题分析：**
>       网络问题，如连接慢、下载慢等问题，直接使用抓包查看问题
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
>     参考：http://bbs.learnfuture.com/topic/6281
>           https://blog.pytool.com/linux/linux-backlog%E6%80%A7%E8%83%BD%E5%88%86%E6%9E%90/    Linux php-fpm backlog参数潜在问题
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
