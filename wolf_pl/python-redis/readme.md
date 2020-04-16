### python-redis 相关
- **概述：**
>
>
>
>
>
>
>

- **python常用操作：**
>       Python操作Redis的5种数据类型：
>           1、字符串类型 String
>               redis.set("name", "Jack", ex=20)            #ex 过期时间 单位为 s
>               redis.mset(name1='zhangsan', name2='lisi')  #批量设置值
>               redis.mget(["name1","name2"])               #批量获取
>               redis.scan_iter(match=None, count=None)     #同字符串操作，用于增量迭代获取key
>               ret = redis.get("name")
>           2、列表类型 list
>               redis.lpush("object", 'six')
>               redis.lpush("object", 'five')
>               ret = redis.lrange("object", 0, 5)
>               print(ret[::-1])
>           3、哈希类型 hash
>               redis.hset("user:info", "name", "Jack")
>               redis.hset("user:info", "age", "20")
>               redis.hscan_iter(name, match=None, count=None)  #利用yield封装hscan创建生成器，实现分批去redis中获取数据
>                   参数：match，匹配指定key，默认None 表示所有的key
>                         count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
>               ret = redis.hgetall("user:info")
>           4、集合类型 set
>               redis.sadd("set", "one")
>               redis.sadd("set", "two")
>               redis.sscan_iter(name, match=None, count=None)  #用于增量迭代分批获取元素，避免内存消耗太大
>               ret = redis.smembers("set")
>           5、有序集合类型 sorted set
>               redis.zadd("mark", "one", 1)
>               redis.zadd("mark", "two", 2)
>               redis.zadd("mark", "three", 3)
>               redis.zscan_iter(name, match=None, count=None,score_cast_func=float)
>               ret = redis.zrange("mark", 1, 3)
>

- **python-redis连接方式：**
>       连接方式1：
>           # decode_responses=True 解决的是值类型是 bytes 字节的问题
>           r = redis.Redis(host="192.168.66.128", port="6379", db=0, decode_responses=True)
>       连接方式2：
>           pool = redis.ConnectionPool(host="192.168.66.128", port=6379, db=0, decode_responses=True)
>           r = redis.Redis(connection_pool=pool)
>
>
>
>
>
>
>


- **常用命令：**
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
>
>
>
>
>
>
