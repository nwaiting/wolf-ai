# webRTC 学习
>       客户端交互流程：
>           client : publish
>           (worker : init)//信令目前无效
>           client : offer
>           worker : answer
>           client : candidate
>           worker : ready
>           应该是这个流程吧，client不发answer的
>
>
>       clientA
>           1、从roomserver获取config master信息
>           2、创建peerconnectionObject
>           3、创建音频的audiotrack
>           4、创建视频的videotrack
>           5、创建offer
>           6、setLocalDescription
>           7、从ICE Server（turn服务器）获取ICECondidate
>
>
>       1、从roomserver获取config master信息
>       2、create PeerConnecting
>       3、add streams
>       4、create offer
>       5、send SDP offer到signal server，signalserver发送到clientothers
>           然后clientothers发送一个relay answer
>       6、从stun server请求获取 my ipaddress
>           从stun server接收到iceCandidate
>       7、发送candidate到signalserver，signalserver发送到clientothers，clientothers然后addiceCandidate
>            clientothers从stunserver获取ipaddress，然后发送到signalserver，signalserver发送到clientA
>        8、双发建立p2p连接
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
