#include <iostream>
#include <vector>
#include <list>
#include <algorithm>
#include <stdint.h>
using namespace std;

/**
    * No1.塔树选择和最大问题
    *
    * 一个高度为N的由正整数组成的三角形，从上走到下，求经过的数字和的最大值。
    * 每次只能走到下一层相邻的数上，例如从第3层的6向下走，只能走到第4层的2或9上。
    *      5
    *     8 4
    *    3 6 9
    *   7 2 9 5
    * 例子中的最优方案是：5 + 8 + 6 + 9 = 28
    *
    * 输入：符合塔树的二维数组。
    * 输出：经过的最大值。
    *
    * 分析：
    * dp(x,y)：表示第x层第y个数所经过的最大值。
    * dp(x,y)={
    *      array[x][y]  当x==0;
    *      dp[x-1,y] + array[x][y] 当x!=0,y=0;
    *      dp[x-1,y-1] + array[x][y] 当x!=0,y=x;
    *      max(dp[x-1,y-1],dp[x-1,y]) + array[x][y] 当x!=0;
    * }
*/

static int32_t n = 6;

//从后面开始往前面推导
int func1(const std::vector<std::vector<int32_t> > &vecs, std::vector<std::vector<int32_t> > &dp)
{
    for (auto i = 0; i < n; i++) {
        dp[n - 1][i] = vecs[n - 1][i];
    }

    for (auto i = n - 1; i >= 0; i--) {
        for (auto j = 0; j <= i; j++) {
            dp[i][j] = (std::max)(dp[i + 1][j], dp[i + 1][j + 1]) + vecs[i][j];
        }
    }
    return dp[0][0];
}

void showPath(const std::vector<std::vector<int32_t> > &vecs, const std::vector<std::vector<int32_t>> &dp)
{
    std::list<int32_t> showlist;
    int32_t next_value = dp[0][0] - vecs[0][0];
    showlist.push_back(vecs[0][0]);
    for (auto i = 1; i < dp.size(); i++) {
        for (auto j = 0; j < dp.size(); j++) {
            if (next_value == dp[i][j]) {
                showlist.push_back(vecs[i][j]);
                next_value -= vecs[i][j];
                break;
            }
        }
    }

    for (auto &it : showlist) {
        std::cout << it << "->";
    }
    std::cout << std::endl;
}

int towerTree(const std::vector<std::vector<int32_t>> &vec, int32_t x, int32_t y)
{
    if (x == 0){
        return vec[0][0];
    }

    if (y == 0){
        return vec[x][y] + towerTree(vec, x - 1, y);
    }
    else if (y == x){
        //这种情况下，只有一种路线可以达到
        return vec[x][y] + towerTree(vec, x - 1, y - 1);
    }
    else {
        return (std::max)(towerTree(vec, x - 1, y), towerTree(vec, x - 1, y - 1)) + vec[x][y];
    }
}

//不使用额外的dp存储空间，直接计算结果
//从前面往后面开始计算
int func2(const std::vector<std::vector<int32_t>> &vec)
{
    std::list<int32_t> results;
    for (auto i = 0; i < 5; i++) {
        results.push_back(towerTree(vec, n, i));
    }

    return results.back();
}

int main(int argc, char **argv)
{
    std::vector<std::vector<int32_t> > dp;
    std::vector<std::vector<int32_t>> sourcedata;
    for (auto i = 0; i <= n; i++) {
        dp.push_back({ 0, 0, 0, 0, 0, 0, 0 });
        sourcedata.push_back({ 0, 0, 0, 0, 0, 0 });
    }

    sourcedata[0] = { 9, 0, 0, 0, 0, 0 };
    sourcedata[1] = { 12, 15, 0, 0, 0, 0 };
    sourcedata[2] = { 10, 6, 8, 0, 0, 0 };
    sourcedata[3] = { 2, 18, 9, 5, 0, 0 };
    sourcedata[4] = { 19, 7, 10, 4, 16, 0 };


    //方法一，使用额外的存储空间，可以回溯
    int32_t ret = func1(sourcedata, dp);
    std::cout << "func1 result is " << ret << std::endl;
    showPath(sourcedata, dp);


    //方法二，不使用额外空间，直接计算
    sourcedata[0] = { 9};
    sourcedata[1] = { 12, 15};
    sourcedata[2] = { 10, 6, 8};
    sourcedata[3] = { 2, 18, 9, 5};
    sourcedata[4] = { 19, 7, 10, 4, 16};
    ret = func2(sourcedata);
    std::cout << "func2 result is " << ret << std::endl;

    std::cin.get();
    return 0;
}
