#coding=utf-8

"""
    python常用的数据结构：
        list
        tuple
        dict
        set

    python常用的数据结构底层实现：
        python的dict底层实现：
            哈希表 (hash tables)
                哈希函数
                装填因子
                冲突
            CPython使用伪随机探测(pseudo-random probing)的散列表(hash table)作为字典的底层数据结构
            解决哈希冲突通常的做法有两种，一种是链接法，另一种是开放寻址法，Python选择后者
            链接法：
                把散列到同一个槽中的所有元素都放在一个链表中
            开放寻址法：
                开放寻址法中，所有的元素都存放在散列表里，当产生哈希冲突时，通过一个探测函数计算出下一个候选位置，
                    如果下一个获选位置还是有冲突，那么不断通过探测函数往下找，直到找个一个空槽来存放待插入元素

        python的set底层实现：
            CPython中集合和字典非常相似。事实上，集合被实现为带有空值的字典，只有键才是实际的集合元素。此外，集合还利用这种没有值的映射做了其它的优化。

        python的list底层实现：
            在CPython中，列表list被实现为长度可变的数组

        python的tuple底层实现：
            在CPython中，tuple被实现为数组

"""

"""
    python对象：
        1.可变对象和不可变对象：不可变对象包括int，float，string，tuple等。可变对象包括list，dict，自定义类的实例等。
        2.在python中通过= 复制的变量，都是同时即把变量的值，也把变量在内存中的地址复制也过去了。即=复制过的变量不仅内存地址一样，变量的值也一样。
            但是需要注意的是：对于不可变类型(如int)的变量，如果要更改变量的值，则会创建一个新值，并且给这个新值分配一个新的内存地址，然后把变量指向这个新值的内存地址上，
            而旧值如果没有被引用就等待垃圾回收。如果是可变类型变量。如果修改变量的值，则可以直接修改变量的值，变量的引用地址不会变。
            a、不可变类型：
                变量赋值 a=5 后再赋值 a=10，这里实际是新生成一个 int 值对象 10，再让 a 指向它，而 5 被丢弃，不是改变a的值，相当于新生成了a。
                    数值类型 int, long, bool, float
                    字符串 str
                    元组 tuple
            b、可变类型：
                变量赋值 la=[1,2,3,4] 后再赋值 la[2]=5 则是将 list la 的第三个元素值更改，本身la没有动，只是其内部的一部分值被修改了。
                    列表 list
                    字典 dict
        3.本质是因为不可变对象一旦新建后，系统就会根据他的大小给他分配固定死的内存，所以不允许修改，只修改值只能申请新的内存和地址。而可变对象，他的内存大小可以随着值的变化而自动扩容   

     Python的所有变量其实都是指向内存中的对象的一个指针，都是值的引用。

"""


class TestObj(object):
    def __init__(self):
        pass
    def __str__(self):
        # 外部在print(obj)或者str(obj)  两种情况下会调用
        pass
    def __repr__(self):
        # 外部直接obj时候(如在命令行中)或在外部直接调用repr(obj)
        pass
    def __enter__(self):
        # 外部使用with时会调用
        pass
    def __exit__(self):
        # with退出的时候会调用
        pass
    def __getattr__(self):
        # 对象获取属性值的时候会触发
        pass
    def __setattr__(self):
        # 对象设置属性值的时候会触发
        # obj.a=1会触发
        pass
    def __setitem__(self):
        # 对象设置属性值的时候会触发
        # obj['a']=1 会触发
        pass
    def __call__(self, *args, **kwargs):
        # obj(a,b)  会调用
        pass
    def __eq__(self):
        # todo ...
        pass
    __slots__ = ('name','age')
        # 如果我们想要限制class的属性怎么办？比如，只允许对Student实例添加name和age属性
        # 变量：用tuple定义允许绑定的属性名称
        # 定义一个特殊的__slots__变量，来限制该class能添加的属性
        # 注意：使用__slots__要注意，__slots__定义的属性仅对当前类起作用，对继承的子类是不起作用的
        #       除非在子类中也定义__slots__，这样，子类允许定义的属性就是自身的__slots__加上父类的__slots__


"""
    python使用pipenv虚拟环境打包exe文件
    #建立虚拟环境
    pipenv install
    #进入虚拟环境（上一步可省略,因为没有虚拟环境的话会自动建立一个）
    pipenv shell
    #安装模块
    pip install requests pyquery pysimplegui fake_useragent
    pip install -r requirements
    #打包的模块也要安装
    pip install pyinstaller
    #开始打包
    pyinstaller -Fw E:\test\url_crawler.py
"""





if __name__ == '__main__':
    main()
