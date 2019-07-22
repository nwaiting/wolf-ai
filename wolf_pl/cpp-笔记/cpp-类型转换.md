## cpp-笔记 - 类型转换
- **概述：**
>       c语言强制类型转换主要用于基础的数据类型间的转换：
>           (type-id)expression     //转换格式1
>           type-id(expression)     //转换格式2
>
>       c++除了能使用c语言的强制类型转换外，还新增了四种强制类型转换：
>           一、static_cast<new_type>      (expression)
>               1、用于类层次结构中基类（父类）和派生类（子类）之间指针或引用的转换。
>                   a、进行上行转换（把派生类的指针或引用转换成基类表示）是安全的；
>                   b、进行下行转换（把基类指针或引用转换成派生类表示）时，由于没有动态类型检查，所以是不安全的。
>               2、用于基本数据类型之间的转换，如把int转换成char，把int转换成enum。这种转换的安全性也要开发人员来保证。
>               3、把空指针转换成目标类型的空指针。
>               4、把任何类型的表达式转换成void类型。
>               注意：static_cast不能转换掉expression的const、volatile、或者__unaligned属性。
>           二、dynamic_cast<new_type>     (expression)
>               如果转换目标是引用类型并且失败了，则dynamic_cast运算符将抛出一个std::bad_cast异常(该异常定义在typeinfo标准库头文件中)
>               dynamic_cast主要用于类层次间的上行转换和下行转换，还可以用于类之间的交叉转换（cross cast）
>               在类层次间进行上行转换时，dynamic_cast和static_cast的效果是一样的
>               在进行下行转换时，dynamic_cast具有类型检查的功能，比static_cast更安全。dynamic_cast是唯一无法由旧式语法执行的动作，也是唯一可能耗费重大运行成本的转型动作。
>               1、指针类型
>               2、引用类型
>           三、const_cast<new_type>       (expression)
>               const_cast，用于修改类型的const或volatile属性。
>               该运算符用来修改类型的const(唯一有此能力的C++-style转型操作符)或volatile属性。除了const 或volatile修饰之外， new_type和expression的类型是一样的。
>               1、常量指针被转化成非常量的指针，并且仍然指向原来的对象
>               2、常量引用被转换成非常量的引用，并且仍然指向原来的对象
>               3、const_cast一般用于修改底指针。如const char *p形式
>           四、reinterpret_cast<new_type> (expression)
>               new_type必须是一个指针、引用、算术类型、函数指针或者成员指针。
>               它可以把一个指针转换成一个整数，也可以把一个整数转换成一个指针（先把一个指针转换成一个整数，再把该整数转换成原类型的指针，还可以得到原先的指针值）。
>               reinterpret_cast意图执行低级转型，实际动作（及结果）可能取决于编辑器，这也就表示它不可移植。
>               举一个错误使用reintepret_cast例子，将整数类型转换成函数指针后，vc++在执行过程中会报"...中的 0xxxxxxxxx 处有未经处理的异常: 0xC0000005: Access violation"错误，
>                   如：
>                   int p = 10;
>                   test_func fun2 = reinterpret_cast<test_func>(&p);
>                   fun2(p);    //...处有未经处理的异常: 0xC0000005: Access violation
>               IBM的C++指南、C++之父Bjarne Stroustrup的FAQ网页和MSDN的Visual C++也都指出：错误的使用reinterpret_cast很容易导致程序的不安全，
>                   只有将转换后的类型值转换回到其原始类型，这样才是正确使用reinterpret_cast方式。
>
>           备注：new_type为目标数据类型，expression为原始数据类型变量或者表达式。
>           static_cast和reinterpret_cast的区别主要在于多重继承：
>               如：
>                   class A {
>                        public:
>                        int m_a;
>                    };
>
>                    class B {
>                        public:
>                        int m_b;
>                    };
>
>                   class C : public A, public B {};
>                   C c;
>                   printf("%p, %p, %p", &c, reinterpret_cast<B*>(&c), static_cast <B*>(&c));
>               解释：
>                   前两个的输出值是相同的，最后一个则会在原基础上偏移4个字节，这是因为static_cast计算了父子类指针转换的偏移量，
>                   并将之转换到正确的地址（c里面有m_a,m_b，转换为B*指针后指到m_b处），而reinterpret_cast却不会做这一层转换。
>
>
>       《Effective C++》中将c语言强制类型转换称为旧式转型，c++强制类型转换称为新式转型
>
>       注意：
>           1、新式转换较旧式转换更受欢迎。原因有二，
>               一是新式转型较易辨别，能简化“找出类型系统在哪个地方被破坏”的过程；
>               二是各转型动作的目标愈窄化，编译器愈能诊断出错误的运用。
>           2、尽量少使用转型操作，尤其是dynamic_cast，耗时较高，会导致性能的下降，尽量使用其他方法替代
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
>
