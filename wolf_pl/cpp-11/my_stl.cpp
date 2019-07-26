#include <iostream>


/*
    map是否是有序？
        map内部是红黑树，在插入元素时会自动排序

    两个元素键是否相等？
        map用它来判断两个key的大小，并返回bool类型的结果。
        利用这个函数，map可以确定元素在容器中遵循的顺序以及两个元素键是否相等（！comp（a，b）&&！comp（b，a）），确保map中没有两个元素可以具有等效键
        map 容器的比较函数在相等时不能返回 true，换句话说，不能使用<=或>=来比较。这是为什么？
        map或multimap容器用等价来判断键是否相等。如果表达式 key1<key2 和 key2<key1 的结果都是 false，那么 key1 和 key2 是等价的，所以它们被认为是相等的。
        换一种方式，等价意味着 !(key1<key2)&&!(key2<key1) 的运算值为 true


*/


int main(int argc, char const *argv[]) {
    /* code */
    return 0;
}
