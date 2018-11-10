#include <iostream>
#include <algorithm>
#include <stdlib.h>
#include <stdint.h>
#include <map>
#include <vector>
using namespace std;

/*
    qsort和sort的区别：
        qsort：
        include<stdlib.h>
        （基本快速排序的方法，每次把数组分成两部分和中间的一个划分值，而对于有多个重复值的数组来说，基本快速排序的效率较低，且不稳定）。集成在C语言库函数里面的的qsort函数，使用 三 路划分的方法解决排序这个问题。所谓三路划分，是指把数组划分成小于划分值，等于划分值和大于划分值的三个部分。
        具体介绍：-^^
            void qsort(void *base, int nelem, int width, int (*fcmp)(const void *,const void *));
            int compare (const void *elem1, const void *elem2 ) );

        qsort（即，quicksort）主要根据你给的比较条件给一个快速排序，主要是通过指针移动实现排序功能。排序之后的结果仍然放在原来数组中。
        参数意义如下:
            第一个参数 base 是 需要排序的目标数组名（或者也可以理解成开始排序的地址，因为可以写&s[i]这样的表达式）
            第二个参数 num 是 参与排序的目标数组元素个数
            第三个参数 width 是单个元素的大小（或者目标数组中每一个元素长度），推荐使用sizeof(s[0]）这样的表达式
            第四个参数 compare 就是让很多人觉得非常困惑的比较函数啦。

        sort：
            include<algorithm>
            sort是qsort的升级版，如果能用sort尽量用sort，使用也比较简单，不像qsort还得自己去写 cmp 函数
            与qsort同为排序函数，复杂度为n*log2(n)
            std::sort函数优于qsort的一些特点：对大数组采取9项取样，更完全的三路划分算法，更细致的对不同数组大小采用不同方法排序

            总结sort排序顺序：
                sort函数根据comp函数的返回值，对comp函数的两个参数排序。
                如果comp返回true，排序为“参数1”“参数2”，否则排序为“参数2”“参数1”。
                想要升序排列，则return parameter1<parameter2
                想要降序排列，则return parameter1>parameter2

        sort自定义比较函数：
            方法1：声明外部比较函数
                bool Less(const Student& s1, const Student& s2)
                {
                    return s1.name < s2.name; //从小到大排序
                }
                std::sort(sutVector.begin(), stuVector.end(), Less);
                注意：比较函数必须写在类外部（全局区域）或声明为静态函数
                当comp作为类的成员函数时，默认拥有一个this指针，这样和sort函数所需要使用的排序函数类型不一样。
                否则，会出现<unresolved overloaded function type>错误

            方法2：重载类的比较运算符
                bool operator<(const Student& s1, const Student& s2)
                {
                    return s1.name < s2.name; //从小到大排序
                }
                std::sort(sutVector.begin(), stuVector.end());
                
            方法3：声明比较类
            struct Less
            {
                bool operator()(const Student& s1, const Student& s2)
                {
                    return s1.name < s2.name; //从小到大排序
                }
            };

            std::sort(sutVector.begin(), stuVector.end(), Less());

    */

struct TestStruct{
    int32_t a;
    int32_t b;
    TestStruct(int32_t _a, int32_t _b) :a(_a), b(_b){}
    ~TestStruct(){}
};

std::map<std::string, TestStruct*> m_map;
typedef std::map<std::string, TestStruct*>::value_type MapValueType;

//这种实现有问题，会报错：错误C2678 二进制“=”: 没有找到接受“const std::string”类型的左操作数的运算符(或没有可接受的转换)
//由于在const函数中调用了非const函数
class CmpByValueClass
{
public:
    bool operator()(MapValueType &v1, MapValueType &v2) {
        if (v1.second->a < v2.second->a){
            return true;
        }
        return false;
    }
};

bool CmpByValueFun(MapValueType &v1, MapValueType &v2)
{
    if (v1.second->a < v2.second->a){
        return true;
    }
    return false;
}

void func1()
{
    TestStruct aa(1, 2);
    m_map["aaa"] = &aa;
    TestStruct bb(3, 5);
    m_map["bbb"] = &bb;
    TestStruct cc(2, 3);
    m_map["ccc"] = &cc;

    std::vector<MapValueType> vecs(m_map.begin(), m_map.end());
    //std::sort(vecs.begin(), vecs.end(), CmpByValueClass());
    std::sort(vecs.begin(), vecs.end(), CmpByValueFun);
}

int main()
{
    func1();
    cin.get();
    return 0;
}
