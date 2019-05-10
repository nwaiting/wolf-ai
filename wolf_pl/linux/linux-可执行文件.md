## linux - linux可执行文件
- **概述：**
>       ldd 是我们经常贯用的检测 PE文件依赖的好工具.
>
>

- **not a dynamic executable：**
>       用ldd 看我的程序时却输出：
>           not a dynamic executable
>       原因很简单就是程序是x64的. 把这个x64的程序放到了x32的机器上,用ldd看就是这种效果
>
>       其实也可以使用另外一命令来看
>           readelf -d 你的程序 | grep NEEDED
>
>       x64 的 ELF(win下称pe文件) 文件地址空间 和 x32的不一样. x64的地址空间更大
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
