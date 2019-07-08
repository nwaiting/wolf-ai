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

- **待续：**
>       参考：https://www.cnblogs.com/lingdhox/p/4209659.html
>           https://blog.csdn.net/glw0223/article/details/90734581      ICE之STUN协议---Binding
>           https://www.cnblogs.com/limedia/p/stun.html     Stun协议的格式记录
>           https://michaelyou.github.io/2017/08/13/ssl-traffic-analysis/   SSL/TLS 会话流量分析
>           实现简易webrtc 网关：
>           https://www.jianshu.com/p/61e3c9e13456?utm_campaign=maleskine&amp;utm_content=note&amp;utm_medium=seo_notes&amp;utm_source=recommendation
>           https://www.meiwen.com.cn/subject/ruyckftx.html     通过janus认识libnice
>           https://segmentfault.com/a/1190000015075880     聊聊 WebRTC 网关服务器1：如何选择服务端端口方案？
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
