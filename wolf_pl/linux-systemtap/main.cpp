#include <iostream>
#include <unistd.h>
#include "main_i.h"


int main()
{
    Node a6 = Node();
    a6.value_ = 5;
    Node a7 = Node();
    a7.value_ = 7;
    Node a5 = Node();
    a5.value_ = 13;
    Node a4 = Node();
    a4.value_ = 9;
    Node a3 = Node();
    a3.value_ = 6;
    Node a2 = Node();
    a2.value_ = 8;
    Node a1 = Node();
    a1.value_ = 10;
    a1.left_ = &a2;
    a1.right_ = &a5;
    a2.left_ = &a3;
    a2.right_ = &a4;
    a3.left_ = &a6;
    a3.right_ = &a7;
    char *p = NULL;
    Solution *ps = new Solution();
    while(true) {
    	pre_list(&a1);
    	cout << ps->maxPathSum(&a1) << endl;
	sleep(2);
	}
    return 0;
}
