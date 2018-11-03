#include <iostream>
#include <vector>
#include <stdint.h>
#include <algorithm>

using namespace std;

void func1() {
    /*
    vector的erase和remove方法：
        erase有一个方法，就是删除两个节点之间的全部元素，这时依靠remove操作将等于删除值的节点全部移到容器末尾，进行删除
            vec.erase(remove(vec.begin(), vec.end(), 6), vec.end());
        STL中remove（）只是将待删除元素之后的元素移动到vector的前端，而不是删除，若要真正移除，需要搭配使用erase()。
            对于原vector { 10 20 10 15 12 7 9 }，删除10，会将10后面的元素移动到前面
            删除10以后的元素变成{20 15 12  7   9  7 9}

    */
    std::vector<int32_t> test1 = { 1, 3, 3, 5, 6, 7, 9, 9, 3};
    std::remove(test1.begin(), test1.end(), 3);
    for (auto &it : test1) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
    // 1, 5, 6, 7, 9, 9, 9, 9, 3

    test1 = { 1, 3, 3, 5, 6, 7, 9, 9, 3 };
    test1.erase(std::remove(test1.begin(), test1.end(), 3), test1.end());
    for (auto &it : test1) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
    // 1, 5, 6, 7, 9, 9

    test1 = { 1, 3, 3, 5, 6, 7, 9, 9, 3 };
    for (auto i = 0; i < test1.size(); i++) {
        if (test1[i] == 6) {
            test1.erase(test1.begin() + i, test1.end());
        }
    }
    test1.erase(std::remove(test1.begin(), test1.end(), 3), test1.end());
    for (auto &it : test1) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
    // 1, 5
}

void func2()
{
    /*
        vector的6种初始化方法
    */
    vector<int> v1; //默认初始化
    vector<int> v2(v1); //使用其他的vector进行初始化
    vector<int> v3 = { 1, 2, 3, 4 };    //直接赋值
    vector<int> v4(v3.begin(), v3.begin()+5);   //使用其他的vector进行赋值
    vector<int> v5(v4.begin(), v4.end() - 1);   //使用其他的vector进行赋值
    vector<int> v6(7);  //包含7个缺省的值
    vector<int> v7(7,10);   //7个10的vector
}

int main(int argc, char const *argv[])
{
    func1();

    std::cin.get();
    return 0;
}
