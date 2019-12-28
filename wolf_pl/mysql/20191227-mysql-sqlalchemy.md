## python - mysql sqlalchemy
- **概述：**
>
>
>

- **sqlalchemy语法与sql对应关系：**
>       1、排序：
>           # 第一个字段升序排序，第二个字段降序排序
>               select class.class_name, count(1) as c from users join class on users.class_id = class.id
>                   group by class.class_name order by class_name, c desc;
>           # 两个字段都是降序排序
>               select class.class_name, count(1) as c from users join class on users.class_id = class.id
>                   group by class.class_name order by class_name desc, c desc;
>
>           from sqlalchemy import desc
>           from sqlalchemy.sql import func
>           User.query.join(Class, User.class_id == Class.id).group_by(Class.class_name).\
>               with_entities(Class.class_name, func.count('*').label('c')).order_by(Class.class_name, desc('c')).all()
>
>       case自定义排序
>           比如有一个排序需求：(status==1,modify_user==None,status==3,status==2)
>           from sqlalchemy import case
>           offices_query.order_by(case((ResourcesOffice.status=='1',1),
>               (ResourcesOffice.modify_user.is_(None),2),
>               (ResourcesOffice.status =='3',3),
>               (ResourcesOffice.status =='2',4)))
>           case里面是一个元组，然后(ResourcesOffice.status =='1',1)，后面的1代表的是顺序，前面的是筛选条件

>       2、sql根据聚合函数排序
>           ORDER BY IFNULL(length(trim(s.class_name)),0) ASC
>               trim(s.class_name)：去除字符串中的空格
>               length(trim(s.class_name)：去除空格后字符串长度
>               ifnull(expr1,expr2):如果不是空，取expr1;如果是空，取expr2
>
>           根据聚合查询总收入，按总收入逆序
>               db.session.query(TpOrders.room_type_id, (func.sum(TpOrders.real_income)).label('total_real_income'),  func.count(TpOrders.id)).
>                   group_by(TpOrders.room_type_id).order_by( desc('total_real_income')).all()
>
>           根据日期（年月日，忽略时分秒）进行分组统计查询
>               db.session.query(func.date_format(TpOrders.check_out_date, '%Y-%m-%d').label('date'),func.sum(TpOrders.real_income),func.count(TpOrders.id)).
>                   group_by('date').all()
>
>       3、sqlalchemy查询：
>           a、简单查询
>               Post.query.filter(Post.title == 'aaa').first()
>           b、left join查询
>               select user.name,count(article.id) from  user
>                left join article
>                on user.id=article.uid
>                group by user.id
>                order by count(article.id) desc
>           c、like查询、多条件查询
>               from sqlalchemy import and_, or_, not_
>               session.query(User).filter(
>                   or_(
>                       User.id<2,
>                       and_(User.name=='aaa',User.id>3),
>                       User
>                   )).all()
>               等价的sql：
>                   select * from User where id<2 or (name="eric" and id>3) or extra != ""
>           d、filter组合查询
>               sess.query(IS).filter(IS.node == node).filter(IS.password == password).all()    连续调用
>               sess.query(IS).filter(and_(IS.node == node,IS.password == password)).all()      使用and_
>               sess.query(IS).filter_by(node=node, password=password).all()    调用filter_by
>
>           e、常用的条件查询
>               相等:
>                   query.filter(User.name == 'ed')
>               不相等
>                   query.filter(User.name != 'ed')
>               通配符搜索
>                   query.filter(User.name.like('%ed%'))
>               通配符搜索(不敏感)
>                   ilike()
>               存在于
>                   query.filter(User.name.in_(['ed', 'wendy', 'jack']))
>               不存在于
>                   query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
>               为空
>                   query.filter(User.name == None)
>               不为空  IS NOT NULL
>                   query.filter(User.name != None)
>               AND
>                   query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
>               OR
>                   query.filter(or_(User.name == 'ed', User.name == 'wendy'))
>               MATCH
>                   query.filter(User.name.match('wendy'))
>
>           f、查询返回
>               返回列表(List)和单项(Scalar)
>               all()：
>                   返回一个列表
>                   session.query(User).filter(User.name.like('%ed')).order_by(User.id).all()
>                   [<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>,<User(name='fred', fullname='Fred Flinstone', password='blah')>]
>               first()：
>                   返回至多一个结果，而且以单项形式，而不是只有一个元素的tuple形式返回这个结果
>                   query.first()
>                   <User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
>               one()：
>                   返回且仅返回一个查询结果。当结果的数量不足一个或者多于一个时会报错
>               one_or_none()：
>                   从名称可以看出，当结果数量为0时返回None， 多于1个时报错
>               scalar()
>                   和one()类似，返回单项而不是tuple
>           g、聚合函数
>               from sqlalchemy import func
>               session.query(func.count(User.name), User.name).group_by(User.name).all()
>               session.query(func.count('*')).select_from(User).scalar()
>               session.query(func.count(User.id)).scalar()     对User的主键进行计数
>           h、查询时限制条数
>               limit：
>                   可以限制每次查询的时候只查询几条数据，取前10条
>                   session.query(Article).limit(10).all()
>               offset：
>                   可以限制查找数据的时候过滤掉前面多少条，如下面，从第11条数据开始取10条
>                   session.query(Article).offset(10).limit(10).all()
>               slice切片:
>                   可以对Query对象使用切片操作，来获取想要的数据。sliece(start, end) 从start取到end。slice(0,10)取第一条到第10条
>                   可以使用`slice(start,stop)`方法来做切片操作。也可以使用`[start:stop]`的方式来进行切片操作。一般在实际开发中，中括号的形式是用得比较多的。
>                   本质上来说，SQLAlchemy会将其翻译成LIMIT/OFFSET语句来实现，
>                   session.query(Article).slice(10, 20).all()
>                   session.query(Article)[0:10]
>
>
>       4、sqlalchemy添加和删除数据：
>           a、添加多条数据
>               person1 = Person(name = "blue" , age = 30)
>               person2 = Person(name = "tom" , age = 23)　
>               session.add_all([person1,person2])
>           b、sqlalchemy 没有实现replace into，只有先query，然后add
>           c、删除数据
>               user = User.query.filter_by(name='Michael').first()
>               if user is not None:
>                   db.session.delete(user)
>
>
>      5、flask-sqlalchemy实现分页：
>           Employee.query.paginate(page_index,per_page=10)
>
>           对于继承自flask_sqlalchemy.Model的类，都有一个paginate(page=None, per_page=None, error_out=True, max_per_page=None)
>               方法来获得一个flask_sqlalchemy.Pagination对象
>           paginate(page=None, per_page=None, error_out=True, max_per_page=None)
>               page:指定页码，从1开始
>               per_page:每一页有几个项
>
>       6、sqlalchemy通配符
>           db_session.query(User).filter(User.name.like('e%')).all()
>           db_session.query(User).filter(~User.name.like('e%')).all()
>

- **func中的聚合函数：**
>       func.count:
>           统计行的数量
>       func.avg
>           求平均值
>       func.max
>           求最大值
>       func.min
>           求最小值
>       func.sum
>           求和
>

- **sqlalchemy中使用原生sql查询：**
>       from sqlalchemy.sql import text
>       db_session.query(User).filter(text("select * from User id<:value and name=:name")).params(value=3,name="DragonFire")
>       db_session.query(User).filter(text("id<:value and name=:name")).params(value=3,name="DragonFire")
>
>

- **sqlalchemy中的别名：**
>       别名映射  name as nick
>       db_session.query(User.name.label("nick")).all()
>       取数据时候，就要使用nick字段
>       for row in user_list:
>           print(row.nick) # 这里要写别名了
>

- **sqlalchemy的filter和filter_by的区别：**
>       1、filter --> column == expression
>           filter中，语法更加贴近于Python的语法
>           传入参数的写法，要用：类名.列名 两个等号 去判断
>               query(User.name).filter(User.fullname==’Ed Jones’)
>           更复杂的查询的语法，比如_and()，or_()等多个条件的查询，只支持filter
>               query.filter(or_(User.name == ‘ed’, User.name == ‘wendy’))
>               query.filter(and_(User.name == ‘ed’, User.fullname == ‘Ed Jones’))
>       2、filter_by --> keyword = expression
>           传入参数的写法，只需要用：（不带类名的）列名 单个等号 就可以判断
>               query(User.name).filter_by(fullname=’Ed Jones’)
>

- **sqlalchemy更新数据：**
>       更新字段的值：
>           UPDATE user SET name="NBDragon" WHERE id=20     更新一条数据
>           db_session.query(User).filter(User.id == 20).update({"name":"NBDragon"})
>
>       更新多条数据：
>           res = db_session.query(User).filter(User.id <= 20).update({"name":"NBDragon"})
>           res返回就是当前这句更新语句所更新的行数
>

- **sqlalchemy删除数据：**
>       sqlalchemy添加和删除数据：
>           a、添加多条数据
>               person1 = Person(name = "blue" , age = 30)
>               person2 = Person(name = "tom" , age = 23)　
>               session.add_all([person1,person2])
>           b、sqlalchemy 没有实现replace into，只有先query，然后add
>           c、删除数据
>               user = User.query.filter_by(name='Michael').first()
>               if user is not None:
>                   db.session.delete(user)
>
>               DELETE FROM `user` WHERE id=20
>               db_session.query(User).filter(User.id==20).delete()
>

- **sqlalchemy的join查询：**
>       sqlalchemy中只有innner join和outer join两种：
>           query.join --> inner join
>               inner join则是将两个表中数据全部列出
>           query.outerjoin --> left outer join 或者 right outer join
>               outer join中的左链接和右链接，根据链接时主表和副表的顺序，左连接左边的全部列出，右边的按照条件查询出来
>
>       1、sql原生查询：
>           select user.username,count(article.id) from user
>               join article on user.id=article.uid
>               group by user.id order by count(article.id) desc
>       对应的sqlalchemy查询：
>           session.query(user.username,func.count(article.id)).join(article,users.id==article.uid).
>               group_by(user.id).order_by(func.count(article.id).desc())
>           由于没有使用外键，所以需要显示声明user.id==article.uid的关联关系，如果使用了外键，则会自动关联，则语句简化为：
>           session.query(user.username,func.count(article.id)).join(article).group_by(user.id).order_by(func.count(article.id).desc())
>
>       2、sql原生语句
>           select users.*,adr_count.address_count from users left join
>               (select user_id,count(*) as address_count from address group by user_id) as adr_count
>               on users.id=adr_count.user_id
>       对应的sqlalchemy查询：
>           subq = session.query(address.user_id,func.count(*).label('address_count')).group_by(address.user_id).subquery()
>           res = session.query(user.username,subq.c.address_count).outerjoin(subq, user.id==subq.c.user_id).all()
>
>       3、自己指定关联的字段，否则需要在建表时指定外键关联
>           select xxx from trans_details inner join trans_details on users.id=trans_details.user_id where users.username like '%xx%'
>       对应的sqlalchemy查询
>           session.query(trans_details).join(users, trans_details.user_id==users.id).filter(users.username.like('%xx%'))
>
>       4、多个join的复杂sql
>           SELECT credit_bills_details.no AS credit_bills_details_no, credit_bills_details.amount AS credit_bills_details_amount, cards.no AS cards_no
>           FROM credit_bills_details
>           LEFT OUTER JOIN card_trans_details ON credit_bills_details.no = card_trans_details.trans_no
>           INNER JOIN cards ON card_trans_details.to_card_id = cards.id
>           WHERE credit_bills_details.credit_bill_id=3
>
>       对应的sqlalchemy查询
>           session.query(credit_bills_details.no,credit_bills_details.amount,cards.no).
>           outerjoin(card_trans_details, credit_bills_details.no==card_trans_details.no).
>           join(cards, card_trans_details.to_card_id==cards.id).
>           filter(credit_bills_details.credit_bill_id==3)
>

- **having：**
>       having：对查找结果进一步过滤，类似于SQL语句的where
>       原生sql：
>           select age, count(id) from user group by age having age > 20
>       对应的sqlalchemy查询：
>           session.query(user.age, func.count(user.id)).group_by(user.age).having(user.age > 20).all()
>
>
>

- **待续：**
>       参考：https://github.com/eastossifrage/sql_to_sqlalchemy/blob/master/chapter002/departments.py     sqlalchemy和sql查询
>           https://segmentfault.com/q/1010000018380836/    sqlalchemy如何拼接多个filter
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
