### linux-内核设计 - 文件系统
- **概述：**
>       线性目录是之前的一种经典的目录设计结构，但是不利于系统性能的提升。从ext3开始，加入了快速平衡树哈希目录项名称。
>           如果是ext4系统，目录使用哈希的B树(hashed btree，即htree)组织和查找目录项。为了兼容ext2，htree隐藏在目录文件中。
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

- **待续：**
>       参考：
>           https://www.cnblogs.com/alantu2018/p/8461272.html       Ext4文件系统架构分析(一)
>           https://www.cnblogs.com/alantu2018/p/8461587.html       Ext4文件系统架构分析(二)
>           https://www.cnblogs.com/alantu2018/p/8461598.html       Ext4文件系统架构分析(三)
>           https://www.cnblogs.com/alantu2018/p/8461749.html       Linux文件系统详解
>           https://blog.csdn.net/iamonlyme/column/info/ext4-filesystem     深入理解EXT4文件系统
>           http://oenhan.com/ext3-dir-hash-index   ext3目录索引机制分析
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
