#include <iostream>
#include <vector>
#include <stdint.h>
#include <algorithm>
#include <functional>
#include <numeric>

/*
    http://c.biancheng.net/stl/algorithms/  c++详细基础

    算法1：sort()
    算法2：partial_sort()  实现局部排序，如寻找最大的前4个数
    算法3：nth_element()   实现取第几大的数据
    算法4：max_element()   取最大值或者索引
    算法5：min_element()   取最小值或索引
    算法6：find()  查找
    算法7：transform()	在指定的范围内应用于给定的操作，并将结果存储在指定的另一个范围内
    算法8：for_each()	在指定的范围内应用于给定的操作
	算法9：reverse()		反转排序容器内指定范围中的元素
	算法10：reverse_copy()	反转排序容器内指定范围中的元素,!!!!!!!! 注：输入和输出不能是同一个迭代器，即不能在内部反转
    算法11：iota(begin, end, start);   从start开始递增加1，从start开始递增加1，然后赋值到begin到end空间
    算法12：accumulate(begin, end, start); 从start开始累加到end，然后在加上start
    算法13：replace_if() 替换
*/


void Printf(const std::vector<int32_t> &vecInt)
{
    for (auto &it:vecInt) {
        std::cout << it << " ";
    }
    std::cout << std::endl;
}

//算法2：partial_sort()  实现局部排序，如寻找最大的前4个数
void func2()
{
    std::vector<int32_t> a = {1,5,6,200,324,45,756,96,78,32,5};
    std::partial_sort(a.begin(), a.begin()+3, a.end());
    Printf(a);

    std::partial_sort(a.begin(), a.begin() + 3, a.end(), std::greater<int32_t>());
    Printf(a);
}

//算法3：nth_element()   实现取第几大的数据，如取第3小的数，前3个就是最小的
void func3()
{
    std::vector<int32_t> a;
    //当数据较小时，对数据进行了全排序，每个平台实现不一样，当数据较大时，仅进行了部分排序
    for (auto i = 1; i <= 5000; i++){
        a.push_back(i);
    }
    std::random_shuffle(a.begin(), a.end());
    Printf(a);

    std::nth_element(a.begin(), a.begin() + 5, a.end());
    Printf(a);
}

//算法4：max_element()   取最大值或者索引
//算法5：min_element()   取最小值或索引
void func4()
{
    std::vector<int32_t> a;
    for (auto i = 1; i <= 10; i++){
        a.push_back(i);
    }
    std::random_shuffle(a.begin(), a.end());
    Printf(a);

    std::vector<int32_t>::iterator bigone = max_element(a.begin(), a.end());
    std::cout << *bigone << std::endl;      //获取最大值
    std::cout << bigone - a.begin() << std::endl;   //获取最大值的索引，从0开始

    std::vector<int32_t>::iterator smallone = min_element(a.begin(), a.end());
    std::cout << *smallone << std::endl;      //获取最大值
    std::cout << smallone - a.begin() << std::endl;   //获取最大值的索引，从0开始
}

//算法6：find()  查找
void func6()
{
    std::vector<int32_t> a;
    for (auto i = 1; i <= 10; i++){
        a.push_back(i);
    }
    std::random_shuffle(a.begin(), a.end());
    Printf(a);

    std::vector<int32_t>::iterator vecIte = std::find(a.begin(), a.end(), 5);
    std::cout << *vecIte << std::endl;
    std::cout << vecIte - a.begin() << std::endl;
}

// 算法7：transform()	在指定的范围内应用于给定的操作，并将结果存储在指定的另一个范围内
//		std::transform的两个声明，一个是对应于一元操作，一个是对应于二元操作
//		std::transform(first1, last1, first2, result, op_add);	详解：将first1和first2开头的范围内的每个元素相加，然后依次存储到result中
// 算法8：for_each()	在指定的范围内应用于给定的操作
// 算法7和算法8的区别：
// 1、直接改变元素；for_each()和transform()都具有这种能力
// 2、复制到另一个区间的过程中改变元素的值，这种情况下，源区间的值不会发生变化，只有transform()具有这种能力

int op_increase(int i) { return i+=1; }
int op_sum(int i, int j) { return i + j; }
void func7()
{
	std::vector<int32_t> a;
	for (auto i = 1; i <= 10; i++){
		a.push_back(i);
	}
	Printf(a);

	std::vector<int32_t> b(a);
	std::for_each(b.begin(), b.end(), [](int32_t &n){n *= 5; });
	Printf(b);

	std::vector<int32_t> b1(a);
	std::for_each(b1.begin(), b1.end(), op_increase);	//测试显示，如果op_increase中参数不适用引起，那么b1结果不会改变
	Printf(b1);

	std::vector<int32_t> b2(a);
	std::transform(b2.begin(), b2.end(), b2.begin(), op_increase);	//如果op_increase中参数不使用引用，那么b2中任然会被改变
	Printf(b2);

	std::vector<int32_t> c(a);
	std::vector<int32_t> d(a);
	std::transform(c.begin(), c.end(), d.begin(), c.begin(), op_sum);	//二元操作,将c和d开头的范围内的每个元素相加，然后依次存储到c中
	Printf(c);
	Printf(d);
}

//算法9：reverse()		反转排序容器内指定范围中的元素
//算法10：reverse_copy()	反转排序容器内指定范围中的元素
//		std::reverse_copy与std::reverse唯一的区别是：reverse_copy会将结果拷贝到另外一个容器中，而不影响原容器的内容。
void func9()
{
	std::vector<int32_t> data = {23,2342,45,645,56,32,55,9,32,342,943};
	Printf(data);

	std::vector<int32_t> data1(data);
	std::reverse(data1.begin(), data1.end());
	Printf(data1);

	std::vector<int32_t> data2(data);
	std::reverse_copy(data2.begin(), data2.end(), data2.begin());	//！！！！注：输入和输出为同一个空间，反转有问题
	Printf(data2);

	std::vector<int32_t> data4(data);
	std::vector<int32_t> data5(data4.size());	//!!!! data5必须要初始化空间大小
	std::reverse_copy(data4.begin(), data4.end(), data5.begin());
	Printf(data5);
}

//算法11：iota(begin, end, start);   从start开始递增加1，然后赋值到begin到end空间
//算法12：accumulate(begin, end, start); 从start开始累加到end，然后在加上start 头文件：#include <numeric>
//       accumulate (InputIterator first, InputIterator last, T init,BinaryOperation binary_op);  可自定义二元操作
int32_t myfunc11(int32_t x, int32_t y){ return x + 3 * y; }
void func11()
{
    std::vector<int32_t> data = { 1, 2, 3, 4, 5 };
    int32_t sum = std::accumulate(data.begin(), data.end(), 0);
    std::cout << "sum is " << sum << std::endl;

    std::vector<int32_t> data1(data);
    std::iota(data1.begin(), data1.end(), 50);
    Printf(data1);

    std::vector<int32_t> data2(data);
    int32_t sum2 = std::accumulate(data2.begin(), data2.end(), 50, myfunc11);
    std::cout << "sum2 is " << sum2 << std::endl;
}

int main()
{
    //func2();
    //func3();
    //func4();
    //func5();

	//func6();

	//func9();

    func11();

    std::cin.get();
    return 0;
}
