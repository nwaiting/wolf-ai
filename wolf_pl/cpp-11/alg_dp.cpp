#include <iostream>
#include <stdint.h>
#include <vector>
#include <algorithm>
#include <set>
#include <queue>
#include <string.h>

//dp for LIS O(n^2)
//求最长单调递增子序列长度
uint32_t LIS1(const std::string &src)
{
	if (src.size() <= 1){
		return src.size();
	}

	std::vector<int32_t> results(src.size(), 1);
	int32_t maxlen = 1;
	for (uint32_t i = 1; i < src.size(); i++) {
		for (uint32_t j = 0; j < i; j++) {
			if (src[j] < src[i]){
				results[i] = std::max(results[i], results[j] + 1);
			}
		}

		maxlen = std::max(maxlen, results[i]);
	}
	return maxlen;
}

// dp for LIS	O(n^2)
//求最长单调递增子序列 ////////////////////
int32_t LIS2(const std::string &src, std::vector<int32_t>& pre, int32_t &nindex)
{
	if (src.size() <= 1){
		return src.size();
	}

	pre.resize(src.size(), -1);
	std::vector<int32_t> results(src.size(), 1);
	int32_t maxlen = 1;
	for (uint32_t i = 1; i < src.size(); i++) {
		for (uint32_t j = 0; j < i; j++) {
			if (src[j] < src[i] && results[i] < results[j]+1) {
				results[i] = results[j] + 1;
				pre[i] = j;
			}
		}

		if (maxlen < results[i]){
			maxlen = results[i];
			nindex = i;
		}
	}

	return maxlen;
}

std::string GetLISList(const std::string &src, const std::vector<int32_t> &pre, int32_t nindex)
{
	std::string res;
	while (nindex >= 0) {
		res.insert(res.begin(), src[nindex]);
		nindex = pre[nindex];
	}

	return res;
}

//求最长单调递增子序列 ////////////////////


void LIS3Insert(std::string &resSrc, int32_t &maxlen, const std::string &src, uint32_t index)
{
	if (maxlen <= 0){
		resSrc.insert(resSrc.end(), src[index]);
		maxlen++;
		return;
	}

	uint32_t left = 0, right = resSrc.size() - 1, mid = 0;
	while (left <= right) {
		mid = (right + left) / 2;
		if (src[index] < resSrc[mid]){
			right = mid - 1;
		}
		else if (src[index] >= resSrc[mid]){
			left = mid + 1;
		}
	}

	if (left >= maxlen){
		resSrc[maxlen] = src[index];
		maxlen++;
	}
	else {
		if (resSrc[left] < src[index]){
			resSrc[left + 1] = src[index];
		}
		else {
			resSrc[left] = src[index];
		}
	}
}

// dp for LIS	O(nlgn)
//求最长单调递增子序列 缓冲区
int32_t LIS3(const std::string &src)
{
	std::string res;
	int32_t maxlen = 0;
	for (uint32_t i = 0; i < src.size(); i++){
		LIS3Insert(res, maxlen, src, i);
	}

	return maxlen;
}

struct Node{    char val;    std::vector<char> con;};void const_graph(std::vector<Node*>& nodes){    Node* ap = new Node{ 'A', { 'C', 'B', 'D' } };    nodes[int('A' - 'A')] = ap;    ap = new Node{ 'B', { 'D', 'E' } };    nodes[int('B' - 'A')] = ap;    ap = new Node{ 'C', {} };    nodes[int('C' - 'A')] = ap;    ap = new Node{ 'D', {} };    nodes[int('D' - 'A')] = ap;    ap = new Node{ 'E', { 'A' } };    nodes[int('E' - 'A')] = ap;}std::vector<Node*> gnodes(100);std::set<char> visited;std::queue<char> q;bool is_visited(char c){    return std::find(visited.begin(), visited.end(), c) != visited.end();}void find_path(char c, std::vector<char>& paths){    if (!is_visited(c)) {        paths.push_back(c);        visited.insert(c);    }    for (auto it : gnodes[int(c - 'A')]->con) {        if (!is_visited(it)) {            find_path(it, paths);        }    }}

/*
For example, given the map:A �� [C, B, D] (A is connected to C, B, D directly)B �� [D, E]C �� [] (empty list means current place isn't connected to any other place)D �� []E �� [A]
*/

void find_path_bfs(char c, std::vector<char>& paths){
    paths.push_back(c);
    visited.insert(c);
    for (auto it : gnodes[int(c - 'A')]->con) {
        q.push(it);
    }

    while (!q.empty()){
        char tmpc = q.front();
        q.pop();
        if (!is_visited(tmpc)) {
            for (auto it : gnodes[int(tmpc - 'A')]->con) {
                q.push(it);
            }
            visited.insert(tmpc);
            paths.push_back(tmpc);
        }
    }
}




/*
    lcs：long common string
*/
#define N 100
int dp[N][N];
int flag[N][N];
//longCommonString("ABCBDAB", "BDCABA");

void longCommonString(const std::string& s1, const std::string& s2)
{
    int lena = s1.size();
    int lenb = s2.size();
    for (int i = 1; i < lena; i++) {
        for (int j = 1; j < lenb; j) {
            if (s1[i-1] == s2[j-1]) {
                if (dp[i][j] < dp[i - 1][j - 1] + 1) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                }
            }
            else{
                if (dp[i - 1][j]>dp[i][j - 1]) {
                    dp[i][j] = dp[i - 1][j];
                }
                else {
                    dp[i][j] = dp[i][j - 1];
                }
            }
        }
    }
    std::cout << dp[lena - 1][lenb - 1] << std::endl;
}


class Solution {
public:
    int minimumTotal(std::vector<std::vector<int>>& triangle) {
        int m = triangle.size();
        std::vector<int> dp(triangle[m - 1].begin(), triangle[m - 1].end());
        for (int i = m - 2; i >= 0; i--){
            for (int j = 0; j < triangle[i].size() - 1; j++){
                dp[j] = triangle[i][j] + std::max(dp[j], dp[j + 1]);
            }
        }
        return dp[0];
    }
    // [5, 75, 25] 100
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            int other_num = target - nums[i];
            int begin = i + 1;
            int end = nums.size()-1;
            while (begin <= end){
                int mid = (begin + end) / 2;
                if (other_num > nums[mid]){
                    begin = mid + 1;
                }
                else if (other_num < nums[mid]){
                    end = mid - 1;
                }
                else{
                    return std::vector<int>{i, mid};
                }
            }
        }
        return std::vector<int>{};
    }
};

char charp[32] = "abc";
const char* testp()
{
    return charp;
}


int main()
{
    /*
	std::string data("1462897");
	std::cout << LIS1(data) << std::endl;
	

	std::vector<int32_t> pres;
	int32_t nnindex = 0;
	std::cout << LIS2(data, pres, nnindex) << std::endl;
	std::string ress = GetLISList(data, pres, nnindex);
	std::cout << ress.c_str() << std::endl;


	std::cout << LIS3(data) << std::endl;

    [9, 0, 0, 0, 0],
    [12, 15, 0, 0, 0],
    [10, 6, 8, 0, 0],
    [2, 18, 9, 5, 0],
    [19, 7, 10, 4, 16]

    */

    /*
    std::vector<std::vector<int>> datas{ { 9 ,0}, { 12, 15 }, { 10, 6, 8 }, { 2, 18, 9, 5 }, { 19, 7, 10, 4, 16 } };
    std::cout << "======= " << Solution().minimumTotal(datas) << std::endl;

    //[5,75,25]
    std::vector<int> datas1{ 0, 4, 3, 0 };
    std::vector<int> res = Solution().twoSum(datas1, 0);
    for (auto it : res) {
        std::cout << it << " ";
    }
    std::cout <<"========"<< std::endl;
    */

    /*
    const_graph(gnodes);    std::vector<char> p;    find_path('A', p);
    for (auto it : p) {
        std::cout << it << std::endl;
    }
    std::cout << "============" << std::endl;

    p.clear();
    visited.clear();
    find_path('B', p);
    for (auto it : p) {
        std::cout << it << std::endl;
    }

    std::cout << "bfs===================" << std::endl;
    p.clear();
    visited.clear();
    q = std::queue<char>();
    find_path_bfs('A', p);
    for (auto it : p) {
        std::cout << it << std::endl;
    }
    std::cout << "============" << std::endl;

    p.clear();
    visited.clear();
    q = std::queue<char>();
    find_path_bfs('B', p);
    for (auto it : p) {
        std::cout << it << std::endl;
    }


    longCommonString("ABCBDAB", "BDCABA");
    */

	std::cin.get();
	return 0;
}
