## nginx开发c++模块
- **概述：**
>       nginx的常用添加模块：
>           $CORE_MODULES   核心模块
>           $EVENT_MODULES  事件模块
>           $HTTP_MODULES   HTTP模块
>           $HTTP_FILTER_MODULES    HTTP过滤模块
>           $HTTP_HEADERS_FILTER_MODULES    HTTP头部过滤
>
>       nginx模块开发常用变量：
>           $NGX_ADDON_DEPS 指定模块指定依赖路径
>           ngx_addon_name  在configure执行时使用，一般为模块名称
>           NGX_ADDON_SRCS  指定模块的源代码
>           ngx_addon_dir   可以设置ngx_addon_dir变量，等价于configure执行时的-add-module=PATH
>
>       参考：https://blog.csdn.net/qq_18810607/article/details/79886076
>       nginx开发c++模块步骤：
>           1、首先创建newmodule文件夹
>           2、配置config文件
>               配置变量
>           3、在module文件夹下创建源文件
>           4、编译./configure --add-module=newmodule/
>           5、编写模块代码
>               大致流程：
>                   a、nginx读取到配置文件时，发现newmodule模块
>                   b、调用ngx_http_newmodule_commands指定的ngx_http_newmodule回调函数
>                   c、ngx_http_newmodule回调时设置处理HTTP的回调函数ngx_http_newmodule_handler
>               (1)首先引入需要的nginx核心模块
>               (2)定义一个nginx的HTTP模块ngx_module_t，编写代码实现逻辑处理
>                   static ngx_int_t ngx_http_newmodule_handler()
>                   static char* ngx_http_newmodule()
>                   static ngx_command_t ngx_http_newmodule_commands[] = {
>                               ngx_string("mymodule"),
>                               ...,
>                               //当某个配置快中出现newmodule时，就会回调此函数
>                               ngx_http_newmodule,
>                               ...}
>                   static ngx_http_module_t ngx_http_newmodule_module_ctx = {}
>                   ngx_module_t ngx_http_newmodule_module = {...,
>                               //ctx,对于HTTP模块来说，ctx必须是ngx_http_module_t接口
>                               ngx_http_newmodule_module_ctx,
>                               //commands
>                               ngx_http_newmodule_commands,
>                               //定义http模块时，必须设置成NGX_HTTP_MODULE
>                               NGX_HTTP_MODULE,
>                               ...}
>                   配置项对应的回调函数：
>                       static char *ngx_http_newmodule(){
>                               ...;
>                               //在NGX_HTTP_CONTENT_PHASE阶段会调用此回调函数
>                               clcf->handler = ngx_http_newmodule_handler;
>                               }
>                   实际完成处理的回调函数：
>                       static ngx_int_t ngx_http_newmodule_handler()
>               (3)编译测试
>                   ./configure --add-module=newmodule/
>                   make install
>
>                   配置nginx.conf
>                       location / {
>                               newmodule;
>                            }
>
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
