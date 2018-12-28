#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <stdint.h>
#include <list>
using namespace std;

/*
*   LCS(最长公共子序列)、LIS（最长递增子序列）、最大子序列、最长公共子串（要求连续）
*
*
*
*
*/

/////////////////////////////// LCS 最长公共子序列

int LCS(const std::string &s1, const std::string &s2)
{
    std::vector<std::vector<int32_t>> commonstr;
    std::vector<int32_t> tmp_vec(s2.size()+1, 0);
    for (auto i = 0; i <= s1.size(); i++) {
        commonstr.push_back(tmp_vec);
    }

    //dp
    for (auto i = 1; i <= s1.size(); i++) {
        for (auto j = 1; j <= s2.size(); j++) {
            //当判断是中文时，需要改一下
            if (s1[i-1] == s2[j-1]) {
                commonstr[i][j] = commonstr[i-1][j-1] + 1;
            }
            else {
                commonstr[i][j] = (std::max)(commonstr[i - 1][j], commonstr[i][j - 1]);
            }
        }
    }

#ifdef DEBUG
    for (auto &iti:commonstr) {
        for (auto &itj: iti) {
            std::cout << itj << " ";
        }
        std::cout << std::endl;
    }
#endif

    std::list<int8_t> commlist;
    int32_t ii = s1.size(), jj = s2.size();
    //commlist.push_back(commonstr[ii][jj]);
    commlist.push_back(s1[ii]);
    while (ii > 0 && jj > 0) {
        if (commonstr[ii-1][jj] == commonstr[ii][jj]) {
            ii--;
        }
        else {
            //commlist.push_back(commonstr[ii-1][jj-1]);
            commlist.push_back(s1[ii-1]);
            ii--;
            jj--;
        }
    }


    while (!commlist.empty()) {
        printf("%c ", commlist.back());
        commlist.pop_back();
    }
    std::cout << std::endl;

    return commonstr[s1.size()][s2.size()];
}

void showLCS(const std::string &s1, const std::string &s2)
{
    std::cout<<"LCS: " << s1.c_str()<<" - "<<s2.c_str()<<" -> " << LCS(s1, s2) << std::endl;
}


///////////////////最长功能字串

int32_t LCSubstring(const std::string &s1, const std::string &s2)
{
    int32_t longest_lcsubstring = 0;
    std::vector<std::vector<int32_t>> dp;
    std::vector<int32_t> tmp_vec(s2.size() + 1, 0);
    for (auto i = 0; i <= s1.size(); i++) {
        dp.push_back(tmp_vec);
    }

    for (auto i = 1; i <= s1.size(); i++) {
        for (auto j = 1; j <= s2.size(); j++) {
            if (s1[i] == s2[j]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                longest_lcsubstring = (std::max)(longest_lcsubstring, dp[i][j]);
            }
        }
    }

#ifdef DEBUG
    for (auto &iti:dp) {
        for (auto &itj:iti) {
            std::cout << itj << " ";
        }
        std::cout << std::endl;
    }
#endif

    std::list<int8_t> commonlist;
    bool flag = true;
    for (auto i = s1.size(); i > 0 && flag; i--) {
        for (auto j = s2.size(); j > 0 && flag; j--) {
            if (dp[i][j] == longest_lcsubstring) {
                int32_t tmp_l = longest_lcsubstring;
                while (tmp_l > 0) {
                    commonlist.push_back(s1[i]);
                    tmp_l--;
                    i--;
                }
                flag = false;
                break;
            }
        }
    }

    while (!commonlist.empty()) {
        printf("%c ", commonlist.back());
        commonlist.pop_back();
    }
    std::cout << std::endl;

    return longest_lcsubstring;
}

void showLCSubstring(const std::string &s1, const std::string &s2)
{
    std::cout <<"lcsubstring: "<< s1.c_str() << " - " << s2.c_str() << " -> " << LCSubstring(s1, s2) << std::endl;
}


//////////////////////LIS

int32_t LIS(const std::string &s1, const std::string &s2)
{

}

void showLIS(const std::string &s1, const std::string &s2)
{
    std::cout << "LIS:" << s1.c_str() << " - " << s2.c_str() << " -> " << LIS(s1, s2) << std::endl;
}

int main()
{
    showLCS("ABCBDAB", "BDCABA");
    showLCS("成都空调移机多少钱", "成都空调移机多少钱");
    showLCS("房地产中介好做吗", "苹果6现在多少钱");

    showLCSubstring("ABCABABD", "BDCABA");

    std::cin.get();
    return 0;
}
