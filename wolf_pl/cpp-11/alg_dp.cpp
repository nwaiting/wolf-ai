#include <iostream>
#include <stdint.h>
#include <vector>
#include <algorithm>

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

int main()
{
	std::string data("1462897");
	std::cout << LIS1(data) << std::endl;
	

	std::vector<int32_t> pres;
	int32_t nnindex = 0;
	std::cout << LIS2(data, pres, nnindex) << std::endl;
	std::string ress = GetLISList(data, pres, nnindex);
	std::cout << ress.c_str() << std::endl;


	std::cout << LIS3(data) << std::endl;

	std::cin.get();
	return 0;
}
