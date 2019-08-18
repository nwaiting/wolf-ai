## media-应用
- **概述：**
>       从flv中抽取h264数据：
>           ffmpeg -i input.flv -vcodec copy -an output.264
>
>       姜生 2018-04-04 15:48:21
>       我把这个文件里的 264 raw 数据提取出来了，并解码为 yuv，我看了一下好几个时段里包含多帧有相同的画面
>       姜生 2018-04-04 15:48:35
>       你拿一个 yuv 播放器看看
>       姜生 2018-04-04 16:13:24
>       你用yuv播放器啊
>       姜生 2018-04-04 16:14:22
>       画面联系多帧没有变化，就说明这个问题了啊
>       姜生 2018-04-04 16:16:21
>       让yuv播放器按照一定的帧率来播放，就可以发现明显的卡顿
>
>       FlvAnalyzer.exe
>       FlvParse.exe
>       H264BSAnalyzer.exe
>       SpecialFFLV.exe
>
>
>       分析在线视频：
>           ./ffprobe -i http://10.200.20.54:8088/webm/f8c68397b41e0279187b11eba64b7782 -show_entries frame=media_type,pkt_pts,pkt_size,width,height,pict_type -of xml > st_audiopts.xml
>           
>
>
>
>

- **待续：**
>       参考：
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
>
>
>
>
