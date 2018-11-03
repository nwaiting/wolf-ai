#include <unordered_map>
#include <iostream>
#include <stdint.h>
#include <random>
#include <time.h>
#include <exception>
using namespace std;

/*
    unordered_map：存储时是根据key的hash值判断元素是否相同，即unordered_map内部元素是无序的
    map：而map中的元素是按照二叉搜索树存储，进行中序遍历会得到有序遍历

    如果需要内部元素自动排序，使用map，不需要排序使用unordered_map
    如果是自定义类型，那么就需要自己重载operator<或者hash_value()了

    cplusplus中明确指出m[key]和m.at(key)的差别是：
    对于map<class K, class T> m，当key不存在时，m[key]将调用T的默认构造函数，强制将序对<key, T()>插入，并返回T()的引用；而后者将抛出exception。
*/

void func1()
{
    unordered_map<int32_t, int32_t> umap_int;
    default_random_engine dre(time(NULL));
    uniform_int_distribution<> uni_int(1, 100);

    for (auto i = 0; i < 10; i++) {
        //插入值 方法1
        umap_int.insert(make_pair(i, uni_int(dre)));
        //插入值 方法2
        //map_int.insert(unordered_map<int32_t, int32_t>::value_type(uni_int(dre), i));
    }

    for (auto it : umap_int) {
        cout << it.first << "-" << it.second << endl;
    }

    for (auto it : { 1, 3, 5, 10 }) {
        //lookup if it exist
        cout << umap_int.count(it) << endl;
    }

    //find
    unordered_map<int32_t, int32_t>::const_iterator cite = umap_int.find(5);
    if (cite != umap_int.end()) {
        cout << "find " << cite->second << endl;
    }

    int32_t res = umap_int.at(9);
    cout << "key is 9, value is " << res << endl;

    umap_int.at(9) = 10086;
    cout << "key is 9, value is " << umap_int.at(9) << endl;

    try
    {
        res = umap_int.at(10);
        cout << "key is 10, value is " << res << endl;
    }
    catch (exception& e)
    {
        cout << e.what() << endl;
    }
}

int main()
{
    func1();

    cin.get();
    return 0;
}
