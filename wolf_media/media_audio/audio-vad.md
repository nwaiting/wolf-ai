## media-audio VAD(Voice Activity Detection)
- **概述：**
>       VAD（Voice Activity Detection）算法的作用是检测是否是人的语音，它的使用范围极广，降噪、语音识别等领域都需要有vad检测。
>
>       最初使用统计模型到VAD：
>           假设语音和噪声的离散傅立叶变换（Discrete Fourier Transform，DFT）系数是渐进独立的高斯随机变量
>           由于高斯混合模型（Gaussian Mixture Model，GMM）在噪声环境中也能取得较好的性能，经常作为统计模型用于VAD
>           基于统计模型的VAD算法可以通过设计与数据记录相同条件下的模型，实现对噪声的鲁棒性
>
>

- **webRTC的vad详解：**
>       该VAD的算法主要用了2个models来对语音建模，并且分成噪声类和语音类。
>       通过比较似然比的方法来确定是否是语音。其中有三个模式可以选择，每个模式算法是一致的，只是相关阈值不同。
>       GMM的更新方法是梯度法，并没有使用常见的EM算法。这是因为其数据量不够大，难以准确估计种类，另外也节省部分运算量。
>       算法过程：
>           1、将信号通过分频降到8kHz。在这个频带计算噪声和语音的特征做VAD判决
>           2、WebRtcVad_CalculateFeatures函数计算特征，其特征包括6个频带的log能量，分别是80-250、250-500、500-1kHZ、1kHz-2kHz、2kHz-3kHz、3kHz-4kHz。
>               使用分频方法计算这些特征。这六个特征放在向量feature_vector中，使用2维度的GMM模型来建模
>           3、WebRtcVad_GaussianProbability函数输入信号、均值、方差，计算高斯分别概率密度：P\left( x \right) = \frac{1}{\sigma }{e^{\frac{{ - {{\left( {x - \bar x} \right)}^2}}}{{2{\sigma ^2}}}}}。注意这里少了一个 \frac{1}{{\sqrt {2\pi } }}的系数，因为后面用到概率的时候都是相对量，能够抵消。例如似然比和后验概率
>           4、对于每一个特征 求对数似然比，一共6个
>           5、计算加权对数似然比，是似然比的加权系数
>           6、如果6个特征中有一个满足似然比超过了阈值就认为有语音
>               或者加权似然比超过了阈值
>           7、WebRtcVad_FindMinimum函数对每个特征feature，求出了100个帧里头的16个最小值。这些最小值都有一个年龄，最大不超过100，也就是说100帧之后失效。这个最小值用来更新噪声的均值
>           8、计算噪声加权均值
>           9、模型参数更新，包括语音和噪声的两个高斯分布均值和方差更新。
>               注意噪声均值的更新使用了长期的最小值，也即公式的第三部分。该部分与VAD的标志位是无关的。跟新完后结束VAD计算。最后需要对均值和方差做相应的限制
>
>
>
>

- **子带能量：**
>       计算每个滤波组输出的对数能量，即为子带能量
>
>

- **检测原理：**
>       webrtc的vad检测原理是根据人声的频谱范围，把输入的频谱分成六个子带（80Hz~250Hz，250Hz~500Hz,500Hz~1K,1K~2K,2K~3K,3K~4K）。
>           使用高通滤波器滤除80hz以下的内容
>           分别计算这六个子带的能量。然后使用高斯模型的概率密度函数做运算，得出一个对数似然比函数。对数似然比分为全局和局部，全局是六个子带之加权之和，
>           而局部是指每一个子带则是局部，所以语音判决会先判断子带，子带判断没有时会判断全局，只要有一方过了，就算有语音
>

- **webRTC的vad检测：**
>       webrtc的vad检测代码比较简洁，核心代码只在三个文件中，
>           1、webrtc_vad.c 该文件是用户调用的API函数，使用vad一般只需要调用该里面的函数即可
>               WebRtcVad_Create  WebRtcVad_Init 申请内存和初始化一些参数
>               WebRtcVad_set_mode 设置vad要处理的采样率，一般是8000或16000
>               WebRtcVad_Process 核心函数，完成检测是否有人声的核心
>               使用方法：
>                   　　WebRtcVad_Create（）；
>                   　　WebRtcVad_Init（）；
>                   　　WebRtcVad_set_mode（）；
>                   　　WebRtcVad_Process（）；
>           2、vad_core.c 该文件是webrtc_vad.c 文件中函数的实现代码，也是vad最深层的核心代码
>
>       注意：
>           共有三种帧长可以用到，分别是80/10ms，160/20ms，240/30ms。其它采样率的48k，32k，24k，16k会重采样到8k来计算VAD。
>           之所以选择上述三种帧长度，是因为语音信号是短时平稳信号，其在10ms~30ms之间可看成平稳信号，
>               高斯马尔科夫等比较的信号处理方法基于的前提是信号是平稳的，在10ms~30ms，平稳信号处理方法是可以使用的。
>           vad的代码中可以看出，实际上，系统只处理默认10ms,20ms,30ms长度的数据，其它长度的数据没有支持，
>               笔者修改过可以支持其它在10ms-30ms之间长度的帧长度发现也是可以的。
>           vad检测共四种模式，用数字0~3来区分，激进程度与数值大小正相关：
>               0: Normal
>               1：low Bitrate
>               2：Aggressive
>               3：Very Aggressive
>           可以根据实际的使用,在初始化的时候可以配置
>
>

- **面临挑战：**
>       VAD算法的作用是检测语音，在远场语音交互场景中，VAD面临着两个难题：
>           1、可以成功检测到最低能量的语音(灵敏度)
>           2、在多噪环境下成功检测（漏检率和虚检率）
>               漏检反应的是原本是语音但是没有检测出来
>                   相对而言漏检是不可接受的
>               虚检率反应的是原本不是语音信号而被检测成语音信号的概率
>                   虚检可以通过后端的ASR和NLP算法进一步过滤，但是虚检会带来系统资源利用率上升，随之系统的功耗和发热会进一步增加，而这会上升为可移动和随声携带设备的一个难题
>

- **滤波器分析：**
>       使用高通滤波器滤除80hz以下的内容
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
>       参考：https://blog.csdn.net/ssdzdk/article/details/42876011    WebRtc 的VAD算法解析
>           https://blog.csdn.net/shichaog/article/details/52399354     WebRTC之VAD算法
>           https://shichaog1.gitbooks.io/hand-book-of-speech-enhancement-and-recognition/content/chapter7.html     第七章 语音检测(VAD)原理和实例
>           https://zhuanlan.zhihu.com/p/60371062   音频知识（二）—— MFCC详解
>           https://blog.csdn.net/book_bbyuan/article/details/80725945  WebRTC VAD 中所用滤波器之分析（详解）
>           https://blog.csdn.net/book_bbyuan/article/details/78944630  WebRTC VAD算法初探（详解-代码级详解）
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
