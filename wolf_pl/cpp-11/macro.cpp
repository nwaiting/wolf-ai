#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;

/*
    可变参数的宏定义
    #和##的用法
*/

//方法1 使用时候可以逗号后带参数，逗号后可以不带参数
// #的作用是对token进行连接，下面的定义中format、args、__VA_ARGS__ 都是token
#define LOG(format, ...) fprintf(stdout, format, ##__VA_ARGS__)

//c99中定义
//#define LOG(format, ...) fprintf(stdout, format, __VA_ARGS__)

//方法2 逗号后必须带参数
//gcc中支持
//#define LOG(format, args, ...) fprintf(stdout, format, ##args)


/*
    #和##的作用
    # 的功能是将后面的宏参数进行字符串化操作
    ## 的功能将前后两个子串连接起来形成一个新的子串
    注：1、凡是宏定义里有用#和##的地方宏参数是不会在展开，如_STRI(INT_MAX)中的INT_MAX就不会被展开为2147483647,如果想要使其中的宏参数展开，则需要多加一层中间转换 #define  STRI(s) _STRI(s)
        2、如果##前面有一些空格，##会吧前面的空格去掉完成强连接
*/
#define paster(n) cout<<"token"<<#n<<"="<<n<<endl;
#define _CONS(a,b) int(a##+##b)
#define _STRI(s) #s

//A1(a1, int);  等价于: int name_int_type;
//详解：在第一个宏定义中，”name”和第一个”_”之间，以及第2个”_”和第二个”type”之间没有被分隔，所以预处理器会把name_##type##_type解释成3段：“name_”、“type”、以及“_type”，这中间只有“type”是在宏前面出现过的，所以它可以被宏替换
//思想是用##分割成多段，看哪一段能被替换
#define A1(name, type)  type name_##type##_type


//A2(a1, int);  等价于: int a1_int_type;
//详解：而在第二个宏定义中，“name”和第一个“_”之间也被分隔了，所以预处理器会把name##_##type##_type解释成4段：“name”、“_”、“type”以及“_type”，这其间，就有两个可以被宏替换了。
//思想是用##分割成多段，看哪一段能被替换
#define A2(name, type)  type name##_##type##_type

int main()
{
    std::string addrres("hongkong");
    LOG("hello, welcome to %s\n", addrres.c_str());
    //方法2不可用
    LOG("hello end!!!\n");


    paster(9); //token9=9
    cout << _CONS(1, 2) << endl; //3
    cout << _STRI(INT_MAX) << endl; //INT_MAX
#define  STRI(s) _STRI(s)
    cout << STRI(INT_MAX) << endl; //2147483647

    cin.get();
    return 0;
}
