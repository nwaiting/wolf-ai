## cpp-笔记 - ThreadSanitizer使用
- **概述：**
>       利用Thread Sanitizer工具检查数据竞争的问题
>       ThreadSanitizer又叫TSan，是一个检查线程Data Race的C/C++工具。它集成在新版的gcc和clang中，通过编译时加-fsanitize=thread，可以在运行时检测出Data Race的问题
>
>       Data Race：
>           Data Race是指多个线程在没有正确加锁的情况下，同时访问同一块数据，并且至少有一个线程是写操作，对数据的读取和修改产生了竞争，从而导致各种不可预计的问题。
>           Data Race的问题非常难查，Data Race一旦发生，结果是不可预期的，也许直接就Crash了，也许导致执行流程错乱了，也许把内存破坏导致之后某个时刻突然Crash了。
>
>
>       注：
>           编译程序：g++ simple_race.cc -fsanitize=thread -fPIE -pie -g
>           1、除了加-fsanitize=thread外，一定要加-fPIE -pie
>           2、-g 是为了能显示文件名和行号
>           3、如果分生成obj(-c)和link两个步骤，每一步都加：thread -fPIE -pie -g，并且在link的时候加-ltsan
>           4、只支持64位，最好指定编译64位(-m64)
>           5、如果依赖其他静态库，其他静态库编译时必须指定-fPIC（如果不是请重编）
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
