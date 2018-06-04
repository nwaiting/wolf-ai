#include <iostream>
#include <random>
#include <algorithm>
#include <vector>
#include <inttypes.h>
#include <numeric>

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

/*
    iota(begin,end,start); 从start开始递增加1
    accumulate(begin, end, start); 从start开始累加到end，然后在加上start
    itoa();从int转char
*/

struct Functor
{
    int operator() (int a, int b)
    {
        return a + b;
    }
};

void func3()
{
    vector<int32_t> gem(10, 0);
    for (auto it : gem){
        cout << it << " ";
    }
    cout << endl;

    std::iota(gem.begin(), gem.end(), -1);
    for (auto it:gem) {
        cout << it << " ";
    }
    cout << endl;

    //方法1
    int32_t total = std::accumulate(gem.begin(), gem.end(), 10);
    cout << "total1 " << total << endl;

    //方法2
    total = std::accumulate(gem.begin(), gem.end(), 10, plus<int32_t>());
    cout << "total2 " << total << endl;

    //方法3
    total = std::accumulate(gem.begin(), gem.end(), 10, Functor());
    cout << "total3 " << total << endl;

    //方法4 lambda
    total = std::accumulate(gem.begin(), gem.end(), 10, [](int a, int b) -> int {return a + b; });
    cout << "total4 " << total << endl;
}

int main()
{
    //func1();

    //func2();

    func3();

    cin.get();
    return 0;
}
