## linux - IO
- **概述：**
>       文件IO
>       高级IO
>       标准库IO
>       系统IO
>
>
>
>
>

- **系统IO**
>       Linux下的基本IO系统调用，这些调用不仅仅是文件IO的基础，也是linux下所有通信方式的基础
>
>![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/unix_io.jpg)
>       上图展示了几种IO的关系模式，以及应用程序中，应该使用哪些场景。
>       标准IO：！！！
>           磁盘和终端设备IO的首选
>       网络套接字：！！！
>           尽量使用健壮的RIO或者系统IO
>


- **文件IO**
>       文件IO所有函数都是针对文件描述符的
>       文件描述符不仅仅用于普通文件的访问，也用于设备文件、管道、目录、快速用户空间锁、FIFOS、套接字。！！！
>       遵循一切皆文件的理念，任何你能读写的东西都可以用文件描述符来访问。
>
>       unix文件系统中大多数IO需要用到的五个常用函数：
>           open
>           read
>           write
>           lseek
>           close
>           这些都是不带缓冲的IO，即每次read或write都调用内核中的一个系统调用。
>           这些不带缓冲的IO函数不是ISO C从组成部分，他们是POSIX.1和Signgle UNIX Specification的组成部分。
>           dup
>           fcntl
>           sync
>           fsync
>           ioctl
>
>       open()函数：
>           int open(const char *name,int flags);
>           int open(const char *name,int flags,mode_t mode);
>           fd=open(file,O_WRONLY|O_CREATE|O_TRUNC,0644);
>
>       Unix进程文件共享：
>           unix系统支持不同进程间共享打开的文件。
>           内核用于所有IO的数据结构：
>               内核使用了三种数据结构表示打开的文件，如下图：
> ![avatar](https://github.com/nwaiting/wolf-ai/tree/master/wolf_others/pic/unix_file_share.jpg)
>               上图显示了一个进程的三张表之间的关系。该进程有两个不同的打开的文件：一个文件打开为标准输入，另一个打开为标准输出
>                   这张安排对于不同进程之间共享文件的方式非常重要
>
>               1、每个进程在进程表中都有一个记录项，包括一张打开的文件描述表，每个描述符占一项
>                   文件描述符
>                   指向一个文件表项的指针
>               2、内核为所有打开文件维护一张文件表，每个表项包含
>                   文件状态
>                   当前文件偏移
>                   指向改文件v节点表项指针
>               3、v节点结构
>                   文件类型
>                   对此文件进程各种操作的函数的指针
>               （v节点结构：包含文件类型、进程操作此文件的函数指针、对于大多数文件还包含文件i节点）
>               （i节点：包含了文件所有者、文件长度、文件所在设备、指向文件实际数据块在磁盘上所在位置的指针等）
>
> ![avatar](https://github.com/nwaiting/wolf-ai/tree/master/wolf_others/pic/unix_file_share2.jpg)
>       如上图，如果两个独立进程各自打开了同一个文件，假定第一个进程在文件描述符3上打开该文件，另一个进程在文件描述符4上打开该文件。
>           打开该文件的每个进程都得到一个文件表项，但对一个给定的文件只有一个v节点表项。每个进程都有自己的文件表项的一个理由：这种安排使每个进程都有他自己的对文件的当前偏移量。
>
>           1）在完成每个write后，在文件表项中的当前文件偏移量既增加缩写的字节数。如果这使文件偏移量超过了当前文件长度，则在i节点表项中的当前文件长度被设置为当前文件偏移量（也就是该文件加长了）
>           2）如果用O_APPEND标志打开了一个文件，则相应标志也被设置到文件表项的文件状态标志中。每次对这种具有添写标志的文件执行写操作时，
>               在文件表项中的当前文件偏移量首先被设置为i节点表项中的文件长度。这就使得每次写的数据添加到文件的当前末尾。
>           3）若一个文件用lseek定位到文件当前尾端，则文件表项中的当前文件偏移量被设置为i节点表项中的当前文件长度。
>           4）lseek函数只修改文件表项中的当前文件偏移量，没有进行任何I/O操作。
>
>       父子进程fork共享的文件：如下图
>![avatar](https://github.com/nwaiting/wolf-ai/tree/master/wolf_others/pic/unix_file_share_fork.jpg)
>
>
>

- **高级IO**
>       高级IO含有以下类型：
>           非阻塞IO
>           记录锁
>           系统V流机制
>           IO多路回转(select、poll函数)
>           readv和writev函数
>           存储隐射IO(mmap)
>
>       mmap()函数：
>           void * mmap(void *addr,size_t len,int port,int flags,int fd,off_t offset);
>               使用read、write系统调用需要从用户缓冲区进行数据读写，而使用映射文件进行操作可以避免多余的数据拷贝。
>           注意：
>               除了潜在的页错误，读写映射文件不会带来系统调用和上下文切换的开销，就像直接操作内存一样简单。
>               当多个进程映射同一个对象到内存中，数据在进程间共享，只读和写共享的映射在全体中都是共享的;
>                   私有可写的尚未进行写时拷贝的页是共享的。
>               在映射对象中搜索只需要一般的指针操作，而不必使用lseek()
>
>           缺点：
>               隐射区域的大小通常也是页大小的整数倍
>               映射区域必须在进程地址空间内
>               创建和维护映射以及相关的内核数据结构有一定的开销
>
>
>

- **标准库IO**
>       在基础系统IO调用之上经常需要在用户空间做缓冲，即C的标准IO库。！！！
>
>       在文件IO中所有函数都是针对文件描述符的。对于标准IO库，操作都是围绕流进行的。
>           当用标准IO库打开或关闭一个文件时，我们已使一个流与一个文件相互关联。
>
>       当打开一个流时，标准IO函数fopen返回一个指向FILE对象的指针。
>           FILE对象是一个结构，包含了标准IO为管理改流所需要的所有信息，包括：实际IO的文件描述符、指向该流缓冲区的指针、缓冲区的长度、
>           当前缓冲区的字符数以及出错标志等等。
>
>       标准IO库是提供缓冲区的，标准IO提供缓冲区的目的是尽可能减少read和write调用次数。标准IO库处理很多细节，比如缓冲区分配、优化长度执行等。
>
>       标准IO提供了三种类型缓冲：
>           1、全缓冲
>               这种情况下，在填满标准IO缓冲后才进行实际IO操作。
>               对于磁盘上的文件通常是由标准IO库实施全缓冲的。
>               在一个流上执行第一次IO操作后，标准IO函数通常会调用malloc获得所需的缓冲区
>           2、行缓冲
>               这种情况下，在输入和输出中遇到换行符时，标准IO库执行IO操作。
>               当流涉及一个终端时，如标准输入、输出，通常使用行缓冲
>               注意：
>                   a、标准IO收集每一行的缓冲区是固定的，所以只要填满了缓冲区，那么即使还没有写一个换行符，也进行IO操作
>                   b、任何时候只要通过标准IO从外部得到数据，那么就会造成冲洗所有行缓冲输出流
>           3、不带缓冲
>               标准IO库不对字符进行缓冲存储。
>               如果用标准IO函数fputs写15个字符到不带缓冲的流中，则该函数很可能直接写到关联的文件上。
>
>           这是缓冲类型：
>               void setbuf(FILE *restrict fp,char *restrict buf);
>               int  setvbuf(FILE *restrict fp,char *restrict buf,int mode,size_t size); // 若成功则返回0，出错则返回非0值
>               mode参数设置：
>                   _IOFBF 全缓冲
>                   _IOLBF 行缓冲
>                   _IONBF 不带缓冲
>
>       强制冲洗一个流：
>           int fflush(FILE *fp);
>           该函数使该流所有未写的数据都被传送至内核。
>
>       打开流的函数：
>           FILE *fopen(const char *restrict pathname,const char *restrict type);
>
>           //在一个指定的流上打开一个指定的文件，如该流已经打开，则关闭该流
>           FILE *freopen(const char *restrict pathname,const char *restrict type,FILE *restrict fp);
>
>           //获取一个现有的文件描述符，并使一个标准的IO流与该描述符相结合
>           FILE *fdopen(int filedes,const char *type);
>
>       对于二进制IO，可以使用下面的函数：
>           size_t fread(void *restrict ptr,size_t size,size_t nobj,FILE *restrict fp);
>           size_t fwrite(const void *restrict ptr,size_t size,size_t nobj,FILE *restrict fp);
>           这两个函数可以读写对象、结构数组，使用二进制IO的基本问题是，它只能用于读在同一系统上已写的数据。
>           因为一个机构中，同一成员的偏移量可能因编译器和系统而不同。用来存储多字节整数和浮点数值的二进制格式在不同机器体系结构间也可能不同。
>
>       每次一行的IO，一次读写一行，可以使用下面的函数：
>           fgets()
>           fputs()
>
>
>

- **linux的文件：**
>       文件有文件名和数据，在linux上被分成两个部分：用户数据(user data)和元数据(metadata)
>       用户数据：
>           文件数据块，数据块是记录文件真实数据的地方
>       元数据：
>           元数据是文件的附加属性，如文件大小、创建时间、所有者信息等
>       inode号：
>           linux中，元数据的inode号（即索引节点号）才是文件的唯一标识，而不是文件名。系统或程序通过inode号找到文件数据块。
>
>       linux下软、硬连接区别：
>           硬链接：
>               一个inode号对应多个文件名，硬链接就是同一个文件使用了多个别名，但是拥有共同的inode，硬链接的文件有连接计数器(link count)
>           软连接：
>               软连接文件有自己的inode号以及用户数据块，用户数据块中存放的内容是另一文件的路径名的指向。
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
