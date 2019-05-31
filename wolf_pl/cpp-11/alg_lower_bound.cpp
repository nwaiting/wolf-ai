#include <iostream>

/*
    lower_bound( )和upper_bound( )都是利用二分查找的方法在一个排好序的数组中进行查找的
    upper_bound：
        Returns an iterator pointing to the first element in the range [first,last) which compares greater than val.
        1、
            template <class ForwardIterator, class T>
            ForwardIterator upper_bound (ForwardIterator first, ForwardIterator last,const T& val);

        2、
            template <class ForwardIterator, class T, class Compare>
            ForwardIterator upper_bound (ForwardIterator first, ForwardIterator last,const T& val, Compare comp);

    lower_bound
        Returns an iterator pointing to the first element in the range [first,last) which does not compare less than val
        1、
            template <class ForwardIterator, class T>
            ForwardIterator lower_bound (ForwardIterator first, ForwardIterator last,const T& val);

        2、
            template <class ForwardIterator, class T, class Compare>
            ForwardIterator lower_bound (ForwardIterator first, ForwardIterator last,const T& val, Compare comp);

*/

int main(int argc, char const *argv[]) {
    /* code */
    return 0;
}
