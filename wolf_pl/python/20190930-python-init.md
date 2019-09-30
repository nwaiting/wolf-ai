## python - init
- **概述：**
>       本文主要介绍以下几个内容：
>           1、package的init
>           2、class类的__init__
>           3、__new__
>           4、super
>

- **__init__.py：**
>       目录中包含了 __init__.py 时，当用 import 导入该目录时，会执行 __init__.py 里面的代码
>
>       1、import mypackage 精确导入
>            __init__.py 在包被导入时会被执行
>       2、from mypackage import *  模糊导入
>           __all__ 变量就是干这个工作的
>

- **__init__(self)和__new__(cls)：**
>       __new__方法是静态方法，而__init__是实例方法。
> 
>       1、__new__是一个类方法，它返回的是一个实例
>       2、__init__是一个实例方法，它什么都不返回
>       3、只有在__new__方法返回一个cls对象时,__init__方法才会被调用，否则__init__方法不会被调用
>
>       new方法主要是当你继承一些不可变的class时(比如int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。还有就是实现自定义的metaclass。
>       new实现单例：
>           class Singleton(object):
>               def __new__(cls):
>                   # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
>                   if not hasattr(cls, 'instance'):
>                       cls.instance = super(Singleton, cls).__new__(cls)
>                   return cls.instance
>
>

- **super：**
>       在类的继承中，如果重定义某个方法，该方法会覆盖父类的同名方法，但有时，希望能同时实现父类的功能，这时，就需要调用父类的方法了，可通过使用 super 来实现
>       Animal 是父类，Dog 是子类，我们在 Dog 类重定义了 greet 方法，为了能同时实现父类的功能，我们又调用了父类的方法，如：
>       class Animal(object):
>           def greet(self):
>               print("Animal")
>       class Dog(object):
>           def greet(self):
>               super(Dog,self).greet()
>               print("Dog")
>       d = Dog()
>       print(d.__class__.mro())    #获取MRO列表
>       d.greet()
>       输出结果：
>           Animal
>           Dog
>

- **super的原理：**
>       在确保所有的父类的构造方法都使用了super（）函数的时候，就体现了super（）函数的智能性
>       super 其实和父类没有实质性的关联
>       对于你定义的每一个类，Python 会计算出一个方法解析顺序（Method Resolution Order, MRO）列表，它代表了类继承的顺序
>       那这个 MRO 列表的顺序是怎么定的呢，它是通过一个 C3 线性化算法来实现的。一个类的 MRO 列表就是合并所有父类的 MRO 列表
>       MRO 列表三条原则：
>           1、子类永远在父类前面
>           2、如果有多个父类，会根据它们在列表中的顺序被检查
>           3、如果对下一个类存在两个合法的选择，选择第一个父类
>
>       还有一点，父类抛异常的情况，如果子类有不抛异常的方法，异常就不抛出了
>       python2和python3的区别：
>           python2中使用：
>               super（开始类名，self）.函数名()
>           python3中使用：
>               super().函数名（）
>
>

- **待续：**
>       参考：https://www.cnblogs.com/silencestorm/p/8404046.html      python 中 super函数的使用
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
