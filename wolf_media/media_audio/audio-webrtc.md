## media-audio webrtc
- **概述：**
>       webRTC的音频模块主要功能：
>           如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_webrtc_flow.jpg)
>           音频采集模块：
>               负责音频数据的采集
>           控制模块：
>               通过无锁队列对采集到的数据进行管理(数据下发、继续采集)
>           预解复用：
>               音频数据的处理语音前后处理算法，如回声消除、噪声抑制、增益控制、静音检测、舒适噪声等
>           解复用：
>               数据解复用
>           编码发送：
>               NetEQ网络抗抖技术等
>
>

- **webRTC的audio_processing模块介绍：**
>       audio_processing模块为语音处理的精华，包含音频的回音处理、降噪处理、自动增益处理等音频的核心处理业务算法
>       1、aec和aecm，也就是回音消除，其中aecm主要针对移动设备
>       2、agc，是音频自动增益
>       3、ns，就是降噪
>       4、vad，静音检测
>           GMM
>       5、signal_processing，信号处理
>           fft变换算法、bit反转算法、反射系数更正、能量检测等相关的音频信号相关的算法
>       6、其他
>

- **静音检测：**
>       到底在什么样的环境下，要增大音量，还是降低，在通讯行业一般的做法就是采用静音检测，一旦检测为静音或者噪音，则不做处理，反之通过一定的策略进行处理。
>       这里涉及到两个算法：
>           1、静音检测
>               在webRTC中，是计算GMM(高斯混合模型)进行特征提取的
>               音频特征提取有三个主要方法：
>                   (1)、GMM
>                   (2)、Spectrogram(声谱图)
>                   (3)、MFCC即Mel-Frequency Cepstrum(Mel频率倒谱)
>           2、音频增益
>               类似于数据归一化拉伸的做法
>
>
>
>

- **webRTC的语音引擎：**
>       如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_webrtc_audio_engine.png)
>
>
>

- **webRTC的音频函数调用关系：**
>       如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_webrtc_audio.jpg)
>
>
>
>
>

- **回声消除：**
>       回声消除的效果和采用的算法有关，一般有LMS、NLMS、RLS、APA等
>
>
>
>
>
>
>
>

- **待续：**
>       参考：https://blog.csdn.net/whchang8/article/details/76695948  WebRTC 音频处理流程(一)
>           https://blog.csdn.net/whchang8/article/details/76862221     WebRTC 音频处理流程(二) 预解复用部分
>           http://www.cclk.cc/tags/blog/page/2/    webrtc学习4-噪声消除、自动增益等
>           https://www.cnblogs.com/talkaudiodev/p/7441433.html     音频处理之回声消除及调试经验
>           https://www.cnblogs.com/talkaudiodev/p/8996338.html#4199268     谈谈我开发过的几套语音通信解决方案
>           https://www.cnblogs.com/talkaudiodev/p/7400252.html     音频软件开发中的debug方法和工具
>           https://www.cnblogs.com/talkaudiodev/p/7502193.html     音频的编解码及其优化方法和经验
>           https://www.cnblogs.com/talkaudiodev/p/7594233.html     语音传输之RTP/RTCP/UDP及软件实现关键点
>           https://www.zhihu.com/question/21406954     即时语音（如：YY语音）中回声消除技术是如何实现的？
>           http://www.manongjc.com/article/72052.html      webrtc aecd算法解析一（原理分析）
>           https://blog.csdn.net/boywgw/article/details/48311987   【WebRTC】NetEQ概述
>           https://blog.csdn.net/qazwsxwtc/article/details/49155463    webrtc音频引擎之audio_processing介绍
>           https://blog.csdn.net/elesos/article/details/53444124   WebRTC APM音频处理流程概述
>           https://blog.csdn.net/temotemo/article/details/7530504  WebRTC音视频引擎研究(1)--整体架构分析
>           https://blog.51cto.com/billhoo/1213801?page=3&per-page=10   【单独编译使用WebRTC的音频处理模块 - android】
>           https://yuebinyun.github.io/2017/01/10/AEC-%E5%AD%A6%E4%B9%A0-2/    AEC 学习 (2)
>           https://www.cnblogs.com/cpuimage/p/8908551.html     音频自动增益 与 静音检测 算法 附完整C代码
>           https://blog.csdn.net/qazwsxwtc/article/category/1889879    webRTC音频系列博客
>           https://blog.csdn.net/ssdzdk/article/details/39577335   音频相关技术系列博客
>
>
>
