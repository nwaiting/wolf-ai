## media-audio webrtc源码分析
- **概述：**
>
>
>
>

- **音频处理功能：**
>       1、回声消除（AEC/AECM Acoustic Echo Canceller for Mobile 声学回声消除）
>           class EchoCancellation
>           AEC(Acoustic Echo Canceller)和AECM(Acoustic Echo Canceller Mobile)，AEC是在电脑端使用的回声消除器，而AECM是在移动端使用。
>           回声消除的基本原理是使用一个自适应滤波器对未知的回声信道:ω进行参数辨识，根据扬声器信号与产生的多路回声的相关性为基础，建立远端信号模型，
>               模拟回声路径，通过自适应算法调整，使其冲击响应和真实回声路径相逼近。然后将麦克风接收到的信号减去估计值，即可实现回声消除功能。
>       2、回声抑制（AES）
>           EchoControlMobile
>
>       3、增益控制（AGC Auto Gain Control 自动增益控制）
>           GainControl
>
>       4、高通滤波
>           HighPassFilter
>
>       5、信号能量值
>           LevelEstimator
>
>       6、噪声抑制（NS/SE Noise Suppression 噪声抑制）
>           NoiseSuppression
>           算法的核心思想是采用维纳滤波器抑制估计出来的噪声。
>
>       7、激活检测（VAD Voice Activity Detection 静音检测）
>           VoiceDetection
>           gmm
>

- **混音和混屏：**
>       混音：
>           将多个音频流混成一路音频，实现有分为终端实现和服务器实现
>           终端实现：
>               终端接收到多路(一般是多个用户)的音频流之后，在终端本地将多路音频流混成一路音频送给扬声器播放
>               终端混音方式下服务器只起到数据转发的作用，负担比较轻，这种实现的方式的优点是便于扩充，增加用户数量不会对服务器造成太大的负担。
>               缺点是每个终端都需要混音工作，故每个终端都需要有足够的配置，由于接收的是多路音频，所以需要比较大的带宽
>           服务端实现：
>               混音位于服务器，n路音频流首先按各自的编码标准进行解码后的音频流混合成一路，混合后的音频重新编码后发送到待接收的终端
>               服务器混音的优点是终端负担较轻，终端带宽要求也不高，但服务器端需要完成大部分混音工作完成，要求性能足够好。缺点是系统的可扩充性不好，随着终端用户数量的增加，服务器负担会加重
>
>       混屏：
>           将多路视频流合成成一路视频流发给待接受的终端，如将四路QCIF大小的H.264编码码流合并成一路CIF大小的码流技术,输出的码流与普通的H.264的CIF格式的码流完全一样。
>               这个合并的过程放在了MCU上,对于终端来说,与接收单一画面的视频信号相比 ,在带宽占用和信号处理方面不会增加任何额外的负担,且减轻终端的复杂度并提高稳定性
>

- **待续：**
>       参考：https://blog.csdn.net/u010221213/article/details/51644632    WebRTC源码分析二：音频模块结构
>           https://blog.csdn.net/u010221213/article/details/51644715   WebRTC源码分析一：音频处理流程
>           https://www.cnblogs.com/wangbin/p/4462895.html  WebRTC源码分析：音频模块结构分析
>           https://www.cnblogs.com/wangbin/p/4462903.html  webrtc--AudioProcessing的使用
>           https://www.jianshu.com/p/5a8a91cd84ef?hmsr=joyk.com&utm_medium=referral&utm_source=joyk.com    WebRTC音频引擎实现分析（代码说明详解）
>           http://www.ideawu.net/blog/archives/726.html    WebRTC源码架构浅析
>           http://www.aiuxian.com/article/p-1212986.html   WebRtc VoiceEngine代码解析
>           https://www.twblogs.net/a/5b8bf2012b717718832f4625/zh-cn    WebRtc语音整体框架（代码详解）
>           http://zhangpengyf.github.io/2017/02/17/webrtc%E5%B0%81%E8%A3%85sdk-%E4%B8%89-VoiceEngine%E7%9A%84%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95.html     webrtc封装sdk（三）VoiceEngine的使用方法
>           https://www.cnblogs.com/wangbin/p/4462895.html      WebRTC源码分析：音频模块结构分析
>           https://www.cnblogs.com/wangbin/p/4462899.html      WebRtc VoiceEngine代码解析
>           https://www.cnblogs.com/lingyunhu/p/rtc25.html      WebRTC 音视频开发总结（二五）-- webrtc优秀资源汇总
>           https://www.cnblogs.com/lingyunhu   WebRTC 音视频开发总结
>
>
>
>
