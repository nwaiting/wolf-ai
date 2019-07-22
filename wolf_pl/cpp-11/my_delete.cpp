#include <iosream>


/*
    delete只会调用一次析构函数，而delete[]会调用每一个成员的析构函数。在More Effective C++中有更为详细的解释：“当delete操作符用于数组时，
        它为每个数组元素调用析构函数，然后调用operator delete来释放内存。

*/

int main(int argc, char const *argv[]) {
    /* code */
    return 0;
}
