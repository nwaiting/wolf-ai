#include <iostream>
#include <vector>
#include <stdint.h>
#include <algorithm>
#include <functional>

/*
    算法1：sort()
    算法2：partial_sort()  实现局部排序，如寻找最大的前4个数
    算法3：nth_element()   实现取第几大的数据
    算法4：max_element()   取最大值或者索引
    算法5：min_element()   取最小值或索引
    算法6：find()  查找
*/


void Printf(const std::vector<int32_t> &vecInt)
{
    for (auto &it:vecInt) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
}

//算法2：partial_sort()  实现局部排序，如寻找最大的前4个数
void func2()
{
    std::vector<int32_t> a = {1,5,6,200,324,45,756,96,78,32,5};
    std::partial_sort(a.begin(), a.begin()+3, a.end());
    Printf(a);

    std::partial_sort(a.begin(), a.begin() + 3, a.end(), std::greater<int32_t>());
    Printf(a);
}

//算法3：nth_element()   实现取第几大的数据，如取第3小的数，前3个就是最小的
void func3()
{
    std::vector<int32_t> a;
    //当数据较小时，对数据进行了全排序，每个平台实现不一样，当数据较大时，仅进行了部分排序
    for (auto i = 1; i <= 5000; i++){
        a.push_back(i);
    }
    std::random_shuffle(a.begin(), a.end());
    Printf(a);

    std::nth_element(a.begin(), a.begin() + 5, a.end());
    Printf(a);
}

//算法4：max_element()   取最大值或者索引
//算法5：min_element()   取最小值或索引
void func4()
{
    std::vector<int32_t> a;
    for (auto i = 1; i <= 10; i++){
        a.push_back(i);
    }
    std::random_shuffle(a.begin(), a.end());
    Printf(a);

    std::vector<int32_t>::iterator bigone = max_element(a.begin(), a.end());
    std::cout << *bigone << std::endl;      //获取最大值
    std::cout << bigone - a.begin() << std::endl;   //获取最大值的索引，从0开始

    std::vector<int32_t>::iterator smallone = min_element(a.begin(), a.end());
    std::cout << *smallone << std::endl;      //获取最大值
    std::cout << smallone - a.begin() << std::endl;   //获取最大值的索引，从0开始   
}

//算法6：find()  查找
void func5()
{
    std::vector<int32_t> a;
    for (auto i = 1; i <= 10; i++){
        a.push_back(i);
    }
    std::random_shuffle(a.begin(), a.end());
    Printf(a);

    std::vector<int32_t>::iterator vecIte = std::find(a.begin(), a.end(), 5);
    std::cout << *vecIte << std::endl;
    std::cout << vecIte - a.begin() << std::endl;
}

int main()
{
    //func2();
    //func3();
    //func4();
    func5();

    std::cin.get();
    return 0;
}
