#include <iostream>
#include <stdint.h>
#include <map>
#include <vector>
#include <string>
#include <functional> //std::bind
#include <cmath>
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


/*
    移动构造函数：
        属于c++11的右值引用的衍生效果之一
        std::move主要解决拷贝性能问题
        类似于python的深拷贝和浅拷贝，python中的对象赋值和copy.copy都是浅拷贝，赋值的都是对象的引用，copy.deepcopy则是深拷贝
        
        python赋值：
            对象的赋值其实就是对象的引用。当创建一个对象，把它赋值给另一个变量的时候，python并没有拷贝这个对象，只是拷贝了这个对象的引用而已。
        深拷贝：
            外围和内部元素都进行了拷贝对象本身，而不是引用。也就是，把对象复制一遍，并且该对象中引用的其他对象我也复制。
        浅拷贝：
            拷贝了最外围的对象本身，内部的元素都只是拷贝了一个引用而已。也就是，把对象复制一遍，但是该对象中引用的其他对象我不复制

        std::move：
            std::move解决的问题是一个赋值效率的问题
            如对临时变量（函数中的参数）的复制，通过更改对象的所有者(move)，实现免内存搬迁和拷贝（去除深拷贝）
            提高"复制"效率（其实不是复制，仅是更改了对象的所有者）
*/

class TestMove
{
public:
    std::vector<std::string> v_;
    TestMove(std::vector<std::string> &tmp) {
        for (auto& it:tmp) {
            v_.push_back(std::move(it));
        }
    }
};

//std::move使用
//仅仅是简单地将左值转换为右值，它本身并没有转移任何东西，仅仅是让对象可以转移
void func15()
{
    //方法1
    std::string aaa = "123"; //或std::string &&aaa = "123"; 显示的标识aaa是全局字符串的右值引用
    //右值"123"，它的所有者将从原来的左值(变量std::string a),转移到新的左值(std::vector v)
    //所以，使用std::move时一定要保证，以前的左值不再真需要了，典型使用场合就是：（构造）函数的参数，避免了再复制
    std::vector<std::string> v;
    v.push_back(std::move(aaa));
    //因为全局字符串"123"已经从最开始的变量a转移到了v
    fprintf(stdout, "move f1 %s\n", aaa.c_str());


    //方法2
    //移动构造函数
    //最大的用途就是避免同一份内存数据的不必要的变成两份甚至多份、过程中的变量传递导致的内存复制，另外解除了栈变量对内存的引用
    std::vector<std::string>  temp_vec = {"123", "234", "345", "456"};
    fprintf(stdout, "temp_vec size %d\n", temp_vec.size());
    for (auto i:temp_vec) {
        fprintf(stdout, "%s ", i.c_str()); 
    }
    fprintf(stdout, "\n");
    TestMove tm(temp_vec);
    //执行了move后，temp_vec的元素还是4个，但是每个元素是空的，没有内容
    fprintf(stdout, "after move, temp_vec size %d\n", temp_vec.size());
    for (auto i : temp_vec) {
        fprintf(stdout, "%s ", i.c_str());
    }
    fprintf(stdout, "\n");

    //方法3
    //c++11风格的新老容器的数据转移
    //如果一个老容器如vector容器oldv，需要将其内部数据复制到新容器vector的newv，且老容器后面无用，数据量很大
    //c++11的std::make_move_iterator将派上用场，可以将一个普通的迭代器，如oldv.begin(),转化为move迭代器，配合std::copy，将老容器内全部数据的引用，
    //move到新容器同时取消老容器对数据的持有权，这就是c++11风格的告诉数据拷贝
    std::vector<std::string> oldv = { "1111", "2222", "3333", "4444" };
    std::vector<std::string> newv(oldv.size());
    fprintf(stdout, "before make_move_iterator\n");
    for (auto &i:oldv) {
        fprintf(stdout, "%s ", i.c_str());
    }
    fprintf(stdout, "\n");

    //传统做法，赋值
    //std::copy(oldv.begin(), oldv.end(), newv.begin());
    std::copy(std::make_move_iterator(oldv.begin()), std::make_move_iterator(oldv.end()), newv.begin());
    fprintf(stdout, "after move \n");
    fprintf(stdout, "old data \n");
    for (auto &i : oldv) {
        fprintf(stdout, "%s ", i.c_str());
    }
    fprintf(stdout, "\n");

    fprintf(stdout, "new data\n");
    for (auto &i : newv) {
        fprintf(stdout, "%s ", i.c_str());
    }
    fprintf(stdout, "\n");
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
    bind内不仅不再有boost占位符实现的1st,2nd的个数限制，还可以传递常量，并可以指定参数的顺序
*/

class CA
{
public:
    int func(int a) {
        return pow(a, a);
    }
};

struct MyPair
{
    int32_t a_, b_;
    int32_t multiply() {
        return a_ * b_;
    }
};

void func17()
{
    //方式1
    auto f = [](int32_t _a, int32_t _b) {
        return _a + _b;
    };

    auto autof1 = std::bind(f, std::placeholders::_1, std::placeholders::_2);
    fprintf(stdout, "autof1 result %d\n", autof1(10, 20));

    //方式2
    CA ca;
    auto autof2 = std::bind(&CA::func, ca, std::placeholders::_1);
    fprintf(stdout, "autof2 result %d\n", autof2(3));

    //方式3
    MyPair ten_two{10, 2};
    auto autof3 = std::bind(&MyPair::multiply, std::placeholders::_1);   //return x.multiply()
    fprintf(stdout, "autof3 result %d\n", autof3(ten_two));

    //方法4
    auto autof4 = std::bind(&MyPair::a_, ten_two);  //return ten_two.a_
    fprintf(stdout, "autof4 result %d\n", autof4());
}

/*
    18、std::function
    function作为函数指针，同样可以作为参数传递并执行

*/

int my_add1(int32_t a, double b, std::string c)
{
    b = a * 3;
    return int(a + b);
}

void func18()
{
    //方法1
    //function内定义了该function调用时的顺序，也是_1,_2,..._n的顺序，bind内要整理符合绑定的函数参数顺序
    //bind中的_1对应function中的第一个string，bind中的_2对应function中的int32_t
    std::function<int32_t (std::string, int32_t)> function1 = std::bind(my_add1, std::placeholders::_2, 2.0, std::placeholders::_1);
    fprintf(stdout, "function1 result %d\n", function1("aaa", 1));

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

    func15();

    //func16();

    //func17();

    //func18();

    cin.get();
    return 0;
}
