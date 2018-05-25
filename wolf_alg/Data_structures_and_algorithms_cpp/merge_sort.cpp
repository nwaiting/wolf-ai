#include <iostream>
#include <vector>
#include <stdint.h>
#include <random>
#include <time.h>
using namespace std;

template <typename T>
void myShow(vector<T> d)
{
    for (auto &it:d) {
        cout << it << " ";
    }
    cout << endl;
}

void mymerge(vector<int32_t> &d, int32_t l, int32_t m, int32_t r, vector<int32_t>& dest)
{
    int32_t i = l;
    int32_t j = m + 1;
    int32_t k = 0;
    while (i <= m && j <= r) {
        if (d[i] <= d[j]){
            dest[k++] = d[i++];
        }
        else {
            dest[k++] = d[j++];
        }
    }

    while (i <= m) dest[k++] = d[i++];
    while (j <= r) dest[k++] = d[j++];

    k = 0;
    while (l <= r) d[l++] = dest[k++];
}

//思想是先归然后在合并，递归思想
//外排序
void merge_sort(vector<int32_t> &d, int32_t l, int32_t r, vector<int32_t> &dest)
{
    if (l >= r){
        return;
    }

    int32_t m = (l + r) / 2;
    merge_sort(d, l, m, dest);
    merge_sort(d, m+1, r, dest);
    mymerge(d, l, m, r, dest);
}

void func1()
{
    default_random_engine dre(static_cast<uint32_t>(time(NULL)));
    uniform_int_distribution<> uni(1, 10000);
    vector<int32_t> soudata;
    for (auto i = 0; i < 10; i++) {
        soudata.push_back(uni(dre));
    }

    cout << "before sort " << endl;
    myShow(soudata);


    vector<int32_t> des(soudata.size());
    merge_sort(soudata, 0, soudata.size() - 1, des);
    cout << "after sort" << endl;
    myShow(des);
}

int main()
{
    func1();

    cin.get();
    return 0;
}
