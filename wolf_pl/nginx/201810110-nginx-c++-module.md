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
>               (1)首先引入需要的nginx核心模块头文件
>               (2)定义一个nginx的HTTP模块ngx_module_t，编写代码实现逻辑处理
>                   七个重要的函数模块回调：
>                       /**
>                        * 七个重要的模块回调点
>                        */
>                        //master进程启动时调用，但是目前框架从不调用，因此直接设置成NULL就行
>                        ngx_int_t           (*init_master)(ngx_log_t *log);
>                        //初始化所有模块时被调用，master/worker模式下，在启动worker前完成
>                        ngx_int_t           (*init_module)(ngx_cycle_t *cycle);
>                        //worker子进程已经产生，每个worker进程初始化过程会调用所有模块的init_process
>                        ngx_int_t           (*init_process)(ngx_cycle_t *cycle);
>                        //由于nginx不支持多线程模式，所以init_thread在框架中没被调用过
>                        ngx_int_t           (*init_thread)(ngx_cycle_t *cycle);
>                        //此函数也没被调用
>                        void                (*exit_thread)(ngx_cycle_t *cycle);
>                        //worker进程退出前调用
>                        void                (*exit_process)(ngx_cycle_t *cycle);
>                        //master退出前被调用
>                        void                (*exit_master)(ngx_cycle_t *cycle);
>
>                   函数定义过程：
>                       static ngx_int_t ngx_http_newmodule_handler()
>                       static char* ngx_http_newmodule()
>                       static ngx_command_t ngx_http_newmodule_commands[] = {
>                                   ngx_string("mymodule"),
>                                   ...,
>                                   //当某个配置快中出现newmodule时，就会回调此函数
>                                   ngx_http_newmodule,
>                                   ...}
>                       static ngx_http_module_t ngx_http_newmodule_module_ctx = {}
>                       ngx_module_t ngx_http_newmodule_module = {...,
>                                   //ctx,对于HTTP模块来说，ctx必须是ngx_http_module_t接口
>                                   ngx_http_newmodule_module_ctx,
>                                   //commands
>                                   ngx_http_newmodule_commands,
>                                   //定义http模块时，必须设置成NGX_HTTP_MODULE
>                                   NGX_HTTP_MODULE,
>                                   ...}
>                       配置项对应的回调函数：
>                           static char *ngx_http_newmodule(){
>                                   ...;
>                                   //在NGX_HTTP_CONTENT_PHASE阶段会调用此回调函数
>                                   clcf->handler = ngx_http_newmodule_handler;
>                                   }
>                       实际完成处理的回调函数：
>                          static ngx_int_t ngx_http_newmodule_handler()
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

- **编写流程：**
>       1、定义模块配置结构
>           struct ngx_http_newmodule_loc_conf_t{ngx_str_t ed;};
>           定义newmodule模块的指令和参数转化函数：
>               定义模块指令：
>                   static ngx_command_t ngx_http_newmodule_commands[] = {...,ngx_http_newmodule,...}
>               参数转化函数：
>                   static char* ngx_http_newmodule() {
>                           clcf->handle = ngx_http_newmodule_handler;
>                       }
>       2、定义模块Context
>           static char* ngx_http_newmodule_create_loc_conf();  //初始化一个配置结构体
>           static char* ngx_http_newmodule_merge_loc_conf();   //将其父block的配置信息合并到此结构体，实现了配置的继承
>           static ngx_http_module_t ngx_http_newmodule_module_ctx = {NULL,ngx_http_newmodule_init,NULL,NULL,NULL,
>                                    NULL,ngx_http_newmodule_create_loc_conf,
>                                    ngx_http_newmodule_merge_loc_conf};
>       3、定义Handler，模块具体逻辑的处理
>           static ngx_int_t ngx_http_newmodule_handler(ngx_http_request_t *r){//处理具体的http请求}
>       4、组合nginx module
>           ngx_module_t ngx_http_newmodule_module = {
>                   NGX_MODULE_V1,
>                   ngx_http_newmodule_module_ctx,      //module context
>                   ngx_http_newmodule_commands,        //module directives
>                   NGX_HTTP_MODULE,                    //module type
>                   NULL,                               //init master
>                   NULL,                               //init module
>                   NULL,                               //init process
>                   NULL,                               //init thread
>                   NULL,                               //exit thread
>                   NULL,                               //exit process
>                   NULL,                                //exit master
>                   NGX_MODULE_V1_PADDING
>                   }
>
>       5、整理模块代码
>       定义模块配置结构，命名规则ngx_http_[module name]_[main/srv/loc]_conf_t，其中main,srv和loc分别用于表示同一模块在三层block中的配置信息
>           struct ngx_http_newmodule_loc_conf_t{ngx_str_t ed;};
>           static char* ngx_http_newmodule();
>           static void* ngx_http_newmodule_create_loc_conf();
>           static char* ngx_http_newmodule_merge_loc_conf();
>           static ngx_int_t ngx_http_newmodule_init();
>       定义newmodule模块的指令
>           static ngx_command_t ngx_http_newmodule_commands[] = {...,ngx_http_newmodule,...}
>       定义ngx_http_module_t类型的结构体变量，命名规则ngx_http_[module name]_module_ctx，这个结构体主要用于定义各个hook函数，
>           ngx_http_newmodule_create_loc_conf和ngx_http_newmodule_merge_loc_conf会被nginx自动调用
>           static ngx_http_module_t ngx_http_newmodule_module_ctx = {NULL,ngx_http_newmodule_init,NULL,NULL,NULL,
>                                    NULL,ngx_http_newmodule_create_loc_conf,
>                                    ngx_http_newmodule_merge_loc_conf};
>
>       组合nginx module
>           上面是定义了nginx各种组件，然后就是将他们组合起来，一个nginx模块被定义为一个ngx_module_t结构体，这里主要需要填入的信息从上到下一次为Context、指令数组、模块类型以及若干若干特定时间的回调处理函数
>           ngx_module_t ngx_http_newmodule_module = {
>                   NGX_MODULE_V1,
>                   ngx_http_newmodule_module_ctx,      //module context
>                   ngx_http_newmodule_commands,        //module directives
>                   NGX_HTTP_MODULE,                    //module type
>                   NULL,                               //init master
>                   NULL,                               //init module
>                   NULL,                               //init process
>                   NULL,                               //init thread
>                   NULL,                               //exit thread
>                   NULL,                               //exit process
>                   NULL,                                //exit master
>                   NGX_MODULE_V1_PADDING
>                   }
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
>       参考：https://www.cnblogs.com/gaohj/p/7019712.html     实战开发一个Nginx扩展 (Nginx Module)
>       https://blog.csdn.net/qq_18810607/article/details/79886076       开发一个Nginx模块(C语言和c++版本)
>       https://www.kancloud.cn/digest/understandingnginx/202604    Nginx源码解析
>
>
>
>
>
>
>
