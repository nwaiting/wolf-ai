#include <iostream>


std::vector<std::pair<int, int>> findTwoSum(std::vector<int>& src, int sum) {
    std::sort(src.begin(), src.end());
    std::vector<std::pair<int, int>> res;
    for (int i = 0; i < src.size(); i++) {
        int other_num = sum - src[i];
        int begin = i + 1;
        int end = src.size() - 1;
        while (begin <= end) {
            int mid = (begin + end) / 2;
            if (other_num > src[mid]) {
                begin = mid + 1;
            }
            else if (other_num < src[mid]) {
                end = mid - 1;
            }
            else {
                if (other_num == src[mid]) {
                    std::cout << src[i] << "-" << other_num << std::endl;
                    break;
                }
            }
        }
    }
    return res;
}

int main() {
    std::vector<int> data{5,10,25,15,35,55,65,75};
    findTwoSum(data, 80);
    return 0;
}
