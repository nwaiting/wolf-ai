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
>               redis.set("name", "Jack", ex=20)    #ex 过期时间 单位为 s
>               ret = redis.get("name")
>           2、列表类型 list
>               redis.lpush("object", 'six')
>               redis.lpush("object", 'five')
>               ret = redis.lrange("object", 0, 5)
>               print(ret[::-1])
>           3、哈希类型 hash
>               redis.hset("user:info", "name", "Jack")
>               redis.hset("user:info", "age", "20")
>               ret = redis.hgetall("user:info")
>           4、集合类型 set
>               redis.sadd("set", "one")
>               redis.sadd("set", "two")
>               ret = redis.smembers("set")
>           5、有序集合类型 sorted set
>               redis.zadd("mark", "one", 1)
>               redis.zadd("mark", "two", 2)
>               redis.zadd("mark", "three", 3)
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
