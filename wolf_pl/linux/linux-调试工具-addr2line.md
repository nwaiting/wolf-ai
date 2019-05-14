## linux - add2line
- **概述：**
>       如何在程序没有core文件时，定位core的位置？
>           有时配置不给力，Linux直接毁尸灭迹，没有了Core文件；又有时，刚好磁盘空间不足，Core文件写不下了。
>           没有Core文件的时候，如何知道程序在什么地方出错了呢？addr2line就在这时派上用场。
>
>       例子：
>           1、gcc -o test1 -g test1.c
>           2、编译程序，test1.c是程序文件名。执行程序，结果程序异常中断，没有生产core文件。查看系统dmesg信息，发现系统日志的错误信息
>               [54106.016179] test1[8352] trap divide error ip:400506 sp:7fff2add87e0 error:0 in test1[400000+1000]
>           3、上面的dmsg信息里的ip字段后面的数字就是test1程序出错时所程序执行的位置。使用addr2line就可以将400506转换成出错程序的位置：
>               addr2line -e test1 400506
>               /home/hanfoo/code/test/addr2line/test1.c:5 定位到程序出现core的位置，这里的test1.c:5指的就是test1.c的第5行
>
>
>

- **addr2line的原理：**
>       在可执行程序中都包含有调试信息，其中很重要的一份数据就是程序源程序的行号和编译后的机器代码之间的对应关系Line Number Table。
>           DWARF格式的Line  Number Table是一种高度压缩的数据，存储的是表格前后两行的差值，在解析调试信息时，需要按照规则在内存里重建Line Number Table才能使用。
>       Line Number Table存储在可执行程序的.debug_line域，使用命令：
>           readelf -w test1
>       可以输出DWARF的调试信息，其中有两行
>           Special opcode 146: advance Address by 10 to 0x4004fe and Line by 1 to 5
>           Special opcode 160: advance Address by 11 to 0x400509 and Line by 1 to 6
>           这里说明机器二进制编码的0x4004fe位置开始，对应于源码中的第5行，0x400509开始就对应与源码的第6行了，所以400506这个地址对应的是源码第5行位置
>       addr2line通过分析调试信息中的Line Number Table自动就能把源码中的出错位置找出来，再也不怕Linux毁尸灭迹了
>       for example:
>           addr2line -e a.out 0x00007165
>
>
>
>
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
>
