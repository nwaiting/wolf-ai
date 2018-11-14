#include <iostream>
#include <string>
#include <algorithm>
#include <stdint.h>

//反转字符串
void func1()
{
	std::string str1("123456");
	std::cout << str1 << std::endl;

	//方法1
	std::string str2(str1);
	std::reverse(str2.begin(), str2.end());
	std::cout << str2 << std::endl;

	//方法2
	std::string str3(str1);
	uint32_t i = 0, j = str3.size() - 1;
	while (i < j){
		std::swap(str3[i++], str3[j--]);
	}
	std::cout << str3 << std::endl;

	//方法3
	std::string str4;
	for (std::string::const_iterator strIte = str1.begin(); strIte != str1.end(); strIte++){
		str4.insert(str4.begin(), *strIte);
	}
	std::cout << str4 << std::endl;
}

int main()
{
	func1();

	std::cin.get();
	return 0;
}
