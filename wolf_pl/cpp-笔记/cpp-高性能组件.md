## cpp-笔记 - 高性能组件
- **概述：**
>
>
>
>       tbb:
>           （Threading Building Blocks）
>           c++的两个知名的并行库，一个是intel开发的TBB，并行库充分利用多核的优势，通过并行运算提高程序效率
>               tbb由于设计上的原因不能做到任务的连续执行以及任务的组合，但是tbb有跨平台的优势
>           主要功能：
>               并行算法
>               任务调度
>               并行容器
>               同步原语
>               内存分配器
>
>       PPL：
>           （Parallel Patterns Library）
>           c++的两个知名的并行库，一个是微软开发的PPL，并行库充分利用多核的优势，通过并行运算提高程序效率
>           功能和TBB是差不多的，但是PPL只能在windows上使用。ppl和tbb两个并行运算库功能相似，如果需要跨平台则选择tbb,  否则选择ppl
>
>
>       dmlc：
>           主要是Distributed (Deep) Machine Learning Community的一个基础模块
>           DMLC 项目的发起者陈天奇表示，项目最初的想法是减少分布式机器学习开发的成本
>           https://github.com/dmlc/dmlc-core/tree/master/include/dmlc
>           dmlc-core：
>               核心模块
>               https://github.com/dmlc/dmlc-core/tree/master/include/dmlc
>               有一个无所队列组件参考：http://moodycamel.com/blog/2014/a-fast-general-purpose-lock-free-queue-for-c++
>
>
>       队列：
>           A fast single-producer, single-consumer lock-free queue for C++：
>               https://github.com/cameron314/readerwriterqueue
>           A fast multi-producer, multi-consumer lock-free concurrent queue for C++11
>               https://github.com/cameron314/concurrentqueue
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
