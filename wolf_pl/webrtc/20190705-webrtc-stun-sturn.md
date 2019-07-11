### webRTC stun sturn
- **概述：**
>
>
>
>
>
>
>
>

- **webrtc的P2P穿透：**
>       webrtc的P2P穿透部分是由libjingle实现的.
>       步骤顺序大概是这样的:
>           1. 尝试直连.
>           2. 通过stun服务器进行穿透
>           3. 无法穿透则通过turn服务器中转.
>
>

- ****
>       candidate-gathering-done：
>           为agent绑定事件响应，本端候选地址全部收集完成时调用方法cb_candidate_gathering_done
>       component-state-changed：
>           为agent绑定事件响应，当通道的连接状态发生变化时回调方法cb_component_state_changed
>           一个agent可包含多个component，可视为多路复用一个链路
>       new-selected-pair：
>           为agent绑定事件响应，本端在接收到对端的连接候选地址，在尝试连接后，
>           发现一个新的可通信的连接地址对时，调用方法cb_new_selected_pair
>           一个可选地址对由本端一个候选地址和对端的一个候选地址组成
>       new-candidate：
>           略
>       parse_candidate：
>           解析收集到的自已的或接收到的对方的candidate候选地址.一个候选地址主要由编号，优先级，IP地址，端口号，网络类型等几个元素组成
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
10:24:32,959  - DEBUG [0x7f67fd981800] LibNiceConnection - id: 582a4db011a1f3d566af950d12b73c96,  message: adding remote candidate, hostType: 0, hostAddress: 169.254.4.50, hos
tPort: 64815, priority: 2122194687, componentId: 1, ufrag: KDyD, pass: smTIKg0CrCALj6qGKfGvXZS9
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
>
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
