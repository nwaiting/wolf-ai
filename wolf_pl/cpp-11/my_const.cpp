#include <iostream>


/*
    常引用：
        既要利用引用提高程序的效率，又要保护传递给函数的数据不在函数中被改变，就应使用常引用
        常引用声明方式：
            const 类型标识符 &引用名=目标变量名
    临时对象都是const类型的。因此上面的表达式就是试图将一个const类型的对象转换为非const类型，这是非法的。引用型参数应该在能被定义为const的情况下，尽量定义为const
    如何理解临时对象都是const类型的？
    解析：
        非const的引用参数只能是相同类型，const的引用参数可以传相关类型的参数进来，加上const才能接受"右值(right value)"引用
        如：class A {};
            class B{
                public:
                B(A& a){}
            }；
            class B1: public B {
                public:
                B1(const B& b) : B(b){}  //隐式转换生成的临时对象都是const的
                //当把const去掉就会编译报错，会进行自动类型转换
                //B(A& a){} 不但是一个构造函数，而且是一个自定义的类型转换操作(A->B)，如果要去掉这种非有意的自定义类型转换，使用 explicit B(A& a){}
                //B(A& a){}是一个隐式的类型转换函数，当执行B1 b1(a)时会自动调用这个函数将a转换成B类型的临时对象b。这种系统自动生成的临时对象都是const的，而const对象是无法转换成非const对象的，所以B1(const B& b):B(b)这里一定要加const
            }
            A a;
            B b(a);
            B1 b1(a);

        如：
            string foo( );
            void bar(string & s);

            下面是非法的：
                bar(foo( ));
                bar("hello world");
                解析：
                    原因在于 foo( ) 和 "hello world" 串都会产生一个临时对象，而在 C++ 中，这些临时对象都是const 类型的。
                    因此上面的表达式就是试图将一个 const 类型的对象转换为非 const 类型，这是非法的。引用型参数应该在能被定义为 const 的情况下，尽量定义为const的。

            一个非const引用，只能引用与其类型完全相同的对象，或者是其派生类的对象
            const引用类型的隐式转换：
                一个const引用满足非const引用的特性的同时，还有很重要的一点，const引用可以引用一个与其类型完全不相同的类型(因为编译器会生成一个转换后可引用的临时对象)，
                前提是被引用的类型可以转换为引用的类型(编译器自定义的类型提升，或者是用户自定义的类型转换
            为什么在const引用情况下，编译器会生成一个可被引用的临时对象？
                解析：用一个const引用来操作这个临时对象，所以，这个临时对象的状态是不会变的，也就是安全的(当然，如果你把const引用const_cast成一个非const引用来操作这个编译器生成的临时对象，那么结果是未定义的).
            const &是可以重新构造临时对象，非const &不可以，如果编译器不设这个限制，那么将有十分古怪的结果发生，会发生编译器自己构造一个对象，对它进生一系列复杂的操作之后扔掉，这一般不是程序员要做的事。
                因此，c++一般规定，编译器自行构造的临时对象一定是const的。

    “引用”作为函数返回值：
        类型标识符 &函数名（形参列表及类型说明）{ //函数体 }
        好处：
            在内存中不产生被返回值的副本；（注意：正是因为这点原因，所以返回一个局部变量的引用是不可取的。因为随着该局部变量生存期的结束，相应的引用也会失效，产生runtime error!
        1、不能返回局部变量的引用
        2、不能返回函数内部new分配的内存的引用
            被函数返回的引用只是作为一个临时变量出现，而没有被赋予一个实际的变量，那么这个引用所指向的空间（由new分配）就无法释放，造成memory leak
        3、可以返回类成员的引用，但最好是const
        4、流操作符重载返回值申明为“引用”的作用
        5、在另外的一些操作符中，却千万不能返回引用：+ - * / 四则运算符

    结构和联合区别：
        1、结构和联合都是由多个不同的数据类型成员组成, 但在任何同一时刻, 联合中只存放了一个被选中的成员（所有成员共用一块地址空间）, 而结构的所有成员都存在（不同成员的存放地址不同）
        2、对于联合的不同成员赋值, 将会对其它成员重写, 原来成员的值就不存在了, 而对于结构的不同成员赋值是互不影响的
        验证大端和小端：
        union U{
            short a;
            char c;
        };
        U u;
        u.a=0x1234; //只要我们取出变量c的值，进行比对；若其值为34h（低字节保存在低地址中），则机器为小端模式（数据的高字节保存在内存的高地址中），若其值为12h，则机器为大端模式。

    哪几种情况只能用intialization list 而不能用assignment?
        当类中含有const、reference 成员变量；基类的构造函数都需要初始化表

    C++是不是类型安全的？
        不是。两个不同类型的指针之间可以强制转换（用reinterpret_cast)。C#是类型安全的。

    main 函数执行以前，还会执行什么代码？
        全局对象的构造函数会在main 函数之前执行，atexit函数在main函数返回之后
        操作系统装载程序之后，首先运行的代码并不是main的第一行，而是某些特别的代码，这些代码准备好main函数执行所需要的环境，并且负责调用main函数，这时候你才可以再main函数里放心大胆的写各种代码：申请内存、使用系统调用、触发异常、访问IO。
        在main函数返回之后，他会记录main函数的返回值，调用atexit注册的函数，然后结束进程。

    描述内存分配方式以及它们的区别?
        1、从静态存储区域分配
            内存在程序编译的时候就已经分配好，这块内存在程序的整个运行期间都存在。例如全局变量，static 变量
        2、在栈上创建
        3、从堆上分配

    const与#define 相比，有何优点？
        const作用：
            const作用：定义常量、修饰函数参数、修饰函数返回值三个作用。
            被Const修饰的东西都受到强制保护，可以预防意外的变动，能提高程序的健壮性。
        const 常量有数据类型，而宏常量没有数据类型。编译器可以对前者进行类型安全检查。而对后者只进行字符替换，没有类型安全检查，并且在字符替换可能会产生意料不到的错误

    数组与指针的区别？
        1、数组要么在静态存储区被创建（如全局数组），要么在栈上被创建。指针可以随时指向任意类型的内存块。
        2、用运算符sizeof 可以计算出数组的容量（字节数）。sizeof(p),p 为指针得到的是一个指针变量的字节数，而不是p 所指的内存容量。
            C++/C 语言没有办法知道指针所指的内存容量，除非在申请内存时记住它。注意当数组作为函数的参数进行传递时，该数组自动退化为同类型的指针。

    一个空类，编译器也会默认生成4个成员函数：默认构造函数，析构函数，拷贝构造函数，赋值函数
    vector中的push_back问题：
        push_back这个函数会对传递进来的参数进行一次拷贝（调用拷贝构造函数），并将其添加到vector中。
        如果对象没有拷贝构造函数，编译器会为其生成一个，但是这个编译器生成的拷贝构造函数只是进行了一次浅拷贝，
        CDemo d1;
        d1.str=new char[32];
        strcpy(d1.str,"trend micro");
        vector<CDemo> * a1=new vector<CDemo>;
        a1->push_back(d1);
        delete a1;
        本例中就是只是复制了str的值，也就是"strend micro"的地址，即拷贝后的对象和原对象的str都是指向同一块内存区域，但是这个拷贝的对象和原对象的析构函数又都会执行，这里就会delete两次

    栈内存与文字常量区?
            char str1[] = "abc";
        　　char str2[] = "abc";
            //str1 != str2

        　　const char str3[] = "abc";
        　　const char str4[] = "abc";
            // str3 != str4

        　　const char *str5 = "abc";
        　　const char *str6 = "abc";
            // str5 == str6

        　　char *str7 = "abc";
        　　char *str8 = "abc";
            // str7 == str8
        str1,str2,str3,str4是数组变量，它们有各自的内存空间；而str5,str6,str7,str8是指针，它们指向相同的常量区域

    将程序跳转到指定内存地址？
        要对绝对地址0x100000赋值，我们可以用(unsigned int*)0x100000 = 1234;那么要是想让程序跳转到绝对地址是0x100000去执行，应该怎么做？
        首先要将0x100000强制转换成函数指针,然后再调用它
            typedef void(*)() voidFuncPtr;
            *((voidFuncPtr)0x100000)();

    int id[sizeof(unsigned long)];这个对吗？
        正确 这个 sizeof是编译时运算符，编译时就确定了  ,可以看成和机器有关的常量

    引用与指针有什么区别？
        1) 引用必须被初始化，指针不必。
        2) 引用初始化以后不能被改变，指针可以改变所指的对象。
        3) 不存在指向空值的引用，但是存在指向空值的指针。

    全局变量和局部变量有什么区别？是怎么实现的？操作系统和编译器是怎么知道的？
        使用方式不同：通过声明后全局变量程序的各个部分都可以用到；局部变量只能在局部使用；分配在栈区。
        操作系统和编译器通过内存分配的位置来知道的，全局变量分配在全局数据段并且在程序开始运行的时候被加载。局部变量则分配在堆栈里面 。

    如何判断一段程序是由C 编译程序还是由C++编译程序编译的？
        #ifdef __cplusplus
            cout<<“c++";
        #endif

    C++写个程序，如何判断一个操作系统是16位还是32位的？
        定义一个指针p，打印出sizeof(p),如果节后是4，则表示该操作系统是32位，打印结果是2，表示是16位。
        1、利用sizeof
            可以使用sizeof计算int的字节长度来判断是32位还是16位。
            32位机器下：sizeof(int) = 4；16位机器下：sizeof(int) = 2
            但是实际中可能64位的机器sizeof(int)也是4字节，因为很多时候是编译器决定要占用几个字节
        2、利用最大值
            机器位数不同则表示的数字的最大值是不同的。
            32位机器下int的最大值为2147483647，16位机器下int的最大值是32767
            我们可以利用最大值是否溢出情况来判断
                定义一个变量num赋值32768，如果是16位机器这个时候超过了int最大值变成了-32768，如果是32位机器不会超过
        3、对0取反
            32位机器下无符号整型的数值范围是[0，4294967295]，16位机器下无符号整型的范围是[0，65535]
            0的二进制是所有位都是0
                32位下对0取反的结果是所有位都是1，如果把这个数赋值给一个无符号整型变量num，则num值为4294967295
                16位下对0取反的结果是所有位都是1，如果把这个数赋值给一个无符号整型变量num，则num值为65535
            利用对0取反后的结果赋值给无符号整型变量来判断值是否大于65535即可

    多态类中的虚函数表是 Compile-Time，还是 Run-Time 时建立的？
        虚拟函数表是在编译期就建立了,各个虚拟函数这时被组织成了一个虚拟函数的入口地址的数组。
        而对象的隐藏成员--虚拟函数表指针是在运行期--也就是构造函数被调用时进行初始化的,这是实现多态的关键。

    float a,b,c , 问等式 (a+b)+c==(b+a)+c 和 (a+b)+c==(a+c)+b 能否成立？
        两者都不行。在比较float或double时，不能简单地比较。

    重复多次 fclose 一个打开过一次的 FILE *fp 指针会有什么结果？
        导致文件描述符结构中指针指向的内存被重复释放，进而导致一些不可预期的异常

    是不是一个父类写了一个virtual 函数，如果子类覆盖它的函数不加virtual ,也能实现多态?
        virtual修饰符会被隐形继承的。virtual可加可不加。子类的空间里有父类的所有变量(static除外)。
        子类覆盖它的函数不加virtual ,也能实现多态。在子类的空间里，有父类的私有变量。私有变量不能直接访问。

    多态的作用？
        1、隐藏实现细节，使得代码能够模块化；扩展代码模块，实现代码重用；
        2、接口重用：为了类在继承和派生的时候，保证使用家族中任一类的实例的某一属性时的正确调用

    当一个类A 中没有声命任何成员变量与成员函数,这时sizeof(A)的值是多少？
        sizeof(A) = 1；
        编译器不允许一个类的大小为0，会为它分配1字节的内存。试想，若，不这样做，那2个类A的实例在内存中将会无法区分
        一个空类对象的大小是1byte。这是被编译器安插进去的一个字节，这样就使得这个空类的两个实例得以在内存中配置独一无二的地址

     C++里面是不是所有的动作都是main()引起的？
        比如全局变量的初始化，就不是由 main 函数引起的。

    内联函数在编译时是否做参数类型检查？
        内联函数要做参数类型检查，这是内联函数跟宏相比的优势。

    在 C++的一个类中声明一个 static 成员变量有没有用？
        在C++类的成员变量被声明为 static（称为静态成员变量），意味着它为该类的所有实例所共享，也就是说当某个类的实例修改了该静态成员变量，也就是说不管创建多少对象，static修饰的变量只占有一块内存。
        其修改值为该类的其它所有实例所见；而类的静态成员函数也只能访问静态成员（变量或函数）。static是加了访问控制的全局变量，不被继承。

    函数模板与类模板有什么区别？
        函数模板的实例化是由编译程序在处理函数调用时自动完成的
        而类模板的实例化必须由程序员在程序中显式地指定

    函数重载，我们靠什么来区分调用的那个函数？靠返回值判断可以不可以？
        问题是在 C++/C 程序中，我们可以忽略函数的返回值。在这种情况下，编译器和程序员都不知道哪个 Function 函数被调用。

    所有的运算符都能重载吗？
        不能被重载的运算符
        1、不能改变 C++内部数据类型（如 int,float 等）的运算符
        2、不能重载‘.’，因为‘.’在类中对任何成员都有意义，已经成为标准用法

    基类的析构函数不是虚函数，会带来什么问题？
        派生类的析构函数用不上，会造成资源的泄漏

    There are two int variables: a and b, don't use“if”, “? :”, “switch”or other judgement statements, find out the biggest one of the two numbers？
        ( ( a + b ) + abs( a - b ) ) / 2

    在不用第三方参数的情况下，交换两个参数的值。
        a = a + b;
        b = a – b;
        a = a – b;

    写一个能做左值的函数(方法有很多)
        max(x, y) += 2874 + 55;
        int &max(int & x, int & y) {
                return x > y? x : y;
            }

    三元表达式“？:”问号后面的两个操作数必须为同一类型
        cout << (true?1:"1") << endl;   //错误

    数组长度定义：
        而数组定义要求长度必须为编译期常量

    默认构造函数调用带参构造函数可以吗？
        不能。在默认构造函数内部再调用带参的构造函数属用户行为而非编译器行为，亦即仅执行函数调用，而不会执行其后的初始化表达式。
        只有在生成对象时，初始化表达式才会随相应的构造函数一起调用。

    一个栈的入栈序列为ABCDEF，则不可能的出栈序列是：
        该题主要是考虑栈的核心思想是先进后出，并且需要注意入栈和出栈的顺序是未知的，例如你可以先入栈ABCD，然后出栈D，然后入栈E，出栈E，入栈F，出栈F，然后CBA依次出栈，也就是DEFCBA的情况。
        任何出栈的元素后面出栈的元素必须满足以下三点：
            1、在原序列中相对位置比它小的，必须是逆序；
            2、在原序列中相对位置比它大的，顺序没有要求；
            3、以上两点可以间插进行。

    写出判断ABCD四个表达式的是否正确：
        int a = 4;
        (a++) += a; //错误
        左侧不是一个有效变量，不能赋值，可改为 (++a) += a;

    return语句效率：
        1、return String(s1 + s2);
        2、String temp(s1 + s2); return temp;
        解释：
            1、这是临时对象的语法，表示“创建一个临时对象并返回它”
            2、首先，temp 对象被创建，
                同时完成初始化；
                然后拷贝构造函数把 temp 拷贝到保存返回值的外部存储单元中；
                最后，temp 在函数结束时被销毁（调用析构函数）
            然而“创建一个临时对象并返回它”的过程是不同的，编译器直接把临时对象创建并初始化在外部存储单元中，省去了拷贝和析构的化费，提高了效率。

    int max( int *ia, int sz ); 和 int max( int *, int b= 10 ); 算函数重载？还是重复声明？
        如果在两个函数的参数表中只有缺省实参不同则第二个声明被视为第一个的重复声明 。

    int a;  //数字递增变换范围 0 -> ... -> 2147483647 -> -2147483648 -> -2147483647 -> -2147483646 -> ...
    unsigned int a;     //数字递增变化范围 0 -> ... 4294967295 -> 0 -> 1 > ...
    https://blog.csdn.net/guotianqing/article/details/77341657  c语言中 char* 和 unsigned char* 的区别浅析         

    c++初始化列表：
        初始化列表位于函数参数表后，函数体前，故列表的初始化工作发生在函数体内代码之前。列表中各量的初始化顺序与变量在类中定义的顺序相同，与排列顺序无关
        初始化列表的使用规则如下：
            1、若类存在继承关系，派生类必须在初始化列表中调用基类的构造函数
            2、类的const常量，成员为引用类型只能在初始化列表中初始化，不能在函数体内赋值
            3、类的数据成员可以采用初始化列表和函数体赋值两种方式
                对于非内部数据类型成员对象应采用初始化列表方式，这样效率更高；
                对于内部数据类型，两种方式效率相同，但用赋值方式更清晰；
            4、类成员为没有默认构造函数的类类型，因为使用初始化列表可以不必调用默认构造函数来初始化，而是直接调用拷贝构造函数初始化

    C++变量的初始化顺序：
        1、基类的静态变量或全局变量
        2、派生类的静态变量或全局变量
        3、基类的成员变量
        4、派生类的成员变量

    初始化顺序：
        1、成员变量在使用初始化列表初始化时，与构造函数中初始化成员列表的顺序无关，只与定义成员变量的顺序有关。因为成员变量的初始化次序是根据变量在内存中次序有关，而内存中的排列顺序早在编译期就根据变量的定义次序决定了
        2、如果不使用初始化列表初始化，在构造函数内初始化时，此时与成员变量在构造函数中的位置有关
        3、注意：类成员在定义时，是不能初始化的
        4、注意：类中const成员常量必须在构造函数初始化列表中初始化
        5、注意：类中static成员变量，必须在类外初始化
        6、静态变量进行初始化顺序是基类的静态变量先初始化，然后是它的派生类。直到所有的静态变量都被初始化。这里需要注意全局变量和静态变量的初始化是不分次序的。
            这也不难理解，其实静态变量和全局变量都被放在公共内存区。可以把静态变量理解为带有“作用域”的全局变量。
            在一切初始化工作结束后，main函数会被调用，如果某个类的构造函数被执行，那么首先基类的成员变量会被初始化


    c++派生类：
        1、在派生类中实现类的基本函数
            基类与派生类的析构函数应为虚函数
            在编写派生类的赋值函数时，要将基类的数据成员重新赋值，若基类的数据成员私有，可以调用基类的赋值函数；
            当基类构造函数要传递参数才能初始化时，派生类必须显式定义构造函数，为基类传参数


    const来提高函数的健壮性：
        const修饰函数的返回值。若返回值是const修饰的指针，则！！指针内容！！不能改变，返回值只能赋给加const修饰的同类型指针；若返回值是值传递，不用const
        而c++中，一个const不是必需创建内存空间，而在c中，一个const总是需要一块内存空间。
        在c++中是否要为const全局变量分配内存空间，取决于这个const变量的用途，如果是充当着一个值替换（即就是将一个变量名替换为一个值），那么就不分配内存空间，不过当对这个const全局变量取地址或者使用extern时，会分配内存，存储在只读数据段。也是不能修改的。
        在c中和c++中区别：
            1、对于基础数据类型，也就是const int a = 10这种，编译器会把它放到符号表中，不分配内存，当对其取地址时，会分配内存（符号表）
            2、对于基础数据类型，如果用一个变量初始化const变量，如果const int a = b,那么也是会给a分配内存
            3、对于自定数据类型，比如类对象，那么也会分配内存。
            4、c中const默认为外部连接，c++中const默认为内部连接.当c语言两个文件中都有const int a的时候，编译器会报重定义的错误。而在c++中，则不会，因为c++中的const默认是内部连接的。如果想让c++中的const具有外部连接，必须显示声明为: extern const int a = 10。

    程序效率：
        时间效率是指运行速度，空间效率是指程序占用的内存或外存状况。全局效率指从操作系统的角度考虑的效率；局部效率指从模块或函数角度上考虑的效率。
        提高程序的全局效率为主，局部效率为辅
        先优化数据结构和算法，再处理程序代码
        不要追求紧凑的代码，因为这并不能产生高效的机器码

    dynamic_cast：
        https://www.cnblogs.com/bastard/archive/2011/12/14/2288117.html
        子类转换成基类，可以直接转换，不是多态类型不能转换的情况（基类到子类的继承关系、兄弟关系、没有关系）
        只用于对象、指针和引用，主要用于执行安全的向下转型。当用于多态类型时，它允许任意的隐式类型转换及相反的过程，但在反向转型时会检查操作是否有效，这种检测在运行时进行，若检测不是有效的对象指针，返回NULL
        安全的基类和子类之间转换、必须要有虚函数、相同基类不同子类之间的交叉转换，但结果是NULL
        1、继承关系的类指针对象或引用之间转换（非引用不行和指针不行）
        2、基类指针转换为子类指针，并不是每一次都有效：只有基类指针本身指向的是一个派生类的对象，然后将此基类指针转换为对应的派生类指针才是有效的。
    static_cast：
        允许执行任意的隐式转换和相反的动作。应用在类指针上，父类指针和子类指针可以相互转换，转换过程中不检查。但是不能将const转化为非const；
        static_cast不能进行无关类型(如非基类和子类)指针之间的转换，不能进行无关指针类型之间的转换
        基本数据类型转换。enum, struct, int, char, float等。
        把空指针转换成目标类型的空指针，把任何类型的表达式转换成void类型
    const_cast：
        用来强制设置对象的常量性或移除
    reinterpret_cast：
        可转换一种类型的指针为其它类型的指针，也可以将指针转换为其它类型。非相关类型间的转换，不对操作内容进行检查。
        仅仅重新解释类型，但没有进行二进制的转换
        转换的类型必须是一个指针、引用、算术类型、函数指针或者成员指针，最普通的用途就是在函数指针类型之间进行转换
    总结：
        基本类型转换用static_cast、多态类之间的类型转换用daynamic_cast、不同类型的指针类型转换用reinterpreter_cast

    static:
        未加static前缀的全局变量和函数都具有全局可见性，其它的源文件也能访问，全局变量名或者函数名前加static，就会对其它源文件隐藏。
            利用这一特性可以在不同的文件中定义同名函数和同名变量，而不必担心命名冲突。
        存储在静态数据区的变量会在程序刚开始运行时就完成初始化，也是唯一的一次初始化。共有两种变量存储在静态存储区：全局变量和static变量。
        未经初始化的全局静态变量、局部静态变量会被程序自动初始化为0

    static const的使用：
        如  class A {
                const static int num1; // 声明（并未定义）
                const static int num2 = 13; // 声明和初始化（并未定义）
                };
            const int A::num1 = 12; // 定义并初始化
            const int num2;  // 定义
        参考： https://www.cnblogs.com/xiezhw3/p/4354601.html


    malloc和new的区别：
        1、new如果分配失败了会抛出bad_malloc的异常，而malloc失败了会返回NULL。因此对于new，正确的姿势是采用try…catch语法，而malloc则应该判断指针的返回值。为了兼容很多c程序员的习惯，C++也可以采用new nothrow的方法禁止抛出异常而返回NULL；

    析构函数能抛出异常吗 ？
        C++标准指明析构函数不能、也不应该抛出异常。
        C++异常处理模型最大的特点和优势就是对C++中的面向对象提供了最强大的无缝支持。那么如果对象在运行期间出现了异常，
            C++异常处理模型有责任清除那些由于出现异常所导致的已经失效了的对象(也即对象超出了它原来的作用域)，并释放对象原来所分配的资源， 这就是调用这些对象的析构函数来完成释放资源的任务，所以从这个意义上说，析构函数已经变成了异常处理的一部分。

    构造函数和析构函数中调用虚函数吗？
        绝对不要在构造函数和析构函数中调用虚函数，他们都不是动态绑定的。
        因为析构函数本身如果是虚函数的，在执行虚函数之前会通过vptr找到正确的析构函数，然而在那个析构函数调用的虚函数依旧是没有动态绑定。我们看到的"动态绑定"是虚析构函数的动态绑定，而不是析构函数所调用的虚函数的多态

    构造函数使用列表初始化还是用赋值方法，效率对比？
        构造函数列表初始化对象或者成员变量的方式只调用了一次copy construction，相比使用构造函数内部的opetaror= 这样的赋值方式给成员变量或对象赋值效率要高，因为这样的方法多调用了一次 default construct函数

    const和mutable作用：
        保护类的成员变量不在成员函数中被修改，是为了保证模型的逻辑正确，通过用const关键字来避免在函数中错误的修改了类对象的状态。
        并且在所有使用该成员函数的地方都可以更准确的预测到使用该成员函数的带来的影响。而mutable则是为了能突破const的封锁线，
        让类的一些次要的或者是辅助性的成员变量随时可以被更改。没有使用const和mutable关键字当然没有错，
        const和mutable关键字只是给了建模工具更多的设计约束和设计灵活性，而且程序员也可以把更多的逻辑检查问题交给编译器和建模工具去做，从而减轻程序员的负担

    mutable：
        mutable是为了突破const的限制而设置的。
        被mutable修饰的变量，将永远处于可变的状态，即使在一个const函数中，甚至结构体变量或者类对象为const，其mutable成员也可以被修改。
        mutable在类中只能够修饰非静态数据成员。
        有些时候，需要在const的函数里面修改一些跟类状态无关的数据成员，那么这个数据成员就应该被mutalbe来修饰。
        mutable的承诺是如果某个变量被其修饰，那么这个变量将永远处于可变的状态，即使在一个const函数中。这与const形成了一个对称的定义，一个永远不变，而另外一个是永远可变
    const:
        const承诺的是一旦某个变量被其修饰，那么只要不使用强制转换(const_cast)，在任何情况下该变量的值都不会被改变，无论有意还是无意，而被const修饰的函数也一样，
        一旦某个函数被const修饰，那么它便不能直接或间接改变任何函数体以外的变量的值，即使是调用一个可能造成这种改变的函数都不行。这种承诺在语法上也作出严格的保证，任何可能违反这种承诺的行为都会被编译器检查出来
    volatile：
        volatile原意是“易变的”，但这种解释简直有点误导人，应该解释为“直接存取原始内存地址”比较合适
        象const一样，volatile是一个类型修饰符。volatile修饰的数据,编译器不可对其进行执行期寄存于寄存器的优化。
        这种特性,是为了满足多线程同步、中断、硬件编程等特殊需要。遇到这个关键字声明的变量，编译器对访问该变量的代码就不再进行优化，从而可以提供对特殊地址的直接访问。
        使用场景：
            1、中断服务程序中修改的供其它程序检测的变量需要加volatile；
            2、多任务环境下各任务间共享的标志应该加volatile；
            3、存储器映射的硬件寄存器通常也要加volatile说明，因为每次对它的读写都可能有不同意义；
    explicit：
        C++中的 explicit关键字主要是用来修饰类的构造函数，表明该构造函数是显式的，禁止单参数构造函数的隐式转换，不允许隐式转换
        也就是说如果一个类的构造函数只有一个参数，那么就可以从这个参数的类型隐式的转换为类类型，这种隐式转换有一定的限制，就是只能转换一次。！！！
        explicit关键字的作用就是防止类构造函数的隐式自动转换，explicit关键字在类构造函数参数大于或等于两个时无效












*/


int main(int argc, char const *argv[]) {
    /* code */
    return 0;
}
