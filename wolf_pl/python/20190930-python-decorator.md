## python - decorator
- **概述：**
>       总述：
>           python装饰器就是用于拓展原来函数功能的一种函数，这个函数的特殊之处在于它的返回值也是一个函数，使用python装饰器的好处就是在不用更改原函数的代码前提下给函数增加新的功能。
>
>
>
>
>
>
>

- **内置装饰器：**
>       Python中有三个内置的装饰器，都是跟class相关的：
>           1、staticmethod
>               类静态方法，其跟成员方法的区别是没有 self 参数，并且可以在类不进行实例化的情况下调用
>           2、classmethod
>               与成员方法的区别在于所接收的第一个参数不是 self （类实例的指针），而是cls（当前类的具体类型）
>           3、property
>               表示可以通过通过类实例直接访问的信息（类实例直接访问的信息）
>
>       例如：
>           class Foo(object):
>               @property
>               def var(self):
>                   return self.val_
>               @var.setter
>               def var(self,var):
>                   self.val_ = var
> 
>       解释：
>           1、对于Python新式类（new-style class），如果将上面的 “@var.setter” 装饰器所装饰的成员函数去掉，则Foo.var 属性为只读属性，使用 “foo.var = ‘var 2′” 进行赋值时会抛出异常。
>           2、对于Python classic class，所声明的属性不是 read-only的，所以即使去掉”@var.setter”装饰器也不会报错
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
>
>
>
>
>
>
>
