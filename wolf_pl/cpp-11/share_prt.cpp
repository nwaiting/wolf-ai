//c++11
/*
参考：https://heleifz.github.io/14696398760857.html
unique_ptr：不允许多个对象管理一个指针
            注：1、

shared_ptr：允许多个对象管理同一个指针，但仅当管理这个指针的最后一个对象析构时才调用delete
            注：1、引用计数容易出现循环引用问题
*/

int main(int argc, char const *argv[]) {
    /* code */
    return 0;
}
