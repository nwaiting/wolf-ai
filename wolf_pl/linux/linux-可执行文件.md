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

- **readelf和objdump：**
>       objdump：
>           objdump是以一种可阅读的格式让你更多地了解二进制文件带有的信息的工具。objdump借助BFD，更加通用一些, 可以应付不同文件格式，它提供反汇编的功能。
>               objdump -h SimpleSection.o对Section部分进行解析，我们可以得到每个段的大小
>       readelf：
>           readelf则并不借助BFD，而是直接读取ELF格式文件的信息，得到的信息也略细致一些。
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
>       参考：
>       https://www.jianshu.com/p/863b279c941e  使用readelf和objdump解析目标文件
>       https://blog.csdn.net/edonlii/article/details/8779075   ELF格式文件符号表全解析及readelf命令使用方法
>       https://blog.csdn.net/linux_ever/article/details/78210089   readelf命令和ELF文件详解
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
