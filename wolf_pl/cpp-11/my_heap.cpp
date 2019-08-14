#include <iostream>
#include <algorithm>
#include <queue>
#include <stdint.h>
#include <random>
#include <time.h>
#include <vector>
using namespace std;

/*
    STL heap包括：
        缺省情况下priority_queue优先级队列是利用一个max-heap最大堆完成，后者是一个以vector表现的完全二叉树。“依权值高低自动递减排序”
        priority_queue允许用户以任何次序将任何元素推入容器内，但取出时一定是从优先权最高(也即数值最高，最大堆)的元素开始取

        push_heap算法：
            新元素插入在底层的vector的end()处。向上回溯
        pop_heap算法：
            把堆顶元素和数值末尾元素调换，向下回溯
        sort_heap算法：
            持续对整个heap做pop_heap操作，每次将操作范围从后向前缩减一个元素。执行过后，原来的heap不再是个合法的heap了
        meak_heap算法：
            找出第一个需要重排的子树头部(n-2)/2，从当前位置向根节点回溯
*/

//std::priority_queue
struct Node {
    int32_t a;
    int32_t b;
};
struct comp
{
    bool operator() (const Node& a, const Node& b) {
        return true;
    }
};

template<typename T>
void showData(const vector<T>& d)
{
    for (auto &it:d) {
        cout << it << "-";
    }
    cout << endl;
}

void func1()
{
    default_random_engine dre(time(NULL));
    uniform_int_distribution<> uni_int(10, 100);

    //使用1，直接使用
    priority_queue<pair<int32_t, int32_t>> heap1;
    for (int i = 0; i < 10; i++) {
        heap1.push(make_pair(uni_int(dre), i));
    }

    while (!heap1.empty()) {
        pair<int32_t,int32_t> tvalue = heap1.top();
        cout << tvalue.first << "-" << tvalue.second << endl;
        heap1.pop();
    }

    //使用2，使用结构体时，如果要自定义比较函数的话，则在Node中重载运算符号 bool operator< () {}
    priority_queue<Node> heap2;

    //使用3，自定义比较函数
    //priority_queue中的三个参数，后两个可以省去，因为有默认参数，不过如果，有第三个参数的话，必定要写第二个参数
    //第三个参数是一个类，这个类里重载operator()，和自定义sort排序不同，sort只需bool cmp（……）
    priority_queue<Node, vector<Node>, comp> heap3;
}

//push_heap、pop_heap、make_heap、sort_heap
//make_heap将[start, end)范围进行堆排序，默认使用less, 即最大元素放在第一个
//pop_heap将front（即第一个最大元素）移动到end的前部，同时将剩下的元素重新构造成(堆排序)一个新的heap
//push_heap对刚插入的（尾部）元素做堆排序
//sort_heap将一个堆做排序,最终成为一个有序的系列，可以看到sort_heap时，必须先是一个堆（两个特性：1、最大元素在第一个 2、添加或者删除元素以对数时间），因此必须先做一次make_heap
void func2()
{
    vector<int32_t> data1;
    default_random_engine dre(time(NULL));
    uniform_int_distribution<> unint(10, 50);
    for (int32_t i = 0; i < 10; i++) {
        data1.push_back(unint(dre));
    }
    showData(data1);

    //默认大根堆
    make_heap(data1.begin(), data1.end());
    showData(data1);

    //取出最大值，然后重新构造堆
    pop_heap(data1.begin(), data1.end());
    cout << data1.back() << endl;
    data1.pop_back();
    showData(data1);

    //对刚插入的值做堆排序
    data1.push_back(10086);
    push_heap(data1.begin(), data1.end());
    showData(data1);

    //对堆做排序
    sort_heap(data1.begin(), data1.end());
    showData(data1);
}

int main()
{
    //func1();

    func2();

    cin.get();
    return 0;
}
