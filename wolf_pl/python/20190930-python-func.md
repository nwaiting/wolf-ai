## python - func
- **概述：**
>
>
>
>
>
>
>
>

- **函数和方法区别：**
>       Function函数：
>           Function也是包含一个函数头和一个函数体, 也同样支持0到n个形参
>           函数是属于 FunctionObject
>       Method方法：
>           Method则是在function的基础上, 多了一层类的关系, 正因为这一层类, 所以区分了 function 和 method。
>           方法是属 PyMethodObject
>

- **Bound Method 和 Unbound Method：**
>       Bound method 多了一个实例绑定的过程
>       A.f 是 unbound method
>       a.f 是 bound method
>           方法的绑定, 肯定是伴随着class的实例化而发生,我们都知道, 在class里定义方法, 需要显示传入self参数, 因为这个self是代表即将被实例化的对象
>
>       PyMethodObject：
>           PyMethodObject 只会在你想要获取一个 bound-method 的时候创建, 而不是这个类实例化的时候创建
>
>       bound method：
>           classmethod方法绑定类对象
>           类中普通方法绑定实例对象
>
>

- **classmethod和staticmethod和常规方式：**
>       Python中3种方式定义类方法：
>           1、常规方式
>               普通的类方法需要通过self参数隐式的传递当前类对象的实例
>           2、@classmethod修饰方式
>               classmethod修饰的方法class_foo()需要通过cls参数传递当前类对象
>           3、@staticmethod修饰方式
>               staticmethod修饰的方法定义与普通函数是一样的
>
>       self和cls的区别不是强制的，只是PEP8中一种编程风格，slef通常用作实例方法的第一参数，cls通常用作类方法的第一参数。
>           即通常用self来传递当前类对象的实例，cls传递当前类对象。
>
>       1、staticmethod 不需要访问和类相关的属性或数据
>       2、classmethod 可以访问和类相关（不和实例相关)的属性
>
>

- **待续：**
>       参考：https://segmentfault.com/a/1190000009157792  Python: 函数与方法的区别 以及 Bound Method 和 Unbound Method
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
