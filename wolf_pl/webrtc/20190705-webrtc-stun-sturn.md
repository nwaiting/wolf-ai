### webRTC stun sturn
- **概述：**
>       STUN（Simple Traversal of UDP over NATs，NAT 的UDP简单穿越）是一种网络协议，它允许位于NAT（或多重NAT）后的客户端找出自己的公网地址，
>           查出自己位于哪种类型的NAT之后以及NAT为某一个本地端口所绑定的Internet端端口。这些信息被用来在两个同时处于NAT 路由器之后的主机之间建立UDP通信。该协议由RFC 3489定义。
>
>       candidate的ip排序：
>           优先级排序依次是：主机候选地址>反射地址>中继后选项
>           host > srvflx > prflx > relay
>

- **ICE：**
>       ICE跟STUN和TURN不一样，ICE不是一种协议，而是一个框架（Framework），它整合了STUN和TURN
>
>       ICE全称Interactive Connectivity Establishment：
>           交互式连通建立方式
>       ICE参照RFC5245建议实现，是一组基于offer/answer模式解决NAT穿越的协议集合
>           它综合利用现有的STUN，TURN等协议，以更有效的方式来建立会话
>       客户端侧无需关心所处网络的位置以及NAT类型，并且能够动态的发现最优的传输路径
>
>       ICE试着找最好的路径来让客户端建立连接,他会尝试所有可能的选项,然后选择最合适的方案,ICE首先尝试P2P连接,如果失败就会通过Turn服务器进行转接
>
>       stun和turn服务的作用主要处理打洞与转发，配合完成ICE协议
>           1、首先尝试使用P2P
>           2、如果失败将求助于TCP，使用turn转发两个端点的音视频数据，turn转发的是两个端点之间的音视频数据不是信令数据
>           因为turn服务器是在公网上，所以他能被各个客户端找到，另外turn服务器转发的是数据流，很占用带宽和资源
>

- **Binding Request/Response：**
>       https://www.cnblogs.com/pannengzhi/p/5061674.html   P2P通信标准协议(三)之ICE
>       https://www.jzgwind.com/?p=973  P2P网络节点间如何互访——详解STUN方式NAT穿透
>       response的源IP和端口等于Binding Request的目的IP和端口
>       response的目的IP和端口等于Binding Request的源IP和端口
>
>       由于STUN Binding request用来进行连接性测试,因此STUN Binding response中会包含终端的实际地址
>       如果这个地址和之前学习的所有地址都不匹配,发送方就会生成一个新的candidate,称为PEER REFLEXIVE CANDIDATE,和其他candidate一样,也要通过ICE的检查测试
>
>       STUN request的发送和接收地址都是接下来进多媒体传输(如RTP和RTCP)的地址和端口,所以,客户端实际上是将STUN协议与RTP/RTCP协议在数据包中进行复用(而不是在端口上复用).
>
>       终端收到成功响应之后,先检查其mapped address是否与本地记录的地址对有匹配,如果没有则生成一个新的候选地址.即对等端的反射地址.如果有匹配,则终端会构造一个可用候选地址对(valid pair)。
>           通常很可能地址对不存在于任何检查列表中,检索检查列表中没有被服务器反射的本地地址,这些地址把它们的本地候选转换成服务器反射地址的基地址,并把冗余的地址去除掉。
>
>       Candidate pair：
>           由本端和远端candidate组成的pair，有自己的优先级
>           由连通性检查成功的candidate pair按优先级排序的链表,用于ICE提名和选择最终路径
>           在本端收到远端candidates后，将Component ID和transport protocol相同的candidates组成pair
>           修整candidate pair，如果是srvflx地址，则需要用其base地址替换
>           STUN 检查请求中需要检查地址的对称性，请求的源地址是响应的目的地址，请求的目的地址是响应的源地址，否则都设置状态为 Failed   ！！！
>

- **STUN消息属性：**
>       属性类型定义：
>           MAPPED-ADDRESS：
>               MAPPED-ADDRESS属性表示映射过的IP地址和端口。它包括8位的地址族，16位的端口号及长度固定的IP地址。
>           RESPONSE-ADDRESS：
>               RESPONSE-ADDRESS属性表示响应的目的地址
>           CHASNGE-REQUEST：
>               客户使用32位的CHANGE-REQUEST属性来请求服务器使用不同的地址或端口号来发送响应
>           SOURCE-ADDRESS：
>               SOURCE-ADDRESS属性出现在捆绑响应中，它表示服务器发送响应的源IP地址和端口
>           CHANGED-ADDRESS：
>               如果捆绑请求的CHANGE-REQUEST属性中的“改变IP”和“改变端口”标志设置了，则CHANGED-ADDRESS属性表示响应发出的IP地址和端口号
>           XOR-RELAYED-ADDRESS：
>               值为该allocation的中继传输地址
>           XOR-MAPPED-ADDRESS：
>               值为客户端的server-reflexive地址
>

- **STUN响应：**
>       在主叫端处于对称型NAT，被叫端处于端口限制型NAT情况下：
>           被叫端的主机地址向主叫端的中继地址发送STUN BINDING 包的时候，在被叫端产生了 Prflx地址,
>               此地址主叫端从请求包的SOURCE_ADDRESS（此处说的SOURCE_ADDRESS是指到来的请求rcheck的src_addr字段）取出
>           据此，主叫端可以判定被叫端处于对称NAT，主叫端给被叫端响应，注入MAPPPED_ADDRESS字段值，被叫端收到响应据此可以判断自身处在对称NAT之下。
>
>       主叫A,被叫B：
>           发包路径：B主机----A中继地址----STUN3478----A主机（SOURCE_ADDRESS）
>           接收到服务器来的包之后，主叫端给被叫端响应,把Prflx地址放入MAPPPED_ADDRESS字段值
>           响应路径：A主机----STUN3478----B中继地址----B主机（MAPPPED_ADDRESS）
>

- **STUN协议：**
>       STUN协议在RFC5389中被重新命名为Session Traversal Utilities for NAT，即NAT会话穿透效用
>       在这里，NAT会话穿透效用被定位为一个用于其他解决NAT穿透问题协议的协议。它可以用于终端设备检查由NAT分配给终端的IP地址和端口号。
>           同时，它也被用来检查两个终端之间的连接性，好比是一种维持NAT绑定表项的保活协议。
>       STUN可以用于多种NAT类型，并不需要它们提供特殊的行为
>
>       STUN本身不再是一种完整的NAT穿透解决方案，它相当于是一种NAT穿透解决方案中的工具。
>

- **STUN用途：**
>       目前定义了三种STUN用途：
>           1、Interactive Connectivity Establishment（ICE）[MMUSIC-ICE]，交互式连接建立
>           2、Client-initiated connections for SIP [SIP-OUTBOUND]，用于SIP的客户端初始化连接
>           3、NAT Behavior Discovery [BEHAVE-NAT]，NAT行为发现
>
>       Classic STUN（RFC3489）：
>           Classic STUN 有着诸多局限性，比如：
>               1、不能确定获得的公网映射地址能否用于P2P通信
>               2、没有加密方法
>               3、不支持TCP穿越
>               4、不支持对称型NAT的穿越
>               5、不支持IPV6
>
>       STUN（RFC5389）：
>           RFC5389是RFC3489的升级版，比如：
>               1、支持UDP/TCP/TLS协议
>               2、支持安全认证
>
>       ICE利用STUN（RFC5389） Binding Request和Response，来获取公网映射地址和进行连通性检查，同时扩展了STUN的相关属性：
>           1、PRIORITY：在计算candidate pair优先级中使用
>           2、USE-CANDIDATE：ICE提名时使用
>           3、tie-breaker：在角色冲突时使用
>
>

- **NAT类型：**
>       NAT（Network Address Translation）是将IP 数据包头中的IP 地址转换为另一个IP 地址的过程，通俗来讲，就是局域网，公用一个public IP。
>       NAT作用：
>           1、NAT的本质就是让一群机器公用同一个IP。这样就暂时解决了IP短缺的问题。
>           2、其实NAT还有一个重要的用途，就是保护NAT内的主机不受外界攻击。
>       一个终端一般都在一个NAT内，NAT会有一个网关路由，对外暴露一个public IP
>
>       NAT类型：
>           1、Full Cone     全锥形NAT
>               IP、端口都不受限。只要客户端由内到外打通一个洞之后（NatIP:NatPort –> A:P1），其他IP的主机(B)或端口(A:P2)都可以使用这个洞发送数据到客户端。
>           2、Restricted Cone   受限锥形NAT
>               IP受限，端口不受限。当客户端由内到外打通一个洞之后(NatIP:NatPort –> A:P1)，A机器可以使用他的其他端口（P2）主动连接客户端，但B机器则不被允许。
>               Restricted Cone限制了外部进入内部的IP，使得只有被打洞IP发出的数据包才允许进入NAT
>           3、Restricted Port Cone  端口受限锥型
>               IP、端口都受限。返回的数据只接受曾经打洞成功的对象（A:P1），由A:P2、B:P1发起的数据将不被NatIP:NatPort接收。
>               Restricted Port Cone不但限制了IP，还限制了端口，使得只有被打洞的IP:PORT才能往这个洞里发送数据，其他任何来自不同于被打洞地址（IP:PORT）的数据包都不能使用这个洞将数据发送到NAT之后
>           Cone NAT指的是只要源IP端口不变，无论发往的目的IP是否相同，在NAT上都映射为同一个端口，形象的看来就像锥子一样
>
>           4、Symmetric NAT     对称型NAT
>               对称型NAT具有端口受限锥型的受限特性。但更重要的是，他对每个外部主机或端口的会话都会映射为不同的端口（洞）。只有来自相同的内部地址（IP:PORT）并且发送到相同外部地址（X:x）的请求，在NAT上才映射为相同的外网端口，即相同的映射。
>               因为每一次连接端口都不一样，所以对方无法知道在对称NAT的client下次用什么端口。 无法完全实现p2p传输（预测端口除外），需要turn server做一个relay，即所有消息通过turn server转发
>               Symmetric NAT对于发往不同目的IP的会话在NAT上将映射为不同的端口，也就是不同的会话。
>               对称型NAT具有端口受限锥型的受限特性。但更重要的是，他对每个外部主机或端口的会话都会映射为不同的端口（洞）。只有来自相同的内部地址（IP:PORT）并且发送到相同外部地址（X:x）的请求，
>                   在NAT上才映射为相同的外网端口，即相同的映射。一个外部地址（X:x）对应一个NAT上的映射，如上图红色三角，每个映射仅接收来自他绑定的外部地址的数据。注：X在这里意为任意一台外部主机，x为这台主机上的任意一个端口。
>               映射关系：
>                   Client->NatIP:Pa1->A:P1，当Client访问B:P1时，映射关系变为：Client->NatIP:Pb->B:P1，同理，NatIP:Pa2也就是Client访问A:P2时的映射
>
>

- **NAT技术：**
>       可以同时让多个计算机同时联网，同时也隐藏了内部地址，NAT对来自外部的数据查看其NAT映射记录，对没有相应记录的数据包进行拒绝，提高了网络的安全性。
>       NAT三种实现方式：
>           1、静态地址转换：一个公网IP对应一个内部IP,一对一转换；
>           2、动态地址转换：N个公网IP对应M个内部Ip,不固定的一对一IP转换关系．同一时间，有M-N个主机无法联网；
>           3、端口多路复用：对外只有一个公网IP,通过端口来区别不同内部IP主机的数据；
>

- **webRTC的网络协议栈：**
>       如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_webrtc_network_stack.jpg)
>
>

- **NAT后的A和B如何建立连接：**
>       由于IP地址资源有限的原因，目前我们使用的各种终端设备都位于局域网后面也就是多台设备共享同一个公网IP；例如：如果位于局域网里面的一个终端Agent A要与互联网上的另一个终端Agent B通信，
>           当A发送的data packet经过局域网出口处的NAT设备时，NAT会将data packet里面的source address字段替换成相应的公网IP和Port，然后再发送data packet到Agent B。
>           Agent B看到的source address就是经过转换后的IP和Port并不知道Agent A的局域网地址；当Agent B的响应到达Agent A的NAT设备后，NAT设备查找内存中保存的和这个外网地址相对应的内网地址，
>           如果找到后就将这个data packet转发到这个地址，这样就实现了通信
>

- **webrtc的P2P穿透：**
>       webrtc的P2P穿透部分是由libjingle实现的.
>       步骤顺序大概是这样的:
>           1. 尝试直连.
>           2. 通过stun服务器进行穿透
>           3. 无法穿透则通过turn服务器中转.
>
>

- **绑定事件：**
>       candidate-gathering-done：
>           为agent绑定事件响应，本端候选地址全部收集完成时调用方法cb_candidate_gathering_done
>       component-state-changed：
>           为agent绑定事件响应，当通道的连接状态发生变化时回调方法cb_component_state_changed
>           一个agent可包含多个component，可视为多路复用一个链路
>       new-selected-pair：
>           为agent绑定事件响应，本端在接收到对端的连接候选地址，在尝试连接后，发现一个新的可通信的连接地址对时，调用方法cb_new_selected_pair
>           一个可选地址对由本端一个候选地址和对端的一个候选地址组成
>       new-candidate：
>           略
>       parse_candidate：
>           解析收集到的自已的或接收到的对方的candidate候选地址.一个候选地址主要由编号，优先级，IP地址，端口号，网络类型等几个元素组成
>
>       借助libnice实现了P2P的连接方式：
>           得到对方的地址后，会进行地址间的挨个匹对，当发现一对可用的地址对时，视为连接成功。同时通道的连接状态会发生变化 connecting —-> connected —-> ready
>

- **event事件：**
>       erizo的webrtcconnection使用监听来通知事件，其状态为：CONN_INITIAL = 101, CONN_STARTED = 102, CONN_GATHERED = 103, CONN_READY = 104, CONN_FINISHED = 105,
>           CONN_CANDIDATE = 201, CONN_SDP = 202, CONN_SDP_PROCESSED = 203,CONN_FAILED = 500
>           1、CONN_INITIAL：WebrtcConnection对象创建后，需要外面手动调用init方法，该方法会回调notifyEvent，并传递事件为改枚举值，message和stream_id均为空值
>           2、CONN_STARTED：这个状态没有看到里面有明显调用的地方，有可能是保留的状态码
>           3、CONN_GATHERED：WebrtcConnection的createOffer或者第一次setRemoteSdp时启动自身ICE过程，ICE完成收集时，发送该通知。message为自己的sdp数据
>           4、CONN_READY：当DTLS握手交互成功完成时，发送该通知
>           5、CONN_FINISH：WebrtcConnection对象关闭，调用close时，发送该通知
>           6、CONN_CANDIDATE：自身ICE获取到Candidate时，发送该通知。message为candidate信息
>           7、CONN_SDP：没有被使用
>           8、CONN_SDP_PROCESSED：处理remote sdp时，发送该通知。message为remote sdp
>           9、CONN_FAILED：ICE失败，Dtls握手交互失败，均发送该通知。message为remote sdp
>
>       webrtcconnection的使用的方法：
>           1、webrtcconnection createOffer
>           2、CONN_GATHERED时，发送sdp给client
>           3、CONN_CANDIDATE时，发送candidate给client
>           4、接收到answer，调用webrtcconnection setRemoteSdp
>           5、接收到candidate，调用webrtcconnection addRemoteCandidate
>           6、CONN_SDP_PROCESSED时，做私有处理
>           7、CONN_FAILED时，进行重试，或者其他异常处理
>

- **transport：**
>       erizo的transport部分负责网络链路处理，其包含ice处理，数据包packet处理传递
>       transport存在，主要是为Dtls-srtp数据处理提供封装，其关联着ice与外部接口webrtcconnection。
>       erizo提供了两套ICE的方案，分别使用不同的ice库，可以再iceconfig参数里进行设置。
>       erizo的DtlsTransport，提供了dtls交互，srtp加密和解密。
>       总结：
>           总结：erizo的链路数据接收模型，是定义一个listener，下一级继承listener，同级聚合listener，实现异步数据的逐级传递。
>

- **打洞过程：**
>       UDP打洞的过程大致如此：
>           1、双方都通过UDP与服务器通讯后，网关默认就是做了一个外网IP和端口号与你内网IP与端口号的映射，这个无需设置的，服务器也不需要知道客户的真正内网IP
>           2、用户A先通过服务器知道用户B的外网地址与端口
>           3、用户A向用户B的外网地址与端口发送消息
>           4、在这一次发送中，用户B的网关会拒收这条消息，因为它的映射中并没有这条规则。
>           5、但是用户A的网关就会增加了一条允许规则，允许接收从B发送过来的消息
>           6、服务器要求用户B发送一个消息到用户A的外网IP与端口号
>           7、用户B发送一条消息，这时用户A就可以接收到B的消息，而且网关B也增加了允许规则
>           8、由于网关A与网关B都增加了允许规则，所以A与B都可以向对方的外网IP和端口号发送消息
>
>
>
>

- **交互流程：**
>       if (msg.offer) { // 监听并处理通过发信通道交付的远程提议
>           pc = new RTCPeerConnection(ice);
>           pc.setRemoteDescription(msg.offer);
>           navigator.getUserMedia({ "audio": true, "video": true }, gotStream, logError);
>       } else if (msg.candidate) { // 注册远程ICE候选项以开始连接检查
>           pc.addIceCandidate(msg.candidate);
>       }
>
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/lingdhox/p/4209659.html
>           https://blog.csdn.net/glw0223/article/details/90734581      ICE之STUN协议---Binding
>           https://www.cnblogs.com/limedia/p/stun.html     Stun协议的格式记录
>           https://michaelyou.github.io/2017/08/13/ssl-traffic-analysis/   SSL/TLS 会话流量分析
>           实现简易webrtc 网关：
>           https://www.jianshu.com/p/61e3c9e13456?utm_campaign=maleskine&amp;utm_content=note&amp;utm_medium=seo_notes&amp;utm_source=recommendation
>           https://www.meiwen.com.cn/subject/ruyckftx.html     通过janus认识libnice
>           https://segmentfault.com/a/1190000015075880     聊聊 WebRTC 网关服务器1：如何选择服务端端口方案？
>           https://blog.csdn.net/chenFteng/article/details/77429453    WebRtc音视频实时通信--libnice库介绍
>           https://blog.csdn.net/w05980598/article/details/79959704    webrtc调试工具chrome://webrtc-internals介绍
>           http://diseng.github.io/2015/04/30/nat  NAT穿透的几种方式
>           http://www.pianshen.com/article/2376142785/     webrtc服务器搭建
>           http://prog3.com/sbdm/blog/liwf616/article/details/45507457     Test UDP hole penetration NAT
>           https://www.jianshu.com/p/4a15556c6318      turn协议的工作原理
>           https://cloud.tencent.com/developer/article/1005490     浅析 P2P 穿越 NAT 的原理、技术、方法 ( 下 ）
>           https://www.cnblogs.com/ishangs/p/3816689.html  STUN/TURN/ICE协议在P2P SIP中的应用（二）
>           https://blog.csdn.net/netease_im/article/details/88876286   WebRTC 之ICE浅谈 ！！！
>           https://www.cnblogs.com/mlgjb/p/8243690.html    P2P技术详解(三)：P2P技术之STUN、TURN、ICE详解
>
>
>
