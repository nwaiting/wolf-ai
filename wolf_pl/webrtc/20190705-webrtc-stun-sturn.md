### webRTC stun sturn
- **概述：**
>       STUN（Simple Traversal of UDP over NATs，NAT 的UDP简单穿越）是一种网络协议，它允许位于NAT（或多重NAT）后的客户端找出自己的公网地址，
>           查出自己位于哪种类型的NAT之后以及NAT为某一个本地端口所绑定的Internet端端口。这些信息被用来在两个同时处于NAT 路由器之后的主机之间建立UDP通信。该协议由RFC 3489定义。
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
>       10:24:32,549  - INFO [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: constructor, stunserver: 216.93.246.18, stunPort: 3478, minPort: 40000, maxPort: 50000
        10:24:32,549  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding mediaStream, id: b7b6816fcd966369bda389a25711f756
        10:24:32,615  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote SDP
        10:24:32,616  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: processing remote SDP
        10:24:32,617  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Creating videoTransport, ufrag: KDyD, pass: smTIKg0CrCALj6qGKfGvXZS9
        10:24:32,617  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: constructor, transportName: video, isBundle: 1
        10:24:32,618  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: creating active-client
        10:24:32,618  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: created
        10:24:32,618  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: starting ice
        10:24:32,618  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: creating Nice Agent
        10:24:32,618  - DEBUG [0x7f67d75fe700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: starting g_main_loop, this: 0x7f67dc3d0f40
        10:24:32,618  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting stun, stun_server: 216.93.246.18, stun_port: 3478
        10:24:32,618  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: adding stream, iceComponents: 1
        10:24:32,618  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote credentials in constructor, ufrag:KDyD, pass:smTIKg0CrCALj6qGKfGvXZS9
        10:24:32,619  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote credentials, ufrag: KDyD, pass: smTIKg0CrCALj6qGKfGvXZS9
        10:24:32,619  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting port range, min_port: 40000, max_port: 50000
        10:24:32,619  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: gathering, this: 0x7f67dc3d0f40
        10:24:32,619  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Discovered New Candidate, candidate: a=candidate:7 1 udp 2013266431 10.200.20.84 40006 typ host generation 0
        10:24:32,620  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote SDP, stream: b7b6816fcd966369bda389a25711f756
        10:24:32,620  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote SDP, stream: b7b6816fcd966369bda389a25711f756, stream_id: b7b6816fcd966369bda389a25711f756
        10:24:32,621  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote SDP to stream, stream: b7b6816fcd966369bda389a25711f756
        10:24:32,621  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: SDP processed
        10:24:32,621  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Getting Local Sdp
        10:24:32,621  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: processing local sdp, transportName: video
        10:24:32,621  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: processed local sdp, transportName: video, ufrag: H8o8, pass: 67avgI5/OfkIKXqB+8AwE/
        10:24:32,905  - DEBUG [0x7f67d75fe700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Discovered New Candidate, candidate: a=candidate:8 1 udp 1677721855 36.152.49.161 16175 typ srflx raddr 10.200.20.84 rport 40006 generation 0
        10:24:32,922  - DEBUG [0x7f67d75fe700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: gathering done, stream_id: 1
        10:24:32,923  - INFO [0x7f67d75fe700] IceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: iceState transition, ice_config_.transport_name: video, iceState: initial, newIceState: cand_received, this: 0x7f67dc3d0f40
        10:24:32,923  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message:IceState, transportName: video, state: 1, isBundle: 1
        10:24:32,923  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  transportName: video, new_state: 2
        10:24:32,923  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Getting Local Sdp
        10:24:32,923  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: processing local sdp, transportName: video
        10:24:32,923  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: processed local sdp, transportName: video, ufrag: H8o8, pass: 67avgI5/OfkIKXqB+8AwE/
        10:24:32,923  - INFO [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  newGlobalState: 103
        10:24:32,951  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:1198673846 1 udp 2122260223 169.254.18.32 64814 typ host generation 0 ufrag KDyD network-id 1, mid: video, sdpMLine: 0
        10:24:32,952  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 1, mediaType: 0
        10:24:32,952  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: adding remote candidate, hostType: 0, hostAddress: 169.254.18.32, hostPort: 64814, priority: 2122260223, componentId: 1, ufrag: KDyD, pass: smTIKg0CrCALj6qGKfGvXZS9
        10:24:32,959  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:1896747724 1 udp 2122194687 169.254.4.50 64815 typ host generation 0 ufrag KDyD network-id 2, mid: video, sdpMLine: 0
        10:24:32,959  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 1, mediaType: 0
        10:24:32,959  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: adding remote candidate, hostType: 0, hostAddress: 169.254.4.50, hostPort: 64815, priority: 2122194687, componentId: 1, ufrag: KDyD, pass: smTIKg0CrCALj6qGKfGvXZS9
        24:32,965  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:1527417831 1 udp 2122129151 10.200.111.59 64816 typ host generation 0 ufrag KDyD network-id 3, mid: video, sdpMLine: 0
        10:24:32,966  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 1, mediaType: 0
        10:24:32,966  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: adding remote candidate, hostType: 0, hostAddress: 10.200.111.59, hostPort: 64816, priority: 2122129151, componentId: 1, ufrag: KDyD, pass: smTIKg0CrCALj6qGKfGvXZS9
        10:24:32,974  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:166835014 1 tcp 1518280447 169.254.18.32 9 typ host tcptype active generation 0 ufrag KDyD network-id 1, mid: video, sdpMLine: 0
        10:24:32,974  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 0, mediaType: 0
        10:24:32,979  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:1066266172 1 tcp 1518214911 169.254.4.50 9 typ host tcptype active generation 0 ufrag KDyD network-id 2, mid: video, sdpMLine: 0
        10:24:32,979  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 0, mediaType: 0
        10:24:32,985  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:361330455 1 tcp 1518149375 10.200.111.59 9 typ host tcptype active generation 0 ufrag KDyD network-id 3, mid: video, sdpMLine: 0
        10:24:32,985  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 0, mediaType: 0
        10:24:32,992  - DEBUG [0x7f67fd981800] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: Adding remote Candidate, candidate: a=candidate:3661794643 1 udp 1685921535 114.86.193.199 43544 typ srflx raddr 10.200.111.59 rport 64816 generation 0 ufrag KDyD network-id 3, mid: video, sdpMLine: 0
        10:24:32,992  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: setting remote candidates, candidateSize: 1, mediaType: 0
        10:24:32,992  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: adding relay or srflx remote candidate, hostType: 1, hostAddress: 114.86.193.199, hostPort: 43544, rAddress: 10.200.111.59, rPort: 64816
        10:24:33,680  - DEBUG [0x7f67d75fe700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: new ice component state, newState: 2, transportName: video, componentId 1, iceComponents: 1
        10:24:33,680  - INFO [0x7f67d75fe700] IceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: iceState transition, ice_config_.transport_name: video, iceState: cand_received, newIceState: ready, this: 0x7f67dc3d0f40
        10:24:33,680  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message:IceState, transportName: video, state: 2, isBundle: 1
        10:24:33,680  - INFO [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: DTLSRTP Start, transportName: video
        10:24:33,681  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: Sending DTLS message, transportName: video, componentId: 1
        10:24:33,698  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: Received DTLS message, transportName: video, componentId: 1
        10:24:33,701  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: Sending DTLS message, transportName: video, componentId: 1
        10:24:33,719  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message: Received DTLS message, transportName: video, componentId: 1
        10:24:33,720  - DEBUG [0x7f67ef9b1700] DtlsTransport - id: 582a4db011a1f3d566af950d12b73c96,  message:HandShakeCompleted, transportName:video, readyRtp:1, readyRtcp:1
        10:24:33,720  - DEBUG [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  transportName: video, new_state: 3
        10:24:33,720  - DEBUG [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: selected pair, local_addr: 10.200.20.84, local_port: 40006, local_type: host
        10:24:33,720  - INFO [0x7f67ef9b1700] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: selected pair, remote_addr: 10.200.111.59, remote_port: 64816, remote_type: host
        10:24:33,720  - INFO [0x7f67ef9b1700] WebRtcConnection - id: 582a4db011a1f3d566af950d12b73c96,  newGlobalState: 104
>
>
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
>
>
>
>
>
