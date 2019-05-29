# g++ and gcc ：
- **概述：**
>       1、对于.c文件，gcc当做c程序，g++当做c++程序
>       2、对于.cpp文件，gcc和g++都会当做c++程序
>       3、编译阶段，g++会调用gcc
>       4、链接阶段，通常会用g++来完成，因为gcc不能自动连接c++的库
>
>
>
>
>
>

- **g++和gcc的区别：**
>       使用场景：
>           g++编译器，直接编译cpp文件
>           gcc编译器，编译c文件，但是如果c文件里面有cpp内容，则编译报错，需要链接相关的库
>       GCC大写的GCC表示：GNU Compiler Collection（GNU编译器集合），可以编译C、C++、Java、Objective-C、Ada等语言
>       gcc是GCC中的GNU C Compiler（C编译器）
>       g++是GCC中的GNU C++ Compiler（C++编译器）
>       g++、gcc只是一种驱动器，根据参数中要编译的文件类型，调用对应的GNU编译器而已。
>       gcc编译一个c文件步骤：
>           1、Call a preprocessor,like cpp
>           2、Call an actual compiler，like cc or cc1
>           3、Call an assembler,like as
>           4、Call a linker,like ld
>       由于编译器是可以更换的，所以gcc不仅仅可以编译c文件
>       更准确的说：gcc调用了C compiler，而g++调用了c++ compiler
>
>       g++和gcc编译时候的区别：
>           1、对于.c和.cpp文件，gcc分别当做c和cpp文件编译(c和cpp的语法强度是不一样的)
>           2、对于.c和.cpp文件，g++则统一当做cpp文件编译
>           3、在使用g++编译文件时，g++会自动连接标准库STL，而gcc则不会自动连接STL
>           4、gcc在编译C文件时，可使用的预定义宏是比较少的
>           5、gcc在编译cpp文件时或者g++在编译c文件和cpp文件时（这时候gcc和g++调用的都是cpp文件的编译器），会加入一些额外的宏，如：
>               #define __GXX_WEAK__ 1
>               #define __cplusplus 1
>               #define __DEPRECATED 1
>               #define __GNUG__ 4
>               #define __private_extern__ extern
>           6、在使用gcc编译c++文件时，为了能够使用STL，需要加参数-lstdc++,但这并不代表gcc -lstdc++和g++等价，它们的区别不仅仅是这个主要参数
>               -g - turn on debugging
>               -Wall - turn on most warnings
>               -O or -O2 - turn on optimizations
>               -o - name of the output file
>               -c - output an object file(.o)
>               -l - specify an includedirectory
>               -L - specify a libdirectory
>               -l - link with librarylib.a
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
>           http://www.cnblogs.com/samewang/p/4774180.html   Linux公社的一篇文章
>           https://www.cnblogs.com/qoakzmxncb/archive/2013/04/18/3029105.html      GCC，LLVM，Clang编译器对比
>           https://www.kancloud.cn/wizardforcel/gcc-tips-100/146931    100个gcc的小技巧
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
