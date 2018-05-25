#include <iostream>
#include <vector>
#include <random>
#include <time.h>
#include <stdint.h>
using namespace std;


template <typename T>
void myShow(vector<T>& s)
{
    for (auto& it:s) {
        cout << it << " ";
    }
    cout << endl;
}

//先找到中间值的位置，然后将中间值置入到相应位置
//内排序
void quick_sort(vector<int32_t>& d, int32_t l, int32_t r)
{
    if (l >= r) {
        return;
    }

    int32_t m = d[l];
    int32_t tl = l;
    int32_t tr = r;
    while (tl < tr) {
        //先从右边开始遍历，顺序比较重要
        while (tl < tr && d[tr] >= m) tr -= 1;
        while (tl < tr && d[tl] <= m) tl += 1;
        if (tl < tr) swap(d[tl], d[tr]);
    }

    swap(d[l], d[tl]);
    quick_sort(d, l, tl - 1);
    quick_sort(d, tl + 1, r);
}

void func1()
{
    default_random_engine dre(time(NULL));
    uniform_int_distribution<> uni(0, 1000);
    vector<int32_t> soudata;
    for (auto i = 0; i < 10; i++) {
        soudata.push_back(uni(dre));
    }

    cout << "source data is " << endl;
    myShow(soudata);

    quick_sort(soudata, 0, soudata.size() - 1);
    cout << "after quick sort" << endl;
    myShow(soudata);
}

int main()
{
    func1();


    cin.get();
    return 0;
}
