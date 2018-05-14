#include <iostream>
#include <random>
#include <algorithm>
#include <vector>
#include <inttypes.h>

using namespace std;

/*
    linux编译：g++ common_use.cpp -o common_use -std=c++0x
*/

void func1()
{
    vector<uint32_t> data1;
    for (int i = 0; i < 10; i++) {
        data1.push_back(i);
    }

    //随机打乱 c++11支持
    std::shuffle(data1.begin(), data1.end(), std::default_random_engine(1));
    for (auto& it : data1)
    {
        cout << it << " ";
    }
    cout << endl;
}

//
void func2() {
    std::vector<int> datas;
    datas.push_back(1);
    datas.push_back(2);
    datas.push_back(3);

    //引用 可以改变原来的值
    /*
    for(auto &it: datas) {
        it = 5;
    }
    */

    //不能改变原来的值
    for (auto it : datas) {
        it = 5;
    }

    cout << "show data:" << endl;
    for (auto it : datas) {
        cout << it << endl;
    }
}


int main()
{
    //func1();

    func2();

    cin.get();
    return 0;
}
