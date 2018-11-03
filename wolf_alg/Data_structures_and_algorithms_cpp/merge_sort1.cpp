#include <iostream>
#include <vector>
#include <stdint.h>

std::vector<int32_t> mergeSortInner(const std::vector<int32_t> &l, const std::vector<int32_t> &r)
{
    std::vector<int32_t> tmp;
    int32_t lindex = 0, rindex = 0;
    while (lindex < l.size() && rindex < r.size()) {
        if (l[lindex] <= r[rindex]){
            tmp.push_back(l[lindex]);
            lindex++;
        }
        else {
            tmp.push_back(r[rindex]);
            rindex++;
        }
    }

    if (lindex < l.size()) {
        tmp.insert(tmp.end(), l.begin() + lindex, l.end());
    }

    if (rindex < r.size()) {
        tmp.insert(tmp.end(), r.begin() + rindex, r.end());
    }
    return tmp;
}

std::vector<int32_t> mergeSort(const std::vector<int32_t> &source)
{
    if (source.size() <= 1){
        return source;
    }

    int32_t middle = source.size() / 2;
    std::vector<int32_t> lf(source.begin(), source.begin() + middle);
    std::vector<int32_t> l = mergeSort(lf);
    std::vector<int32_t> lr(source.begin() + middle, source.end());
    std::vector<int32_t> r = mergeSort(lr);
    return mergeSortInner(l, r);
}

int main()
{
    std::vector<int32_t> s = { 10, 100, 70, 30, 20, 50, 90, 60, 80, 20, 30, 10 };
    std::vector<int32_t> ss = mergeSort(s);
    for (auto &it:ss) {
        std::cout << it << " ";
    }

    std::cin.get();
    return 0;
}

