#include <iostream>
#include <windows.h>
using namespace std;

/*
  图存储方式有：邻接矩阵和邻接表
*/

template <typename T>
struct ENode {
    int32_t one_vertex_;
    int32_t other_vertex_;
    T weights_;
    ENode<T> *next_;
    ENode(){ next_ = NULL; }
    ENode(int32_t onevertex, int32_t othervertex, T weights, )
};

int main(int argc, const char* argv[]) {
    cout << "this is test" << endl;
    Sleep(1000 * 100);
    return 0;
}
