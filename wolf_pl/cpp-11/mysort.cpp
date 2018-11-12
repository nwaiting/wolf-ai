#include <iostream>
#include <algorithm>
#include <stdlib.h>
#include <stdint.h>
#include <map>
#include <vector>
#include <functional>
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


        sort对list排序的问题：
            std:sort() 所使用的容器必須能支持隨機存取, 如: std::vector
            你使用的 std::list 非隨機存取的容器, std::list 排序可使用 std::list::sort() 自帶的來完成.

            注意：！！！！！
                sort算法只能对序列容器进行排序，就是线性的（如vector）
                map是一个集合容器，它里面存储的元素是pair，不是线性存储的（红黑树），所以利用sort不能直接和map结合进行排序

        如何对map自定义排序：
            方法1：初始化时自定义比较函数
            方法2：将集合容器转成序列容器，如将map转成vector，然后排序
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
// !!!!!!在这样的what()内部，整个*this对象被认为是const，这意味着m_message成员也是const。由于std::string的赋值运算符需要左侧的可修改对象（即非const对象），
//  因此不能将任何对象分配给常量合格的std::string对象。您正在提供const之一 !!!!!!
//注意：1、注意MapValueType的类型，如果直接使用std::pair<std::string, TestStruct*>类型好像没问题，使用MapValueType类型有问题
//     2、注意函数的const属性
//     3、直接对map排序也有问题
class CmpByValueClass
{
public:
    bool operator()(MapValueType &v1, MapValueType &v2) {
        return v1.second->a < v2.second->a;
    }
};

class CmpByValueClassPair
{
public:
    bool operator() (const std::pair<std::string, TestStruct*> &v1, const std::pair<std::string, TestStruct*> &v2) const {
        return v1.second->a < v2.second->a;
    }
};

bool CmpByValueFun(MapValueType &v1, MapValueType &v2)
{
    return v1.second->a < v2.second->a;
}

bool CmpByValueFunPair(const std::pair<std::string, TestStruct*> &v1, const std::pair<std::string, TestStruct*> &v2)
{
    return v1.second->a < v2.second->a;
}


//对map自定义排序函数
void func1()
{
    TestStruct aa(1, 2);
    m_map["aaa"] = &aa;
    TestStruct bb(3, 5);
    m_map["bbb"] = &bb;
    TestStruct cc(2, 3);
    m_map["ccc"] = &cc;
    
    /*
        提示错误：error C2784: 'unknown-type std::operator -(std::move_iterator<_RanIt> &,const std::move_iterator<_RanIt2> &)' : could not deduce template argument for 'std::move_iterator<_RanIt> &' from ...
    */
    //std::sort(m_map.begin(), m_map.end(), CmpByValueClass());
    //std::sort(m_map.begin(), m_map.end(), CmpByValueClassPair());
    //std::sort(m_map.begin(), m_map.end(), CmpByValueFunPair);
    //std::sort(m_map.begin(), m_map.end(), CmpByValueFunPair);
}

void func2()
{
    int a[20] = { 2, 4, 1, 23, 5, 76, 0, 43, 24, 65 };
    for (int32_t i = 0; i < 20; i++){
        cout << a[i] << " ";
    }
    cout << endl;

    std::sort(a, a + 20, less<int32_t>());
    for (int32_t i = 0; i < 20; i++){
        cout << a[i] << " ";
    }
    cout << endl;

    int b[20] = { 2, 4, 1, 23, 5, 76, 0, 43, 24, 65 };
    std::sort(b, b + 20, greater<int>());
    for (int32_t i = 0; i < 20; i++){
        cout << b[i] << " ";
    }
    cout << endl;
}

int main()
{
    //func1();

    func2();

    cin.get();
    return 0;
}
