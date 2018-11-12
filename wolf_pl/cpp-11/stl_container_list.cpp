#include <list>
#include <iostream>
#include <stdint.h>
#include <vector>
#include <algorithm>
#include <functional>

void Printf(const std::list<int32_t> &lint)
{
    for (auto &it:lint) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
}

void func1()
{
    std::vector<int32_t> vec;
    for (auto i = 1; i <= 5; i++) {
        vec.push_back(i);
    }
    std::random_shuffle(vec.begin(), vec.end());
    std::list<int32_t> a(vec.begin(), vec.end());
    std::cout << "a: ";
    Printf(a);

    a.reverse();    //反转
    Printf(a);

    std::random_shuffle(vec.begin(), vec.end());
    std::list<int32_t> b(vec.begin(), vec.end());
    std::cout << "b: ";
    Printf(b);
 
//     a.push_front();  增加到链表头
//     a.push_back();   增加到链表尾
//     a.pop_front();   删除链表头的元素
//     a.pop_back();    删除链表尾的元素


    /*
        merge：合并（实验中不会报错，应该是c++11中已经做了兼容，不会报错）
            1）merge()是将两个有序的链表合并成另一个有序的链表，如果有一个链表不是有序的那么在执行代码时会报错：说链表不是有序的。
            2）还有，两个链表中的内容排序顺序与合并时采用的排序顺序必须一致，如果不一致，也会报错，说链表不是有序的。如想要降序合并两个链表，那么合并前的两个链表也必须是按降序排列的。
            3）另外，当执行完merge()后，右边的链表将变为空。
    */
    std::list<int32_t> aa(a);
    std::list<int32_t> bb(b);
    aa.merge(bb);     //合并链表，合并后b就为空了
    Printf(aa);

    std::list<int32_t> aaa(a);
    std::list<int32_t> bbb(b);
    aaa.merge(bbb, std::greater<int32_t>());
    Printf(aaa);

    //swap交换两个链表，两种交换方法效果一样
    std::cout << "=============1" << std::endl;
    std::list<int32_t> aaaa(a);
    std::list<int32_t> bbbb(b);
    aaaa.swap(bbbb);
    Printf(aaaa);
    Printf(bbbb);

    std::list<int32_t> aaaaa(a);
    std::list<int32_t> bbbbb(b);
    std::swap(aaaaa, bbbbb);
    Printf(aaaaa);
    Printf(bbbbb);

    //unique 删除相邻重复元素，仅仅删除相邻的元素，不对所有元素去重
    std::cout << "=============2" << std::endl;
    std::vector<int32_t> a11 = { 1, 1, 4, 3, 5, 1 };
    std::list<int32_t> a1(a11.begin(), a11.end());
    std::list<int32_t> b1(a11.begin(), a11.end());
    a1.unique();
    Printf(a1);
    Printf(b1);
}

int main()
{
    func1();

    std::cin.get();
    return 0;
}
