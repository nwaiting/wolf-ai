#include <iostream>

class A
{
public:
    void fun_3(int k,int m)
    {
        cout<<k<<" "<<m<<endl;
    }
};

void fun(int x,int y,int z)
{
    cout<<x<<"  "<<y<<"  "<<z<<endl;
}

void fun_2(int &a,int &b)
{
    a++;
    b++;
    cout<<a<<"  "<<b<<endl;
}

int main(int argc, char const *argv[]) {
    auto f1 = std::bind(fun,1,2,3); //表示绑定函数 fun 的第一，二，三个参数值为： 1 2 3
    f1(); //print:1  2  3

    auto f2 = std::bind(fun, placeholders::_1,placeholders::_2,3);
    //表示绑定函数 fun 的第三个参数为 3，而fun 的第一，二个参数分别有调用 f2 的第一，二个参数指定
    f2(1,2);//print:1  2  3

    auto f3 = std::bind(fun,placeholders::_2,placeholders::_1,3);
    //表示绑定函数 fun 的第三个参数为 3，而fun 的第一，二个参数分别有调用 f3 的第二，一个参数指定
    //注意： f2  和  f3 的区别。
    f3(1,2);//print:2  1  3

    int n = 2;
    auto f4 = std::bind(fun_2, n,placeholders::_1); //表示绑定fun_2的第一个参数为n, fun_2的第二个参数由调用f4的第一个参数（_1）指定。
    f4(m); //print:3  4

    A a;
    /*
    在将一个R (T::*ptr)(Arg0,Arg1,...)形式的成员函数指针ptr用bind绑定参数时,bind的第一个绑定的参数是成员函数的调用者,随后跟随成员函数的参数绑定方式.
    例如bind(ptr,a,b,c)将会调用a.*ptr(b,c)。当采用_n常量将首参数与函数对象的参数相关联时,所生成的函数对象自动可接受T类型的引用及指针类型,无需再进行封装.
    但要想调用外部数据的成员函数,还需要用ref()、cref()来包装或者绑定一个对该变量的指针
    f5的类型为 function<void(int, int)>
    */
    auto f5 = std::bind(&A::fun_3, a,placeholders::_1,placeholders::_2); //使用auto关键字
    f5(10,20);//调用a.fun_3(10,20),print:10 20

    std::function<void(int,int)> fc = std::bind(&A::fun_3, a,std::placeholders::_1,std::placeholders::_2);
    fc(10,20);//调用a.fun_3(10,20) print:10 20

    return 0;
}
