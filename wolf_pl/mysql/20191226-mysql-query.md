## python - mysql query
- **概述：**
>
>
>
>
>


- **join：**
>       select * from A a left join B b on a.id=b.id
>       1、left join:
>           保留左边A的数据，右边b的字段为空
>       2、right join
>           保留右边B的数据，左边a的字段为空
>       3、inner join
>           取交集，取两个都有的数据
>       4、union
>           取并集，取所有的数据
>

- **GROUP_CONCAT  separator：**
>       GROUP_CONCAT  separator可将查询结果用字符串连接变为一行,需配合使用GROUP BY
>           注意：需配合group by 使用
>           select id,group_concat(name separator ';') mul_name from A group by id
>           select id,group_concat(name order by id separator ';') mul_name from A group by id
>           select id,group_concat(distinct name separator ';') mul_name from A group by id
>

- **聚合函数：**
>       mysql聚合函数总结：
>           1、聚合函数 count（），求数据表的行数
>               select count(*/字段名) from A
>           2、聚合函数 max（），求某列的最大数值
>           3、聚合函数min（）,求某列的最小值
>           4、聚合函数sum（）,对数据表的某列进行求和操作
>           5、聚合函数avg()，对数据表的某列进行求平均值操作
>           6、聚合函数和分组一起使用
>               select count(*),group_concat(age) from A group by age
>
>       分组和聚合函数的一个问题：
>           select name ,max(score) from stu group by bianji;//错误，这样最大成绩对应的学生并不是原学生。
>           参考：https://www.cnblogs.com/straybirds/p/5130852.html        mysql概要（四）order by ，limit ，group by和聚合函数的特点，子查询
>
>

- **limit 使用：**
>       截取记录的条数，一般和order by 配合使用
>       如：
>           limit(2,2),即从第三记录开始取两条记录
>           limit 2,即从第一条记录开始取2条
>           SELECT * FROM products LIMIT 0,8;
>           SELECT * FROM products LIMIT 8 OFFSET 0; (在mysql 5以后支持这种写法)
>
>           使用limit的优化：
>               Select * From ibmng Where id >=(Select id From ibmng Order By id limit 1000000,1) limit 10
>               https://blog.csdn.net/fullstack/article/details/38169407    MySQL大数据下Limit使用
>

- **sql中的关系型运算符顺序：**
>       关系型运算符优先级高到低为：NOT >AND >OR
>
>

- **replace into 与 insert into on duplicate key update区别：**
>       replace into 与 insert into on duplicate key update
>       都是先尝试插入记录，如果不成功，则删除记录，
>       1、replace into不保留原记录的值
>       2、insert into on duplicate key update保留原来字段的值
>       然后插入一条新记录
>
>       如果你插入的记录导致一个UNIQUE索引或者primary key(主键)出现重复，那么就会认为该条记录存在，则执行update语句而不是insert语句，反之，则执行insert语句而不是更新语句。
>       所以 ON DUPLICATE KEY UPDATE是不能写where条件的
>       因为由UNIQUE索引或者主键保证唯一性，不需要WHERE子条件。所以上面的INSERT INTO t_stock_chg(f_market, f_stockID, f_name) VALUES('SH', '600000', '白云机场') ON DUPLICATE KEY UPDATE f_market='SH', f_name='浦发银行';中f_stockID就是唯一主键
>       这里特别需要注意的是：如果行作为新记录被插入，则受影响行的值为1；如果原有的记录被更新，则受影响行的值为2，如果更新的数据和已有的数据一模一样，则受影响的行数是0，这意味着不会去更新，也就是说即使你有的时间戳是自动记录最后一次的更新时间，这个时间戳也不会变动。
>

- **msyql统计count：**
>       使用count()函数实现条件统计的基础是对于值为NULL的记录不计数，常用的有以下三种方式，假设统计num大于200的记录
>           select count(num > 200 or null) from a;
>           select count(if(num > 200, 1, null)) from a
>           select count(case when num > 200 then 1 end) from a
>
>           if()函数：SELECT if(sex=0,'女','男') AS sex FROM student; 这个if()函数就相当于java里面的三目运算符。
>               if(expr1,expr2,expr3)，如果expr1的值为true，则返回expr2的值，如果expr1的值为false，则返回expr3的值。
>               但是如果在sum中使用了if()函数，就是对结果值进行累加，例如SUM(IF(`hosts`.state = 0, 1, 0))，当hosts.state的值为0时，和加1，不为0时，和加0。
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
