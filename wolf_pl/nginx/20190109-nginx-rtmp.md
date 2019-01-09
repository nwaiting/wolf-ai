## nginx - nginx rtmp 模块
- **概述：**
>
>
>

- **rtmp解析rtmp配置项示意流程图：**
>       ngx_core_module     主模块
>       ngx_conf_parse      配置文件解析器
>       ngx_core_module     ngx_rtmp_module （初始化每一个rtmp模块，依次调用各个rtmp模块的create_(main、srv、app)_conf）
>       rtmp_core_module    ngx_rtmp_core_module
>       rtmp系列子module
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
>
>
>
