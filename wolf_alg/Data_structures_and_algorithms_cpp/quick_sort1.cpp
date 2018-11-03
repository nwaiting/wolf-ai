#include <iostream>
#include <vector>
#include <stdint.h>

void quickSort(std::vector<int32_t> &source, int32_t l, int32_t r)
{
    if (l >= r){
        return;
    }

    int32_t key = source[l];
    int32_t begin = l;
    int32_t end = r;
    while (l < r) {
        while (l < r){
            if (source[r] >= key){
                r--;
            }
            else {
                break;
            }
        }

        while (l < r) {
            if (source[l] <= key){
                l++;
            }
            else {
                break;
            }
        }

        if (l < r) {
            std::swap(source[l], source[r]);
        }
    }

    std::swap(source[begin], source[l]);
    quickSort(source, begin, l - 1);
    quickSort(source, l + 1, end);
}

void quickSortArray(int32_t *source, int32_t l, int32_t r)
{
    if (l >= r){
        return;
    }

    int32_t key = source[l];
    int32_t begin = l;
    int32_t end = r;
    while (begin < end) {
        while (begin < end) {
            if (source[end] >= key){
                end--;
            }
            else {
                break;
            }
        }

        while (begin < end) {
            if (source[begin] <= key) {
                begin++;
            }
            else {
                break;
            }
        }

        if (begin < end) {
            std::swap(source[begin], source[end]);
        }
    }

    std::swap(source[begin], source[l]);
    quickSortArray(source, l, begin - 1);
    quickSortArray(source, begin + 1, r);
}

int main()
{
    std::vector<int32_t> s = { 50, 10, 100, 20, 10, 30, 200, 80, 70, 40 };
    int32_t sarray[] = { 50, 10, 100, 20, 10, 30, 200, 80, 70, 40 };
    quickSort(s, 0, s.size()-1);
    for (auto &it:s) {
        std::cout << it << " ";
    }
    std::cout << std::endl;

    quickSortArray(sarray, 0, sizeof(sarray) / sizeof(int32_t) - 1);
    for (auto i = 0; i < 10; i++) {
        std::cout << sarray[i] << " ";
    }

    std::cin.get();
    return 0;
}
