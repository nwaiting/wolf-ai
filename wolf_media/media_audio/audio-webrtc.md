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

- **语音引擎工作流程：**
>       1、发起端进行声音采集
>       2、采集到的声音信号进行回声消除，噪音抑制，自动增益控制处理
>       3、语音压缩编码
>       4、通过Internet网路传输到接收端
>       5、到达接收端，先进入NetEQ模块进行抖动消除，丢包隐藏解码等操作
>       6、将处理过后的音频数据送入声卡设备进行播放
>

- **语音引擎线程模型：**
>       语音引擎在运行时会启动两个线程：
>           一个线程用于接收来自于网络的数据包，并将其插入到抖动缓冲区中
>           一个线程每隔10ms从NetEQ中提取10ms语音数据进行播放
>
>       webRTC将音频会话抽象为一个通道Channel，譬如A与B进行音频通话，则A需要建立一个Channel与B进行音频数据传输，每个Channel包含编解码和RTP/RTCP发送功能
>       一个Channel而言，应用程序中将包含三个活动线程，录音线程，音频接收线程和播放线程
>       录音线程：
>           负责麦克风音频的采集
>           采集到音频后，缓存到一定长度，进行音频处理，主要包括EC，AGC和NS等。然后送到Channel，经过音频Codec模块编码，封装成RTP包，通过Socket发送出去
>       音频接收线程：
>           负责接收远端发送过来的音频包，解封RTP包，解码音频数据，送入NetEQ模块缓存
>       播放线程：
>           播放线程去OutMixer中获取要播放的音频数据，首先依次获取参与会话的Channel中NetEQ存储的音频帧，可以对其做AGC和NS处理；
>           然后混合多个Channel的音频信号，得到混合音频，传递给AudioProcessing模块进行远端分析。最后播放出来
> 
>
>

- **webRTC相关：**
>       2010年5月，Google以6820万美元收购VoIP软件开发商Global IP Solutions的GIPS引擎，并改为名为“WebRTC”
>       WebRTC使用GIPS引擎，实现了基于网页的视频会议
>       webRTC的语音引擎架构，如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_webrtc_audio_framewok.jpg)
>
>
>

- **webRTC的音频引擎相关组件：**
>       VoiceEngine是WebRTC机具价值的技术之一，在VoIP上，技术业界领先，
>       iSAC：Internet Speech Audio Codec
>           针对VoIP和音频流的宽带和超宽带音频编解码器，是WebRTC音频引擎的默认的编解码器
>           采样频率：16khz，24khz，32khz；（默认为16khz）
>           自适应速率为10kbit/s ~ 52kbit/
>           自适应包大小：30~60ms
>           算法延时：frame + 3ms
>       iLBC：Internet Low Bitrate Codec
>           VoIP音频流的窄带语音编解码器
>           采样频率：8khz
>           20ms帧比特率为15.2kbps
>           30ms帧比特率为13.33kbps
>       NetEQ for Voice：
>           针对音频软件实现的语音信号处理元件
>           NetEQ算法：自适应抖动控制算法以及语音包丢失隐藏算法。使其能够快速且高解析度地适应不断变化的网络环境，确保音质优美且缓冲延迟最小。
>           是GIPS公司独步天下的技术，能够有效的处理由于网络抖动和语音包丢失时候对语音质量产生的影响。
>           NetEQ 也是WebRTC中一个极具价值的技术，对于提高VoIP质量有明显效果，加以AEC/NR/AGC等模块集成使用，效果更好
>       Acoustic Echo Canceler (AEC)：
>           回声消除器是一个基于软件的信号处理元件，能实时的去除mic采集到的回声
>       Noise Reduction (NR)：
>           噪声抑制也是一个基于软件的信号处理元件，用于消除与相关VoIP的某些类型的背景噪声（嘶嘶声，风扇噪音等等… …）
>

- **NetEQ模块：**
>       NetEQ模块分为下面四部分：
>           1、自适应缓冲器(Adaptive Packet Buffer)
>           2、语音解码器(SpeechDecoder)
>           3、抖动控制和丢包隐藏(Jitter Control and Error Concealment)
>           4、播放(PlayOut)
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

- **webRTC的语音引擎：**
>       如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_webrtc_audio_engine.png)
>
>

- **webRTC的音频函数调用关系：**
>       如下图，
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/media_pic/media_audio_webrtc_audio.jpg)
>
>

- **回声消除：**
>       回声消除的效果和采用的算法有关，一般有LMS、NLMS、RLS、APA等
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
