## media-audio ns(Noise suppression)
- **概述：**
>       算法的核心思想是采用维纳滤波器抑制估计出来的噪声。
>
>

- **噪声估计：**
>       噪声估计方法：
>           1、基于vad检测的噪声估计，如果检测没有语音，则认为是噪声
>           2、基于全局幅度谱最小原理，估计认为幅度谱最小的情况必然对应没有语音的时候
>           3、基于矩阵奇异值原理估计噪声
>
>       webRTC噪声估计：
>           webRTC没有采用上述的方法，而是对似然比（VAD检测时就用了该方法）函数进行改进，将多个语音/噪声分类特征合并到一个模型中形成一个多特征综合概率密度函数，
>               对输入的每帧频谱进行分析。其可以有效抑制风扇/办公设备等噪声
>
>
>
>

- **NS原理：**
>       算法的核心思想是采用谱减法计算噪声估计和运用维纳滤波器抑制估计出来的噪声。
>
>       谱减法是最常用的一种噪声抑制方法，它基于一个简单的原理:假设噪声为加性噪声，通过从带噪语音谱中减去对噪声谱的估计，就可以得到纯净的信号谱。
>           在不存在语音信号的期间，可以对噪声谱进行估计和更新。做出这一假设是基于噪声的平稳性，或者是一种慢变的过程，这样噪声的频谱在每次更新之间不会有大的改变。
>           增强信号通过计算估计信号谱的逆离散傅里叶变换得到，其相位仍然使用带噪信号的相位。在计算上这种算法比较简单，因为其只包含一次傅里叶变换和反变换。
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
>       参考：https://github.com/jagger2048/WebRtc_noise_suppression/blob/master/readme_cn.md
>           https://blog.csdn.net/shichaog/article/details/52514816     WebRTC之noise suppression算法
>           https://www.e-learn.cn/content/qita/826351      webrtc 单通道降噪算法（ANS）简析
>           https://blog.csdn.net/shichaog/article/details/52514816     WebRTC之noise suppression算法（代码详解）
>           https://blog.csdn.net/qq_28882043/article/details/80885240  Webrtc NS模块算法（代码详解）
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
