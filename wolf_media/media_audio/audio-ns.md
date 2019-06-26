## media-audio ns(Noise suppression)
- **概述：**
>
>
>

- **NS原理：**
>       算法的核心思想是采用谱减法计算噪声估计和运用维纳滤波器抑制估计出来的噪声。
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
