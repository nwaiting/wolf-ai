#include <iostream>
#include <vector>
#include <list>
#include <algorithm>
#include <string>
#include <stdint.h>
using namespace std;

/*
*   LIS（最长递增子序列）、最大连续子串和问题
*
*
*
*
*/

// LIS（最长递增子序列）
int32_t LIS(const std::vector<int32_t> &vecs)
{
    int32_t lis_length = 1;
    int32_t last_value = 0;
    std::vector<int32_t> lengths(vecs.size(), 1);
    for (auto i = 1; i < vecs.size(); i++) {
        for (auto j = 0; j < i; j++) {
            if (vecs[j] < vecs[i] && lengths[j] + 1 > lengths[i]) {
                lengths[i] = lengths[j] + 1;
                if (lengths[i] > lis_length) {
                    lis_length = lengths[i];
                    last_value = vecs[i];
                }
            }
        }
    }

#ifdef _DEBUG
    for (auto &it : lengths) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
#endif

    std::list<int32_t> lis_list;
    int32_t tmp_lis_length = lis_length;
    for (int32_t i = lengths.size() - 1; i >= 0; i--) {
        if (lengths[i] == tmp_lis_length && vecs[i] <= last_value) {
            lis_list.push_back(vecs[i]);
            last_value = vecs[i];
            tmp_lis_length--;
        }
    }


    std::cout << "LIS: ";
    while (!lis_list.empty()) {
        std::cout << lis_list.back() << " ";
        lis_list.pop_back();
    }
    std::cout << std::endl;


    return lis_length;
}

//最大连续子序列和问题
//方法1：暴力法穷举法，O(n^3) 3层循环找到最大子序列和

//方法2：dp算法 O(n)
//分析：dp[n]表示以第n个数结尾的最大连续子序列的和
//      dp[n] = max(0, dp[n-1]) + num[n]  这里是关键 ！！！！
int maxSubSequence(const std::vector<int32_t> &vecs)
{
    std::vector<int32_t> dp(vecs.size(), 0);
    auto i = 0;
    int32_t max_sum = 0;
    int32_t max_index = 0;
    for (; i < vecs.size(); i++) {
        if (vecs[i] > 0) {
            break;
        }
    }

    dp[i] = vecs[i];
    for (i = i + 1; i < vecs.size(); i++) {
        if (dp[i-1]+vecs[i] > 0) {
            dp[i] = dp[i - 1] + vecs[i];
            if (max_sum < dp[i]) {
                max_sum = dp[i];
                max_index = i;
            }
        }
    }

    //找到对应的最大的序列
    int32_t tmp_max_sum = max_sum;
    std::list<int32_t> max_sum_list;
    for (int32_t j = max_index; j >= 0 && tmp_max_sum > 0; j--) {
        if (dp[j] == tmp_max_sum) {
            max_sum_list.push_back(vecs[j]);
            tmp_max_sum -= vecs[j];
        }
    }

    while (!max_sum_list.empty()) {
        std::cout << max_sum_list.back() << " ";
        max_sum_list.pop_back();
    }
    std::cout << std::endl;

    return max_sum;
}



int main()
{
    std::vector<int32_t> vec = { 1, 9, 3, 7, 5, 2, 6, 9, 4 };
    std::cout << LIS(vec) << std::endl;


    vec.assign({ 1, -9, 3, -7, -6, 5, -2, 9, 4 });
    std::cout << maxSubSequence(vec) << std::endl;
    std::cin.get();
    return 0;
}
