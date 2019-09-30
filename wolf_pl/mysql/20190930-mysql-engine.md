## python - mysql engine
- **概述：**
>       主要 MyISAM 与 InnoDB 两个引擎：
>           1、InnoDB 支持事务，MyISAM 不支持，这一点是非常之重要。事务是一种高级的处理方式，如在一些列增删改中只要哪个出错还可以回滚还原，而 MyISAM就不可以了；
>           2、MyISAM 适合查询以及插入为主的应用，InnoDB 适合频繁修改以及涉及到安全性较高的应用；
>           3、InnoDB 支持外键，MyISAM 不支持
>           4、MyISAM 是默认引擎，InnoDB 需要指定；
>           5、InnoDB 不支持 FULLTEXT 类型的索引
>           6、InnoDB 中不保存表的行数，如 select count(*) from table 时，InnoDB；需要扫描一遍整个表来计算有多少行，但是 MyISAM 只要简单的读出保存好的行数即可。注意的是，
>               当 count(*)语句包含 where 条件时 MyISAM 也需要扫描整个表
>           7、对于自增长的字段，InnoDB 中必须包含只有该字段的索引，但是在 MyISAM表中可以和其他字段一起建立联合索引；
>           8、清空整个表时，InnoDB 是一行一行的删除，效率非常慢。MyISAM 则会重建表；
>           9、InnoDB 支持行锁（某些情况下还是锁整表，如 update table set a=1 where user like '%lee%'
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
>
>
>
>
