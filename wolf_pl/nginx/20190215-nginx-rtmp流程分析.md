## nginx - nginx rtmp 流程分析
- **概述：**
>       本文主要内容
>           rtmp client和server交互流程
>           回源
>
>
>
>
>

- **rtmp client和server交互流程：**
>
>       rtmp client和server交互需要经过4个步骤：
>           1、握手
>           2、建立链接
>               建立client和server的网络连接，建立链接用于建立client和server的网络流
>           3、建立流
>           4、播放/发送
>               用户传输音视频数据
>
>

- **回源：**
>
>       nginx-rtmp模块中的relay模块，当client向边缘服务器请求某一路rtmp流且该流不存在时，会向配置的源流服务器请求该rtmp流，请求成功后该边缘服务器分发给client，即中继开始。
>           当最后一个请求rtmp的client关闭流时，该边缘服务器自动断开与源服务器流的请求，即中继结束。
>           该relay中继联动源是基于rtmp流请求的，针对hls、hlf流的请求源存在缺失。
>       中继功能相关模块，目前有三个：
>           1、notify
>           2、auto-push
>           3、relay
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
>       参考：https://blog.evanxia.com/2017/02/1264    Nginx-rtmp-module模块源码学习
>           https://blog.csdn.net/ai2000ai/article/details/84587080     Nginx-rtmp直播之业务流程分析--比较详细
>           https://www.cnblogs.com/jimodetiantang/p/8994061.html   Nginx-rtmp直播之业务流程分析
>           https://zhuanlan.zhihu.com/p/27867576   nginx-rtmp-module学习
>           https://blog.csdn.net/lory17/article/details/61916351#%E6%8E%A8%E6%B5%81%E5%B7%A5%E4%BD%9C  TMP推流及协议学习
>           https://blog.csdn.net/weixin_39371129/article/details/74576960  RTMP协议分析及推流过程
>           https://www.jianshu.com/p/00aceabce944  直播推流实现RTMP协议的一些注意事项
>           https://blog.csdn.net/wu5215080/article/details/72519290    nginx-rtmp源码概述
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
