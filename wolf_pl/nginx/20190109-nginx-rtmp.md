## nginx - nginx rtmp 模块
- **概述：**
>
>       本文主要内容：
>           nginx-rtmp开发
>           RTMP启动流程
>           调用各个RTMP模块preconfiguration
>           初始化事件处理，主要是AMF消息，特殊消息，处理回调注册
>           nginx-rtmp-module目录结构
>           notify模块
>           nginx-rtmp各模块主要功能
>
>
>
>
>

- **nginx-rtmp开发：**
>
>       nginx模块需要定义三个变量，command、ctr、module。rtmp三个变量在rtmp.c文件中，
>       rtmp的启动函数在ngx_rtmp_commands申明的ngx_rtmp_block()
>           ngx_command_t  ngx_rtmp_commands
>               设置set执行函数
>           ngx_core_module_t  ngx_rtmp_module_ctx
>
>           ngx_module_t  ngx_rtmp_module
>
>
>       ngx_rtmp_commands中的set函数是nginx启动的时候，ngx_conf_handler()中调用，调用堆栈如下：
>           static ngx_int_t ngx_conf_handler(ngx_conf_t *cf, ngx_int_t last)
>           char * ngx_conf_parse(ngx_conf_t *cf, ngx_str_t *filename)
>           char * ngx_conf_param(ngx_conf_t *cf)
>           ngx_cycle_t * ngx_init_cycle(ngx_cycle_t *old_cycle)
>           int ngx_cdecl  main(int argc, char *const *argv)
>

- **RTMP启动流程：**
>
>       1、计算RTMP模块数并设置每个模块的上下文索引
>       2、  为每个RTMP模块创建main_conf
>       3、  为每个RTMP模块创建srv_conf
>       4、  为每个RTMP模块创建app_conf
>       5、  调用各个RTMP模块preconfiguration
>       6、  初始化各个RTMP模块 init_main_conf
>       7、  初始化各个RTMP模块各个APP的merge_srv_conf
>       8、  初始化各个RTMP模块各个APP的merge_app_conf
>       9、  初始化各个RTMP服务事件
>

- **调用各个RTMP模块preconfiguration：**
>
>       主要是注册回调
>       NGX_RTMP_CONNECT
>           注册模块：ngx_rtmp_limit_module
>           注册回调：ngx_rtmp_limit_connect
>
>       NGX_RTMP_HANDSHAKE_DONE
>           注册模块：ngx_rtmp_relay_module中初始化
>           注册回调：ngx_rtmp_relay_handshake_done
>
>       NGX_RTMP_DISCONNECT
>           注册模块：ngx_rtmp_cmd_module
>           注册回调：ngx_rtmp_cmd_disconnect_init;
>           注册模块：ngx_rtmp_codec_module
>           注册回调：ngx_rtmp_codec_disconnect;
>           注册模块：ngx_rtmp_limit_module
>           注册回调：ngx_rtmp_limit_disconnect;
>           注册模块：ngx_rtmp_log_module
>           注册回调：ngx_rtmp_log_disconnect;
>           注册模块：ngx_rtmp_netcall_module
>           注册回调：ngx_rtmp_netcall_disconnect;
>
>       NGX_RTMP_MSG_AUDIO
>           注册模块：ngx_rtmp_codec_module
>           注册回调：ngx_rtmp_codec_av
>           注册模块：ngx_rtmp_dash_module
>           注册回调：ngx_rtmp_dash_video
>           注册模块：ngx_rtmp_hls_module
>           注册回调：ngx_rtmp_hls_audio
>           注册模块：ngx_rtmp_live_module
>           注册回调：ngx_rtmp_live_av
>           注册模块：ngx_rtmp_record_module
>           注册回调：ngx_rtmp_record_av
>
>       NGX_RTMP_MSG_VIDEO
>           注册模块：ngx_rtmp_codec_module
>           注册回调：ngx_rtmp_codec_av
>           注册模块：ngx_rtmp_dash_module
>           注册回调：ngx_rtmp_dash_video
>           注册模块：ngx_rtmp_hls_module
>           注册回调：ngx_rtmp_hls_audio
>           注册模块：ngx_rtmp_live_module
>           注册回调：ngx_rtmp_live_av
>           注册模块：ngx_rtmp_record_module
>           注册回调：ngx_rtmp_record_av
>

- **初始化事件处理，主要是AMF消息，特殊消息，处理回调注册**
>
>       static size_t    pm_events[]{}
>       static size_t    amf_events[]{}
>       ngx_rtmp_cmd_module模块：
>           对相应的用户控制消息进行注册
>           static ngx_rtmp_amf_handler_t ngx_rtmp_cmd_map[] = {
>               { ngx_string("connect"),            ngx_rtmp_cmd_connect_init},
>               { ngx_string("createStream"),       ngx_rtmp_cmd_create_stream_init},
>               { ngx_string("closeStream"),        ngx_rtmp_cmd_close_stream_init      },
>               { ngx_string("deleteStream"),       ngx_rtmp_cmd_delete_stream_init     },
>               { ngx_string("publish"),            ngx_rtmp_cmd_publish_init           },
>               { ngx_string("play"),               ngx_rtmp_cmd_play_init              },
>               { ngx_string("play2"),              ngx_rtmp_cmd_play2_init             },
>               { ngx_string("seek"),               ngx_rtmp_cmd_seek_init              },
>               { ngx_string("pause"),              ngx_rtmp_cmd_pause_init             },
>               { ngx_string("pauseraw"),           ngx_rtmp_cmd_pause_init             },}
>
>
>
>

- **开始各个RTMP服务侦听，注册连接到时时执行ngx_rtmp_init_connection的回调**
>
>
>
>
>

- **nginx-rtmp-module目录结构：**
>
>       nginx-rtmp-module/
>              | ------ client/        独立模块，基于nginx的http客户端
>              | ------ multiport/     独立模块，多进程的多端口配置，每个进程监听独立端口
>              | ------ toolkit/        独立模块，工具函数
>              | ------ dash/         rtmp模块，dash直播
>              | ------ hls/           rtmp模块，hls 直播
>              | ------ http/          rtmp模块，http-flv直播
>              | ------ ngx_rtmp.c  驱动rtmp模块加载，监听nginx.conf文件中配置的端口
>              | ------ ngx_live.c   维护直播流和rtmp session映射表，提供对流和session的增删改查功能
>              | ------ ngx_rtmp_cmd_module.c 控制rtmp协议的流程，在每个rtmp阶段到来时触发相应的函数栈
>              | ------ ngx_rtmp_notify_module.c 在rtmp不同阶段向外发送http通知消息
>              | ------ ngx_rtmp_relay_module.c 向外回源或转推功能
>              | ------ ngx_rtmp_live_module.c  将音视频数据从发布者分发给订阅者
>              | ------ ngx_rtmp_codec_module.c 解析音视频头，avc_header hevc_header aac_header
>              | ------ ngx_rtmp_gop_module.c 缓存完整gop数据，实现秒开功能
>              | ------ ngx_rtmp_handler.c 网络数据收发响应函数
>              | ------ ngx_rtmp_control_module.c 控制接口，通过http消息控制rtmp session的消亡
>              | ------ ngx_rtmp_init.c 网络连接/rtmp-session的初始化和关闭接口
>

- **notify模块：**
>       **控制事件包含：**
>           proc：进程启动时通知，只支持 start 触发点
>           play：有播放端接入时通知
>           publish：有推流端接入时通知
>           pull：触发回源拉流事件控制
>           push：触发转推事件控制
>           stream：流创建通知
>           meta：收到音视频头通知
>           record(还未支持)：启动录制通知
>
>       **控制事件触发点包含：**
>           start：事件发生时触发，配置或不配置 start 均为默认开启状态
>           update：事件持续过程中的心跳刷新
>           done：事件结束时触发
>
>       **基本模型：**
>           1、当有拉流时，触发 play 通知，当拉流持续时，每隔一定时间间隔向外发送 update 通知，当拉流结束时发送 done 通知
>           2、当有推流时，触发 publish 通知，当推流持续时，每隔一定时间间隔向外发送 update 通知，当推流结束时发送 done 通知
>           3、当有一路拉流或一路推流时，触发 stream 通知，当流还继续存在时，每隔一定时间间隔向外发送 update 通知，
>               所有推流和拉流都结束时发送 done 通知
>

- **nginx-rtmp各模块主要功能：**
>       ngx_rtmp_dash_module http模块里播放MPEG-DASH相关处理
>       ngx_rtmp_mp4_module 主要支持rtmp MP4这块点播相关功能，支持seek操作
>       ngx_rtmp_flv_module 主要是flv文件格式的点播相关功能，支持seek操作
>       ngx_rtmp_play_module rtmp点播相关，支持本地，远程两种方式点播，远程点播http方式，支持flv，mp4两种格式
>       ngx_rtmp_record_module 视频录制默认是flv格式， 支持按时间，按文件大小，帧个数录制文件
>       ngx_rtmp_hls_module rtmp中rtmp转hls协议处理
>       ngx_rtmp_mpegts rtmp中rtmp转ts协议处理
>       ngx_rtmp_handshake 主要是是三次握手相关
>       ngx_rtmp_handler 主要是数据接收recv，发送send，ping命令相关
>       ngx_rtmp_init 初始化连接相关的信息
>       ngx_rtmp_core_module 主要是rtmp协议核心配置相关.
>       ngx_rtmp rtmp配置解析，rtmp事件框架的初始化信息，注册事件回调函数(协议handler，amfhandler)
>       ngx_rtmp_receive 主要是rtmp协议数据接收这块
>       ngx_rtmp_send 数据发送这块，以及各种rtmp消息包发送封装的函数
>       ngx_rtmp_live_module 主要处理接收音视频消息数据，以及ngx_rtmp_live_av中进行数据分发，从接收到发送给每个其他session
>       ngx_rtmp_netcall_module 主要是http请求相关部分
>       ngx_rtmp_notify_module 主要rtmp发送http请求，通知作用主要监听connect,disconnect,play,publish,close,record_done等相关事件
>       ngx_rtmp_relay_module 主要是rtmp提供回源请求拉流，以及转推，监听_result，_error, onStatus
>       ngx_rtmp_stat_module 主要是rtmp流状态信息可以输出到本地文件
>       ngx_rtmp_shared 主要是rtmp协议内存管理方面，其中用到了引用计数来管理内存
>       ngx_rtmp_bandwidth 主要是rtmp协议的带宽计费
>       ngx_rtmp_cmd_module rtmp消息命令相关play，publish
>       ngx_rtmp_codec_module rtmp音视频编解码信息相关
>       ngx_rtmp_control_module 主要是一些控制接口，录制开始/暂停，支持record,query,drop相关的接口
>       ngx_rtmp_eval 主要提供一些变量替换的函数接口，有内存泄漏
>       ngx_rtmp_amf ngx_rtmp_bitop 主要是封装读，写amf包信息
>       ngx_rtmp_access_module 监听play，publish事件，对ip做检查访问
>       ngx_rtmp_auto_push_module 多进程方案，推流来时，自动推流到其他worker进程
>       ngx_rtmp_exec_module 主要监听publish，play，close，record_done事件，然后进行执行脚本进行相应的业务，如转码
>       ngx_rtmp_limit_module 主要监听connect以及disconnect事件，通过计算连接数量来限制连接个数
>       ngx_rtmp_log_module 主要是rtmp日志相关，连接断开disconncet事件的时候，输出访问日志相关
>

- **关闭连接：**
>       ngx_rtmp_close_session_handler (e=0x23efb28) at ../nginx-rtmp-module/ngx_rtmp_init.c:284
>       in ngx_event_process_posted (cycle=cycle@entry=0x2314bd0, posted=0xe76a00 <ngx_posted_events>) at src/event/ngx_event_posted.c:34
>       in ngx_process_events_and_timers (cycle=cycle@entry=0x2314bd0) at src/event/ngx_event.c:269
>       in ngx_worker_process_cycle (cycle=0x2314bd0, data=<optimized out>) at src/os/unix/ngx_process_cycle.c:815
>       in ngx_spawn_process (cycle=cycle@entry=0x2314bd0, proc=proc@entry=0x43ea77 <ngx_worker_process_cycle>, data=data@entry=0x0,
>           name=name@entry=0x501573 "worker process", respawn=respawn@entry=-3) at src/os/unix/ngx_process.c:198
>       in ngx_start_worker_processes (cycle=cycle@entry=0x2314bd0, n=1, type=type@entry=-3) at src/os/unix/ngx_process_cycle.c:396
>       in ngx_master_process_cycle (cycle=cycle@entry=0x2314bd0) at src/os/unix/ngx_process_cycle.c:135
>       in main (argc=<optimized out>, argv=<optimized out>) at src/core/nginx.c:381
>

- **接收数据异常分析：**
>       用wireshark抓包可以看出有'TCP Window Full'的问题，经查造成此问题的原因就是播放器来不及接收数据
>
>

- **待续：**
>       参考：https://blog.evanxia.com/2017/02/1264    Nginx-rtmp-module模块源码学习
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
