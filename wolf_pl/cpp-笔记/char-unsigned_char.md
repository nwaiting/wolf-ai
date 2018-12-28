## cpp-笔记 - char和unsigned char 区别
- **概述：**
>       char、signed char和unsigned char的区别：
>           1、char
>               如何解析与编译器有关，
>               解析为signed char的编译器：VC、X86上的GCC
>               解析为unsigned char的编译器为：arm-linux-gcc
>           2、signed char
>           3、unsigned char
>
>       char*和unsigned char*的区别：
>           1、char*
>           2、unsigned char*
>           char*是有符号的，如果大于127即0X7F的数就是负数，使用%X格式化数据，系统自动进行了符号扩展，就会产生变化。
>           如果涉及到类型提升的上下文，注意使用char*和unsigned char*的区别
>
>       影响：
>           实际使用中，如普通的赋值、读写文件和网络字节流都没有区别，不管最高位是什么，读取的最终结果都一样，但是在屏幕上面的显示可能不一样。
>           在涉及到类型提升或者类型转换时，会有区别：！！！
>               当将char类型转为int、long等数据类型时，
>               1、对于char类型的变量，系统认为最高位为符号位，然后对最高位进行扩展，即符号位扩展。若最高位为1，则扩展到int类型时，高位都以1填充
>               2、对于unsigned char类型变量，系统直接进行无符号扩展，即0扩展，扩展的高位都是以0填充
>           所以，如果char和unsigned char最高位都是0，则结果是一样的，若char最高位为1，则结果会不一样。！！！！！！！
>           对于unsigned char来说，不管最高位是0还是1，都不会做扩展。！！！！！！
>
>
>       总结：
>           有符号的char做类型转换时候注意转换规则。！！！！！！！！！！
>
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
>
>
>
>
