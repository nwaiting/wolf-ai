#include <iostream>
#include <vector>
#include <stdint.h>
#include <algorithm>
using namespace std;

/*
*   编辑距离：
*       编辑距离又叫Levenshtein（莱文斯坦）距离
*       指两个字串之间，由一个转成另一个所需的最少编辑操作次数
*       俄罗斯科学家Vladimir Levenshtein在1965年提出这个概念
*
*   编辑操作：
*       1、替换一个字符
*       2、插入一个字符
*       3、删除一个字符
*
*/

int edit_dis(const std::string &s1, const std::string &s2)
{
    std::vector<std::vector<int32_t>> editdis;
    std::vector<int32_t> initdata(s2.size()+1, 0);
    for (auto i = 0; i <= s1.size(); i++) {
        editdis.push_back(initdata);
    }

    //先进行初始化
    for (auto i = 0; i <= s1.size(); i++) {
        editdis[i][0] = i;
    }

    for (auto i = 0; i <= s2.size(); i++) {
        editdis[0][i] = i;
    }

    //增、删、改三步
    for (auto i = 1; i <= s1.size(); i++) {
        for (auto j = 1; j <= s2.size(); j++) {
            //增和删
            int32_t tmp_min = (std::min)(editdis[i - 1][j] + 1, editdis[i][j - 1] + 1);
            int32_t d = 0;
            if (s1[i-1] != s2[j-1]) {
                d = 1;
            }
            //改
            tmp_min = (std::min)(tmp_min, editdis[i - 1][j - 1] + d);
            editdis[i][j] = tmp_min;
        }
    }

#ifdef DEBUG
    for (auto &iti : editdis) {
        for (auto &itj : iti) {
            std::cout << itj << " ";
        }
        std::cout << std::endl;
    }
#endif

    return editdis[s1.size()][s2.size()];
}

void showDistance(const std::string &s1, const std::string &s2)
{
    std::cout << s1.c_str() << " - " << s2.c_str() << " -> " << edit_dis(s1, s2) << std::endl;
}

int main()
{
    showDistance("sailn", "failing");   //1
    //由于每个汉字两个字符 所以结果为2
    showDistance("汽车音响改装线路","汽车音响改装线路图");   //2


    std::cin.get();
    return 0;
}
