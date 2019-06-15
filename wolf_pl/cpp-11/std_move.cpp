#include <iosream>
using namespace std;

/*
    右值引用：
        右值引用（及其支持的Move语意和完美转发）是C++0x加入的最重大语言特性之一。从实践角度讲，它能够完美解决C++中长久以来为人所诟病的临时对象效率问题。
        从语言本身讲，它健全了C++中的引用类型在左值右值方面的缺陷。从库设计者的角度讲，它给库设计者又带来了一把利器。从库使用者的角度讲，不动一兵一卒便可以获得“免费的”效率提升

        如：
        A a2(std::move(a1));
            将a1转换为右值，因此a2调用的移动构造而不是拷贝构造

        A(const A& src):m_b(new B(*(src.m_b))){}
        A(A&& src):m_b(src.m_b){}
        A& operator=(const A& src) noexcept{}
        A& operator=(A&& src) noexcept{}
            总之尽量给类添加移动构造和移动赋值函数，而减少拷贝构造和拷贝赋值的消耗。 移动构造，移动赋值要加上noexcept，用于通知标准库不抛出异常
            原value值被moved之后值被转移,所以为空字符串
*/

int main(int argc, char const *argv[]) {
    /* code */

    return 0;
}
