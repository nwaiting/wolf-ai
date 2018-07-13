#include <iostream>
#include <stdint.h>
#include <map>
#include <vector>
#include <string>
using namespace std;

/*
    列出c++11的一些新特性
*/

/////////////第一部分 常规的语法///////////////

// 1、使用nullptr取代NULL，专门用于空指针
void func1()
{
    char *p = (char*)malloc(10);
    if (p == nullptr) {
        fprintf(stdout, "malloc false\n");
    }
    else {
        fprintf(stdout, "malloc success\n");
    }
}

/*
    2、constexpr（可能即将夭折）
    近似const，可以修饰变量，也可以修饰函数
    即可以用字面常量赋值，也可以用const变量赋值
    重点：
        constexpr修饰的函数，生效于编译时而不是运行时，重点应用于修饰函数使其在编译期大幅度被解释
        被constexpr修饰的函数，无论是普通函数还是类成员函数，必须是编译器可计算得到结果，即字面常量，不可是运行时才能获取的内容

        当类成员函数是用constexpr修饰时，构造函数必须用constexpr修饰

*/
const int global = 100;
void func2()
{
    int32_t temp = 10;
    //constexpr int32_t a = 1; //right
    //constexpr int32_t b = global; //right
    // constexpr int32_t c = temp; //error
}

/*
    3、using取代typedef    
*/
void func3()
{
    typedef double db; //c99
    using db = double; //c++11

    typedef void(*function)(int32_t, int32_t); //c99，函数指针类型定义
    using function = void(*)(int32_t, int32_t); //c++11，函数指针类型定义

    using kvpairs = std::map<int32_t, std::string>;  //c++11
    // template<T> using twins = std::pair<T, T>; //c++11用于模板 
}

/*
    4、使用auto、decltype
*/
void func4()
{
    auto a = 1;
    decltype(a) b = 2;
    fprintf(stdout, "b is %d\n", b);
}

/*
    5、字符串和数值类型的转换
    to_string：itoa函数称为历史
    stoi、stol、stoul、stoll、stoull、stof、stod、stold：atoX成为历史
*/
void func5()
{
    fprintf(stdout, "this is to_string %s\n", to_string(100).c_str());
}

/*
    6、生成随机数
    详情见random.cpp
*/
void func6()
{
    // random_device 
}

/*
    7、引用
    std::ref 应用
    std::cref const引用
    主要用于作为c++11函数式编程时传递的参数
*/
void func7()
{

}

/*
    8、时间管理
    std::chrono
*/
void func8()
{

}

/*
    9、正则表达式
    std::regex
*/
void func9()
{

}

/*
    10、断言static_assert
*/
void func10()
{

}


////////////第二部分 容器////////////
/*
    11、tuple & 花括号初始化
*/
void func11()
{

}

/*
    12、hash证实进入stl
    unordered_map、unordered_set、unordered_multimap、unordered_multiset
*/
void func12()
{

}

/*
    13、emplace
    作用于容器，区别于push、insert等，如push_back是在容器尾部追加一个容器类型对象，emplace_back是构造1个新对象并追加在容器尾部
*/
class A
{
public:
    A(int32_t a) :a_(a)
    {
    }
private:
    int32_t a_;
};
void func13()
{
    //c++ 98方法
    std::vector<A> vec;
    A a(100);
    vec.push_back(a);

    //c++11方法
    std::vector<A> vecc;
    vecc.emplace_back(100);
}

/*
    14、shrink_to_fit
    减少无意义的内存空间占用
    push、insert这类操作会触发容器的capacity变大，预留内存的扩大，实际中可能这些空间没用
*/
void func14()
{
    std::vector<int32_t> v{ 1, 2, 3, 4, 5 };
    fprintf(stdout, "memory %d\n", v.capacity());
    v.push_back(6);
    v.push_back(6);
    v.push_back(6);
    v.push_back(6);
    v.push_back(6);
    v.push_back(6);
    fprintf(stdout, "memory %d\n", v.capacity());
    v.shrink_to_fit();
    fprintf(stdout, "memory %d\n", v.capacity());
}


////////////第三部分 类/////////////////
/*
    15 类
        第一大类：
            1、default关键字生成默认构造函数和析构函数
            2、delete关键字禁止拷贝构造、复制构造、自定义参数的构造函数等
            3、委托构造函数
            4、移动构造函数（std::move()）
            减少内存赋值成本
            将不再需要的变量，取消它对原先持有变量（内存）的持有权限
            5、继承构造函数
        第二大类：
            1、override和final
                用于虚函数，更多的作用是显示的标识是否应该更多态继承或不应该
*/
class A11 {
    int data_;
public:
    A11() = default;
    ~A11() = default;
    A11(int _data) :data_(_data) {}
};

void func15()
{

}


/////////////第四部分 函数式编程/////////////////////////
/*
    16、lambda
    同python
*/
void func16()
{
    int32_t a = 1, b = 2;
    auto multi = [](int32_t _a, int32_t _b) {
        _b = _a * 3;
        return _a + _b;
    };

    fprintf(stdout, "multi %d\n", multi(a,b));
}

/*
    17、bind
    c++11风格的函数指针，绑定的函数，可以是普通函数，也可以是类成员函数
*/
void func17()
{
    auto f = [](int32_t _a, int32_t _b) {
        return _a + _b;
    };

    auto autof = std::bind(f, std::placeholders::_1, std::placeholders::_2);
    fprintf(stdout, "lambda %d\n", autof(10,20));
}

/*
    18、std::function
*/
void func18()
{

}

////////////第五部分 动态指针//////////////////
/*
    19、动态指针
        unique_ptr
        shared_ptr
*/
void func19()
{

}

/*
    20、多线程和互斥同步
        std::mutex
        std::unique_lock
        std::condition_variable
*/
void func20()
{

}



int main()
{
    //func1();

    //func4();

    //func5();

    //func14();

    func16();

    cin.get();
    return 0;
}
