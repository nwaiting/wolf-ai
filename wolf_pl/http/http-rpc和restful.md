### http - rpc和restful区别
- **概述**
>       rpc和restful区别：
>           1、对于RESTful而言，这个链接其实就是个对象，我可以增删改查，这些东西是HTTP自带的
>               更多的操作我们没法通过这几个方法来描述呢，就需要使用RPC了
>
>
>

- **RESTful：**
>       RESTful还是基于HTTP的RPC实现
>       RESTful是一种软件架构风格，设计风格而不是标准，只是提供了一组设计原则和约束条件，
>           主要用于客户端和服务器交互类的软件。基于这个风格设计的软件可以更简洁，更有层次，更易于实现缓存等机制
>           在 REST 样式的 Web 服务中，每个资源都有一个地址。资源本身都是方法调用的目标，方法列表对所有资源都是一样的。
>           这些方法都是标准方法，包括 HTTP GET、POST、PUT、DELETE，还可能包括 HEADER 和 OPTIONS
>           RESTful充分利用了HTTP的POST，PUT，DELETE等方法的含义
>

- **RPC(Remote Procedure Call Protocol)：**
>       RPC应该有各种各样的协议，基于或扩展与socket，HTTP等协议。
>       如果不是为了速度，应该不大会有人用socket，毕竟略有开发难度。比如淘宝的HSF也是基于HTTP的通信。
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
>       参考：https://developer.51cto.com/art/201906/597963.htm
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
